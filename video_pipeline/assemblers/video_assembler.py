"""
Video Assembler using Shotstack API
Combines images and audio into final video
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import aiohttp
import base64

logger = logging.getLogger(__name__)


class VideoAssembler:
    """Assemble videos using Shotstack API"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize video assembler

        Args:
            config: Configuration dictionary with Shotstack settings
        """
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("Shotstack API key is required")

        self.stage = config.get("stage", "v1")  # v1 (sandbox) or stage (production)
        self.base_url = f"https://api.shotstack.io/{self.stage}"
        self.output_dir = Path(config.get("output_dir", "outputs/videos"))
        self.poll_interval = config.get("poll_interval", 5)
        self.max_poll_time = config.get("max_poll_time", 600)
        self.default_fps = config.get("default_fps", 30)
        self.resolution = config.get("resolution", "1080")
        self.format = config.get("format", "mp4")

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers"""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def upload_asset(self, file_path: Path) -> str:
        """
        Upload asset to Shotstack

        Args:
            file_path: Path to file to upload

        Returns:
            Asset URL

        Raises:
            RuntimeError: If upload fails
        """
        logger.info(f"Uploading asset: {file_path.name}")

        # Read file as base64
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_base64 = base64.b64encode(file_data).decode('utf-8')

        # For now, return file path - Shotstack can use publicly accessible URLs
        # In production, you might want to upload to S3 or similar
        # For this implementation, we'll assume files are accessible or use data URLs
        logger.warning(
            f"Asset upload not implemented - using local path. "
            f"In production, upload {file_path} to S3/CDN first."
        )

        return str(file_path.absolute()).replace('\\', '/')

    def create_timeline(self, images: List[Path], audio: Optional[Path] = None,
                       image_duration: float = 3.0,
                       transition: str = "fade") -> Dict[str, Any]:
        """
        Create Shotstack timeline from images and audio

        Args:
            images: List of image paths
            audio: Optional audio path for narration
            image_duration: Duration each image is displayed (seconds)
            transition: Transition type between images

        Returns:
            Timeline dictionary
        """
        logger.info(f"Creating timeline with {len(images)} images")

        tracks = []
        current_time = 0.0

        # Image track
        image_clips = []
        for i, image_path in enumerate(images):
            clip = {
                "asset": {
                    "type": "image",
                    "src": str(image_path.absolute()).replace('\\', '/')
                },
                "start": current_time,
                "length": image_duration,
                "transition": {
                    "in": transition,
                    "out": transition
                } if i > 0 else None,
                "effect": "zoomIn"  # Ken Burns effect
            }
            image_clips.append(clip)
            current_time += image_duration

        tracks.append({
            "clips": image_clips
        })

        # Audio track
        if audio:
            audio_clip = {
                "asset": {
                    "type": "audio",
                    "src": str(audio.absolute()).replace('\\', '/')
                },
                "start": 0,
                "length": current_time
            }
            tracks.append({
                "clips": [audio_clip]
            })

        timeline = {
            "tracks": tracks
        }

        logger.debug(f"Timeline created with {len(tracks)} tracks, duration: {current_time}s")
        return timeline

    async def create_edit(self, timeline: Dict[str, Any],
                         output_format: Optional[str] = None,
                         resolution: Optional[str] = None,
                         fps: Optional[int] = None) -> str:
        """
        Create video edit/render job

        Args:
            timeline: Timeline configuration
            output_format: Output format (mp4, gif, etc.)
            resolution: Resolution preset (preview, mobile, sd, hd, 1080)
            fps: Frames per second

        Returns:
            Render ID

        Raises:
            RuntimeError: If creation fails
        """
        output_format = output_format or self.format
        resolution = resolution or self.resolution
        fps = fps or self.default_fps

        payload = {
            "timeline": timeline,
            "output": {
                "format": output_format,
                "resolution": resolution,
                "fps": fps
            }
        }

        logger.info(
            f"Creating render job: {output_format} @ {resolution}p, {fps}fps"
        )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/render",
                    json=payload,
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status not in (200, 201):
                        error_text = await response.text()
                        raise RuntimeError(
                            f"Failed to create render: {response.status} - {error_text}"
                        )

                    result = await response.json()
                    render_id = result.get("response", {}).get("id")

                    if not render_id:
                        raise RuntimeError("No render ID returned from Shotstack")

                    logger.info(f"Render job created with ID: {render_id}")
                    return render_id

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Shotstack API request failed: {e}")

    async def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        Get render job status

        Args:
            render_id: Render job ID

        Returns:
            Status information

        Raises:
            RuntimeError: If status check fails
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/render/{render_id}",
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(
                            f"Failed to get render status: {response.status} - {error_text}"
                        )

                    result = await response.json()
                    return result.get("response", {})

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Shotstack API request failed: {e}")

    async def wait_for_render(self, render_id: str) -> str:
        """
        Wait for render to complete and return video URL

        Args:
            render_id: Render job ID

        Returns:
            Video URL

        Raises:
            TimeoutError: If render exceeds max poll time
            RuntimeError: If render fails
        """
        logger.info(f"Waiting for render {render_id} to complete...")

        start_time = time.time()
        last_progress = -1

        while True:
            # Check timeout
            if time.time() - start_time > self.max_poll_time:
                raise TimeoutError(
                    f"Render exceeded timeout of {self.max_poll_time}s"
                )

            # Get status
            status_data = await self.get_render_status(render_id)
            status = status_data.get("status")

            # Log progress
            if "data" in status_data:
                progress = status_data["data"].get("progress", 0)
                if progress != last_progress:
                    logger.info(f"Render progress: {progress}%")
                    last_progress = progress

            # Check completion
            if status == "done":
                video_url = status_data.get("url")
                if not video_url:
                    raise RuntimeError("Render completed but no URL returned")

                logger.info(f"Render completed successfully: {video_url}")
                return video_url

            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                raise RuntimeError(f"Render failed: {error}")

            elif status in ("queued", "fetching", "rendering"):
                # Still processing, wait and retry
                await asyncio.sleep(self.poll_interval)

            else:
                logger.warning(f"Unknown render status: {status}")
                await asyncio.sleep(self.poll_interval)

    async def download_video(self, video_url: str,
                           output_filename: Optional[str] = None) -> Path:
        """
        Download rendered video

        Args:
            video_url: URL to download video from
            output_filename: Optional output filename

        Returns:
            Path to downloaded video

        Raises:
            RuntimeError: If download fails
        """
        logger.info(f"Downloading video from {video_url}")

        if not output_filename:
            import time
            output_filename = f"video_{int(time.time())}.{self.format}"

        output_path = self.output_dir / output_filename

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    video_url,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status != 200:
                        raise RuntimeError(
                            f"Failed to download video: {response.status}"
                        )

                    video_data = await response.read()

                    with open(output_path, 'wb') as f:
                        f.write(video_data)

                    logger.info(
                        f"Video downloaded to {output_path} ({len(video_data)} bytes)"
                    )
                    return output_path

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Video download failed: {e}")

    async def assemble_video(self, images: List[Path], audio: Optional[Path] = None,
                           image_duration: float = 3.0,
                           output_filename: Optional[str] = None) -> Path:
        """
        Complete video assembly workflow

        Args:
            images: List of image paths
            audio: Optional audio path
            image_duration: Duration each image is displayed
            output_filename: Optional output filename

        Returns:
            Path to final video

        Raises:
            RuntimeError: If assembly fails
        """
        logger.info(f"Starting video assembly with {len(images)} images")

        # Create timeline
        timeline = self.create_timeline(images, audio, image_duration)

        # Create render job
        render_id = await self.create_edit(timeline)

        # Wait for completion
        video_url = await self.wait_for_render(render_id)

        # Download video
        video_path = await self.download_video(video_url, output_filename)

        logger.info(f"Video assembly complete: {video_path}")
        return video_path


