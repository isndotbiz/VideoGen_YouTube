"""
YouTube Uploader
Handles video upload to YouTube using Google API
"""

import logging
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeUploader:
    """Upload videos to YouTube"""

    # OAuth scopes required for YouTube upload
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ]

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize YouTube uploader

        Args:
            config: Configuration dictionary with YouTube settings
        """
        self.credentials_path = Path(config.get(
            "credentials_path",
            "credentials/youtube_credentials.json"
        ))
        self.token_path = Path(config.get(
            "token_path",
            "credentials/youtube_token.json"
        ))
        self.scopes = config.get("scopes", self.SCOPES)
        self.default_privacy = config.get("default_privacy", "private")
        self.default_category = config.get("default_category", "22")  # People & Blogs

        self.youtube = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            try:
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
                logger.info("Loaded existing YouTube credentials")
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed YouTube credentials")
                except Exception as e:
                    logger.warning(f"Failed to refresh credentials: {e}")
                    creds = None

            if not creds:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"YouTube credentials file not found: {self.credentials_path}\n"
                        f"Download OAuth 2.0 credentials from Google Cloud Console:\n"
                        f"1. Go to https://console.cloud.google.com/apis/credentials\n"
                        f"2. Create OAuth 2.0 Client ID (Desktop application)\n"
                        f"3. Download JSON and save as {self.credentials_path}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path),
                    self.scopes
                )
                creds = flow.run_local_server(port=0)
                logger.info("Obtained new YouTube credentials")

            # Save credentials
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            logger.info(f"Saved YouTube credentials to {self.token_path}")

        # Build YouTube service
        self.youtube = build('youtube', 'v3', credentials=creds)
        logger.info("YouTube API service initialized")

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        category_id: Optional[str] = None,
        privacy_status: Optional[str] = None,
        thumbnail_path: Optional[Path] = None,
        playlist_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube

        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: Privacy status (public, unlisted, private)
            thumbnail_path: Optional custom thumbnail
            playlist_id: Optional playlist to add video to

        Returns:
            Upload response with video ID and details

        Raises:
            FileNotFoundError: If video file doesn't exist
            HttpError: If upload fails
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        privacy_status = privacy_status or self.default_privacy
        category_id = category_id or self.default_category
        tags = tags or []

        logger.info(f"Uploading video: {title}")
        logger.info(f"  File: {video_path}")
        logger.info(f"  Privacy: {privacy_status}")

        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        # Create media upload
        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,  # Upload in single request
            resumable=True,
            mimetype='video/*'
        )

        try:
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")

            video_id = response['id']
            logger.info(f"Video uploaded successfully! Video ID: {video_id}")
            logger.info(f"Video URL: https://www.youtube.com/watch?v={video_id}")

            # Set custom thumbnail if provided
            if thumbnail_path and thumbnail_path.exists():
                self.set_thumbnail(video_id, thumbnail_path)

            # Add to playlist if specified
            if playlist_id:
                self.add_to_playlist(video_id, playlist_id)

            return {
                'id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'title': title,
                'privacy_status': privacy_status,
                'response': response
            }

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise

    def set_thumbnail(self, video_id: str, thumbnail_path: Path):
        """
        Set custom thumbnail for video

        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image

        Raises:
            FileNotFoundError: If thumbnail doesn't exist
            HttpError: If setting thumbnail fails
        """
        if not thumbnail_path.exists():
            raise FileNotFoundError(f"Thumbnail not found: {thumbnail_path}")

        logger.info(f"Setting thumbnail for video {video_id}")

        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path))
            ).execute()

            logger.info("Thumbnail set successfully")

        except HttpError as e:
            logger.error(f"Failed to set thumbnail: {e}")
            raise

    def add_to_playlist(self, video_id: str, playlist_id: str):
        """
        Add video to playlist

        Args:
            video_id: YouTube video ID
            playlist_id: YouTube playlist ID

        Raises:
            HttpError: If adding to playlist fails
        """
        logger.info(f"Adding video {video_id} to playlist {playlist_id}")

        try:
            self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()

            logger.info("Video added to playlist successfully")

        except HttpError as e:
            logger.error(f"Failed to add to playlist: {e}")
            raise

    def create_playlist(self, title: str, description: str = "",
                       privacy_status: str = "private") -> str:
        """
        Create a new playlist

        Args:
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy status (public, unlisted, private)

        Returns:
            Playlist ID

        Raises:
            HttpError: If creation fails
        """
        logger.info(f"Creating playlist: {title}")

        try:
            response = self.youtube.playlists().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': title,
                        'description': description
                    },
                    'status': {
                        'privacyStatus': privacy_status
                    }
                }
            ).execute()

            playlist_id = response['id']
            logger.info(f"Playlist created successfully! ID: {playlist_id}")
            return playlist_id

        except HttpError as e:
            logger.error(f"Failed to create playlist: {e}")
            raise

    def update_video(self, video_id: str, title: Optional[str] = None,
                    description: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    privacy_status: Optional[str] = None):
        """
        Update video metadata

        Args:
            video_id: YouTube video ID
            title: New title
            description: New description
            tags: New tags
            privacy_status: New privacy status

        Raises:
            HttpError: If update fails
        """
        logger.info(f"Updating video {video_id}")

        try:
            # Get current video details
            video = self.youtube.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()

            if not video['items']:
                raise ValueError(f"Video {video_id} not found")

            video_data = video['items'][0]
            snippet = video_data['snippet']
            status = video_data['status']

            # Update fields
            if title:
                snippet['title'] = title
            if description is not None:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags
            if privacy_status:
                status['privacyStatus'] = privacy_status

            # Submit update
            self.youtube.videos().update(
                part='snippet,status',
                body={
                    'id': video_id,
                    'snippet': snippet,
                    'status': status
                }
            ).execute()

            logger.info("Video updated successfully")

        except HttpError as e:
            logger.error(f"Failed to update video: {e}")
            raise

    def delete_video(self, video_id: str):
        """
        Delete video from YouTube

        Args:
            video_id: YouTube video ID

        Raises:
            HttpError: If deletion fails
        """
        logger.info(f"Deleting video {video_id}")

        try:
            self.youtube.videos().delete(id=video_id).execute()
            logger.info("Video deleted successfully")

        except HttpError as e:
            logger.error(f"Failed to delete video: {e}")
            raise


if __name__ == "__main__":
    # Test YouTube uploader
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    def test():
        config = {
            "credentials_path": "credentials/youtube_credentials.json",
            "token_path": "credentials/youtube_token.json",
            "default_privacy": "private"
        }

        try:
            uploader = YouTubeUploader(config)
            print("\nYouTube uploader initialized successfully!")
            print("Authentication complete.")
            print("\nTo upload a video, use:")
            print("  uploader.upload_video(")
            print("    video_path=Path('your_video.mp4'),")
            print("    title='Your Video Title',")
            print("    description='Video description',")
            print("    tags=['tag1', 'tag2']")
            print("  )")

        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)

    test()