if __name__ == "__main__":
    # Test video assembler
    import sys
    import os

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def test():
        api_key = os.getenv("SHOTSTACK_API_KEY")
        if not api_key:
            print("ERROR: SHOTSTACK_API_KEY environment variable not set!")
            print("Set it with: export SHOTSTACK_API_KEY='your_key_here'")
            sys.exit(1)

        config = {
            "api_key": api_key,
            "stage": "v1",  # Use sandbox stage for testing
            "output_dir": "outputs/videos/test",
            "poll_interval": 3,
            "max_poll_time": 300
        }

        assembler = VideoAssembler(config)

        # Test with dummy image paths (you'll need actual images)
        print("\nNote: This test requires actual image files.")
        print("Create test images or update the paths below.\n")

        # Example usage (commented out - requires real files)
        # images = [
        #     Path("test_image_1.jpg"),
        #     Path("test_image_2.jpg"),
        #     Path("test_image_3.jpg")
        # ]
        # audio = Path("test_audio.mp3")
        #
        # try:
        #     video_path = await assembler.assemble_video(
        #         images=images,
        #         audio=audio,
        #         image_duration=3.0,
        #         output_filename="test_video.mp4"
        #     )
        #     print(f"\nSuccess! Video saved to: {video_path}")
        # except Exception as e:
        #     print(f"\nError: {e}")
        #     sys.exit(1)

        print("Video assembler initialized successfully.")
        print("Update the test code with real image/audio paths to test rendering.")

    asyncio.run(test())
