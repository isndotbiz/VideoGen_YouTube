#!/usr/bin/env python3
"""
Comprehensive Music Library Manager for Epidemic Sound Tracks
Organizes, catalogs, and provides easy access to downloaded music tracks

Features:
- Smart indexing and metadata extraction
- Platform-specific track selection (YouTube, TikTok, Instagram, etc.)
- Usage tracking and statistics
- Favorite/rating system
- Auto-mixing with platform-appropriate volumes
- CLI interface for easy searching and recommendations

Author: Music Library Manager
Date: 2025-12-22
"""

import os
import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("[WARNING] mutagen not installed. Install with: pip install mutagen")
    print("[INFO] Limited metadata extraction will be used")


class MusicLibraryManager:
    """Comprehensive music library management system"""

    def __init__(self, music_dir="background_music", metadata_file="music_library_metadata.json"):
        self.music_dir = Path(music_dir)
        self.metadata_file = Path(metadata_file)
        self.metadata = self._load_metadata()

        # Platform configurations for audio mixing
        self.platform_configs = {
            "youtube": {
                "bg_music_volume_db": -25,  # dB reduction
                "bg_music_volume_percent": 15,  # 15% of narration
                "optimal_bpm": (60, 90),
                "preferred_moods": ["calm", "uplifting", "ambient", "motivational"],
                "max_energy": "medium"
            },
            "tiktok": {
                "bg_music_volume_db": -15,
                "bg_music_volume_percent": 30,
                "optimal_bpm": (100, 140),
                "preferred_moods": ["energetic", "upbeat", "trendy", "dynamic"],
                "max_energy": "high"
            },
            "instagram": {
                "bg_music_volume_db": -18,
                "bg_music_volume_percent": 25,
                "optimal_bpm": (90, 120),
                "preferred_moods": ["uplifting", "trendy", "upbeat", "motivational"],
                "max_energy": "medium-high"
            },
            "podcast": {
                "bg_music_volume_db": -30,
                "bg_music_volume_percent": 10,
                "optimal_bpm": (50, 70),
                "preferred_moods": ["calm", "ambient", "background", "subtle"],
                "max_energy": "low"
            },
            "shorts": {
                "bg_music_volume_db": -20,
                "bg_music_volume_percent": 20,
                "optimal_bpm": (110, 130),
                "preferred_moods": ["upbeat", "energetic", "dynamic"],
                "max_energy": "medium-high"
            }
        }

    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load metadata: {e}")
                return {"tracks": {}, "usage": {}, "favorites": [], "stats": {}}
        return {"tracks": {}, "usage": {}, "favorites": [], "stats": {}}

    def _save_metadata(self):
        """Save metadata to JSON file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save metadata: {e}")

    def _get_file_hash(self, file_path: Path) -> str:
        """Generate unique hash for file"""
        return hashlib.md5(str(file_path.absolute()).encode()).hexdigest()[:16]

    def _extract_metadata_from_filename(self, filename: str) -> Dict:
        """Extract metadata from Epidemic Sound filename format"""
        # Format: ES_Title - Artist.mp3
        metadata = {
            "title": filename,
            "artist": "Unknown",
            "source": "epidemic_sound" if filename.startswith("ES_") else "unknown"
        }

        if filename.startswith("ES_"):
            # Remove ES_ prefix and .mp3 extension
            name = filename[3:].replace('.mp3', '')

            # Split by " - " to get title and artist
            if " - " in name:
                parts = name.split(" - ", 1)
                metadata["title"] = parts[0].strip()
                metadata["artist"] = parts[1].strip()

                # Remove duplicate number suffix like (1)
                if metadata["artist"].endswith(')') and '(' in metadata["artist"]:
                    base_artist = metadata["artist"].rsplit('(', 1)[0].strip()
                    if base_artist:
                        metadata["artist"] = base_artist
            else:
                metadata["title"] = name

        return metadata

    def _extract_audio_metadata(self, file_path: Path) -> Dict:
        """Extract audio metadata using mutagen if available"""
        metadata = {
            "duration": 0,
            "bitrate": 0,
            "sample_rate": 0,
            "channels": 0
        }

        if not MUTAGEN_AVAILABLE:
            return metadata

        try:
            audio = MP3(file_path)
            metadata["duration"] = audio.info.length
            metadata["bitrate"] = audio.info.bitrate
            metadata["sample_rate"] = audio.info.sample_rate
            metadata["channels"] = audio.info.channels
        except Exception as e:
            print(f"[WARNING] Could not extract audio metadata from {file_path.name}: {e}")

        return metadata

    def _infer_mood_from_title(self, title: str) -> str:
        """Infer mood from track title using keyword matching"""
        title_lower = title.lower()

        mood_keywords = {
            "calm": ["calm", "peace", "serene", "tranquil", "quiet", "gentle", "soft"],
            "uplifting": ["uplift", "inspire", "rise", "soar", "ascend", "elevate", "hope"],
            "energetic": ["energy", "power", "dynamic", "intense", "drive", "pulse", "vibrant"],
            "ambient": ["ambient", "atmosphere", "space", "drift", "float", "ether", "cosmic"],
            "motivational": ["motivate", "success", "achieve", "triumph", "victory", "champion"],
            "upbeat": ["upbeat", "happy", "joy", "cheerful", "bright", "sunny", "positive"],
            "dark": ["dark", "shadow", "night", "mysterious", "sinister", "ominous"],
            "epic": ["epic", "grand", "massive", "majestic", "heroic", "cinematic"],
            "emotional": ["emotion", "heart", "feel", "sentiment", "tender", "touch"],
            "background": ["background", "underscore", "subtle", "minimal", "simple"]
        }

        for mood, keywords in mood_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return mood

        return "neutral"

    def _infer_bpm_from_mood(self, mood: str) -> int:
        """Estimate BPM based on mood"""
        bpm_ranges = {
            "calm": (50, 70),
            "ambient": (60, 75),
            "background": (65, 80),
            "uplifting": (80, 110),
            "motivational": (90, 120),
            "upbeat": (110, 130),
            "energetic": (120, 140),
            "epic": (80, 100),
            "emotional": (60, 90),
            "dark": (70, 95),
            "neutral": (80, 100)
        }

        bpm_range = bpm_ranges.get(mood, (80, 100))
        return random.randint(bpm_range[0], bpm_range[1])

    def _calculate_platform_score(self, track: Dict, platform: str) -> float:
        """Calculate suitability score for platform (0-100)"""
        if platform not in self.platform_configs:
            return 50.0  # Default neutral score

        config = self.platform_configs[platform]
        score = 50.0  # Start with neutral

        # Check BPM match
        track_bpm = track.get("bpm", 80)
        optimal_bpm = config["optimal_bpm"]
        if optimal_bpm[0] <= track_bpm <= optimal_bpm[1]:
            score += 20  # Good BPM match
        elif abs(track_bpm - optimal_bpm[0]) < 15 or abs(track_bpm - optimal_bpm[1]) < 15:
            score += 10  # Close match

        # Check mood match
        track_mood = track.get("mood", "neutral")
        if track_mood in config["preferred_moods"]:
            score += 25  # Perfect mood match

        # Boost score for favorites
        if track.get("is_favorite", False):
            score += 10

        # Reduce score if overused
        usage_count = track.get("usage_count", 0)
        if usage_count > 5:
            score -= min(usage_count * 2, 20)

        return max(0, min(100, score))

    def scan_library(self, force_rescan=False):
        """Scan music directory and build/update index"""
        print("\n" + "="*70)
        print("SCANNING MUSIC LIBRARY")
        print("="*70)

        if not self.music_dir.exists():
            print(f"[ERROR] Music directory not found: {self.music_dir}")
            return

        # Find all MP3 files
        mp3_files = list(self.music_dir.glob("*.mp3"))
        print(f"\n[FOUND] {len(mp3_files)} MP3 files in {self.music_dir}")

        new_tracks = 0
        updated_tracks = 0

        for mp3_file in mp3_files:
            file_hash = self._get_file_hash(mp3_file)

            # Check if already indexed
            if file_hash in self.metadata["tracks"] and not force_rescan:
                continue

            print(f"\n[INDEXING] {mp3_file.name}")

            # Extract metadata
            filename_meta = self._extract_metadata_from_filename(mp3_file.name)
            audio_meta = self._extract_audio_metadata(mp3_file)

            # Infer mood and BPM
            mood = self._infer_mood_from_title(filename_meta["title"])
            bpm = self._infer_bpm_from_mood(mood)

            # Build track metadata
            track_data = {
                "file_path": str(mp3_file.absolute()),
                "filename": mp3_file.name,
                "file_hash": file_hash,
                "title": filename_meta["title"],
                "artist": filename_meta["artist"],
                "source": filename_meta["source"],
                "mood": mood,
                "bpm": bpm,
                "duration": audio_meta["duration"],
                "bitrate": audio_meta["bitrate"],
                "sample_rate": audio_meta["sample_rate"],
                "channels": audio_meta["channels"],
                "file_size_mb": mp3_file.stat().st_size / (1024 * 1024),
                "indexed_date": datetime.now().isoformat(),
                "usage_count": 0,
                "rating": 0,
                "is_favorite": False,
                "tags": [],
                "notes": ""
            }

            if file_hash in self.metadata["tracks"]:
                updated_tracks += 1
            else:
                new_tracks += 1

            self.metadata["tracks"][file_hash] = track_data

            print(f"  Title: {track_data['title']}")
            print(f"  Artist: {track_data['artist']}")
            print(f"  Mood: {track_data['mood']}")
            print(f"  BPM: {track_data['bpm']}")
            print(f"  Duration: {track_data['duration']:.1f}s")

        # Save metadata
        self._save_metadata()

        print("\n" + "="*70)
        print(f"[COMPLETE] Scan complete!")
        print(f"  New tracks: {new_tracks}")
        print(f"  Updated tracks: {updated_tracks}")
        print(f"  Total indexed: {len(self.metadata['tracks'])}")
        print("="*70)

    def search_tracks(self, query: str, limit: int = 10) -> List[Dict]:
        """Search tracks by query string"""
        query_lower = query.lower()
        results = []

        for track_hash, track in self.metadata["tracks"].items():
            # Search in title, artist, mood, tags
            searchable = f"{track['title']} {track['artist']} {track['mood']} {' '.join(track.get('tags', []))}".lower()

            if query_lower in searchable:
                results.append(track)

        # Sort by relevance (title matches first, then usage count)
        results.sort(key=lambda x: (
            query_lower in x['title'].lower(),
            -x['usage_count']
        ), reverse=True)

        return results[:limit]

    def get_music_for_platform(self, platform: str, duration: Optional[int] = None,
                               mood: Optional[str] = None) -> Optional[Dict]:
        """Get best matching track for platform"""
        if platform not in self.platform_configs:
            print(f"[WARNING] Unknown platform: {platform}. Using default.")
            platform = "youtube"

        # Filter tracks
        candidates = []
        for track_hash, track in self.metadata["tracks"].items():
            # Filter by duration if specified
            if duration and track["duration"] > 0:
                if abs(track["duration"] - duration) > 30:  # Within 30 seconds
                    continue

            # Filter by mood if specified
            if mood and track["mood"] != mood:
                continue

            # Calculate platform score
            score = self._calculate_platform_score(track, platform)
            candidates.append((score, track))

        if not candidates:
            print("[WARNING] No suitable tracks found")
            return None

        # Sort by score
        candidates.sort(key=lambda x: x[0], reverse=True)

        return candidates[0][1]

    def get_random_music(self, platform: str, filters: Optional[Dict] = None) -> Optional[Dict]:
        """Get random track matching filters"""
        filters = filters or {}

        # Filter tracks
        candidates = []
        for track_hash, track in self.metadata["tracks"].items():
            # Apply filters
            if "mood" in filters and track["mood"] != filters["mood"]:
                continue
            if "min_bpm" in filters and track["bpm"] < filters["min_bpm"]:
                continue
            if "max_bpm" in filters and track["bpm"] > filters["max_bpm"]:
                continue
            if "artist" in filters and track["artist"] != filters["artist"]:
                continue
            if "favorites_only" in filters and filters["favorites_only"] and not track["is_favorite"]:
                continue

            candidates.append(track)

        if not candidates:
            return None

        return random.choice(candidates)

    def get_music_rotation(self, platform: str, video_count: int, filters: Optional[Dict] = None) -> List[Dict]:
        """Get N different tracks for rotation (no repeats)"""
        filters = filters or {}

        # Get all suitable tracks
        all_tracks = []
        for track_hash, track in self.metadata["tracks"].items():
            # Apply filters
            if "mood" in filters and track["mood"] != filters["mood"]:
                continue
            if "min_bpm" in filters and track["bpm"] < filters["min_bpm"]:
                continue
            if "max_bpm" in filters and track["bpm"] > filters["max_bpm"]:
                continue

            # Calculate platform score
            score = self._calculate_platform_score(track, platform)
            all_tracks.append((score, track))

        # Sort by score
        all_tracks.sort(key=lambda x: x[0], reverse=True)

        # Take top tracks, ensuring variety
        selected = []
        used_artists = set()

        for score, track in all_tracks:
            if len(selected) >= video_count:
                break

            # Prefer different artists for variety
            if track["artist"] not in used_artists or len(selected) < video_count // 2:
                selected.append(track)
                used_artists.add(track["artist"])

        # If we need more tracks, add remaining regardless of artist
        if len(selected) < video_count:
            for score, track in all_tracks:
                if track not in selected:
                    selected.append(track)
                    if len(selected) >= video_count:
                        break

        return selected

    def track_usage(self, track_hash: str, video_title: str, platform: str):
        """Record track usage in a video"""
        if track_hash not in self.metadata["tracks"]:
            print(f"[WARNING] Track hash not found: {track_hash}")
            return

        # Update usage count
        self.metadata["tracks"][track_hash]["usage_count"] += 1

        # Record usage details
        usage_key = f"{track_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.metadata["usage"][usage_key] = {
            "track_hash": track_hash,
            "track_title": self.metadata["tracks"][track_hash]["title"],
            "video_title": video_title,
            "platform": platform,
            "date": datetime.now().isoformat()
        }

        self._save_metadata()

    def set_rating(self, track_hash: str, rating: int):
        """Set track rating (0-5 stars)"""
        if track_hash not in self.metadata["tracks"]:
            print(f"[WARNING] Track hash not found: {track_hash}")
            return

        rating = max(0, min(5, rating))
        self.metadata["tracks"][track_hash]["rating"] = rating
        self._save_metadata()

    def toggle_favorite(self, track_hash: str):
        """Toggle favorite status"""
        if track_hash not in self.metadata["tracks"]:
            print(f"[WARNING] Track hash not found: {track_hash}")
            return

        current = self.metadata["tracks"][track_hash].get("is_favorite", False)
        self.metadata["tracks"][track_hash]["is_favorite"] = not current

        # Update favorites list
        if not current:
            if track_hash not in self.metadata["favorites"]:
                self.metadata["favorites"].append(track_hash)
        else:
            if track_hash in self.metadata["favorites"]:
                self.metadata["favorites"].remove(track_hash)

        self._save_metadata()

        status = "added to" if not current else "removed from"
        print(f"[UPDATED] Track {status} favorites")

    def get_library_stats(self) -> Dict:
        """Generate comprehensive library statistics"""
        stats = {
            "total_tracks": len(self.metadata["tracks"]),
            "total_duration_hours": 0,
            "total_size_mb": 0,
            "moods": {},
            "bpm_distribution": {"0-60": 0, "60-80": 0, "80-100": 0, "100-120": 0, "120+": 0},
            "artists": {},
            "sources": {},
            "favorites": len(self.metadata["favorites"]),
            "total_usage": len(self.metadata["usage"]),
            "most_used": [],
            "least_used": [],
            "platform_breakdown": {}
        }

        # Process all tracks
        for track_hash, track in self.metadata["tracks"].items():
            # Duration
            stats["total_duration_hours"] += track.get("duration", 0) / 3600

            # Size
            stats["total_size_mb"] += track.get("file_size_mb", 0)

            # Moods
            mood = track.get("mood", "unknown")
            stats["moods"][mood] = stats["moods"].get(mood, 0) + 1

            # BPM
            bpm = track.get("bpm", 0)
            if bpm < 60:
                stats["bpm_distribution"]["0-60"] += 1
            elif bpm < 80:
                stats["bpm_distribution"]["60-80"] += 1
            elif bpm < 100:
                stats["bpm_distribution"]["80-100"] += 1
            elif bpm < 120:
                stats["bpm_distribution"]["100-120"] += 1
            else:
                stats["bpm_distribution"]["120+"] += 1

            # Artists
            artist = track.get("artist", "Unknown")
            stats["artists"][artist] = stats["artists"].get(artist, 0) + 1

            # Sources
            source = track.get("source", "unknown")
            stats["sources"][source] = stats["sources"].get(source, 0) + 1

        # Most/least used
        tracks_by_usage = sorted(
            [(track["usage_count"], track["title"], track_hash)
             for track_hash, track in self.metadata["tracks"].items()],
            key=lambda x: x[0],
            reverse=True
        )

        stats["most_used"] = tracks_by_usage[:5]
        stats["least_used"] = [t for t in tracks_by_usage if t[0] == 0][:5]

        # Platform breakdown
        for usage_key, usage in self.metadata["usage"].items():
            platform = usage.get("platform", "unknown")
            stats["platform_breakdown"][platform] = stats["platform_breakdown"].get(platform, 0) + 1

        return stats

    def print_stats(self):
        """Print library statistics"""
        stats = self.get_library_stats()

        print("\n" + "="*70)
        print("MUSIC LIBRARY STATISTICS")
        print("="*70)

        print(f"\nOVERVIEW:")
        print(f"  Total Tracks: {stats['total_tracks']}")
        print(f"  Total Duration: {stats['total_duration_hours']:.1f} hours")
        print(f"  Total Size: {stats['total_size_mb']:.1f} MB")
        print(f"  Favorites: {stats['favorites']}")
        print(f"  Total Usage: {stats['total_usage']} times")

        print(f"\nMOOD DISTRIBUTION:")
        for mood, count in sorted(stats['moods'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_tracks']) * 100
            print(f"  {mood.capitalize()}: {count} ({percentage:.1f}%)")

        print(f"\nBPM DISTRIBUTION:")
        for bpm_range, count in stats['bpm_distribution'].items():
            percentage = (count / stats['total_tracks']) * 100 if stats['total_tracks'] > 0 else 0
            print(f"  {bpm_range} BPM: {count} ({percentage:.1f}%)")

        print(f"\nTOP ARTISTS:")
        for artist, count in sorted(stats['artists'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {artist}: {count} tracks")

        print(f"\nSOURCES:")
        for source, count in stats['sources'].items():
            print(f"  {source}: {count} tracks")

        if stats['most_used']:
            print(f"\nMOST USED TRACKS:")
            for usage, title, _ in stats['most_used']:
                if usage > 0:
                    print(f"  {title}: {usage} times")

        if stats['platform_breakdown']:
            print(f"\nPLATFORM USAGE:")
            for platform, count in sorted(stats['platform_breakdown'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {platform.capitalize()}: {count} videos")

        print("="*70)

    def prepare_audio_for_video(self, track_path: str, narration_path: str,
                                platform: str, output_path: str) -> str:
        """
        Prepare audio for video with platform-specific mixing
        Returns path to mixed audio file
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            print("[ERROR] pydub not installed. Install with: pip install pydub")
            print("[INFO] Returning original narration path")
            return narration_path

        if platform not in self.platform_configs:
            print(f"[WARNING] Unknown platform: {platform}. Using YouTube defaults.")
            platform = "youtube"

        config = self.platform_configs[platform]

        print(f"\n[MIXING] Preparing audio for {platform.upper()}")
        print(f"  Background Music: {Path(track_path).name}")
        print(f"  Narration: {Path(narration_path).name}")
        print(f"  Volume Reduction: {config['bg_music_volume_db']} dB")

        try:
            # Load audio files
            music = AudioSegment.from_mp3(track_path)
            narration = AudioSegment.from_file(narration_path)

            # Get duration
            narration_duration = len(narration)

            # Loop music if shorter than narration
            if len(music) < narration_duration:
                repeats = (narration_duration // len(music)) + 1
                music = music * repeats

            # Trim music to narration length
            music = music[:narration_duration]

            # Reduce music volume
            music = music + config['bg_music_volume_db']

            # Overlay narration on top of music
            mixed = music.overlay(narration)

            # Export
            mixed.export(output_path, format="mp3", bitrate="192k")

            print(f"[SUCCESS] Mixed audio saved: {output_path}")
            return output_path

        except Exception as e:
            print(f"[ERROR] Audio mixing failed: {e}")
            return narration_path

    def recommend_track(self, platform: str, duration: Optional[int] = None,
                       mood: Optional[str] = None, show_alternatives: bool = True) -> Optional[Dict]:
        """Get recommendation with explanation"""
        print(f"\n[SEARCHING] Best track for {platform.upper()}")
        if duration:
            print(f"  Duration target: {duration}s")
        if mood:
            print(f"  Mood preference: {mood}")

        track = self.get_music_for_platform(platform, duration, mood)

        if not track:
            print("[ERROR] No suitable tracks found")
            return None

        print(f"\n[RECOMMENDED]")
        print(f"  Title: {track['title']}")
        print(f"  Artist: {track['artist']}")
        print(f"  Mood: {track['mood']}")
        print(f"  BPM: {track['bpm']}")
        print(f"  Duration: {track['duration']:.1f}s")
        print(f"  Usage: {track['usage_count']} times")
        stars_filled = '*' * track['rating']
        stars_empty = '-' * (5 - track['rating'])
        print(f"  Rating: {stars_filled}{stars_empty} ({track['rating']}/5)")

        # Calculate and show score
        score = self._calculate_platform_score(track, platform)
        print(f"  Platform Match Score: {score:.1f}/100")

        if show_alternatives:
            # Show alternatives
            rotation = self.get_music_rotation(platform, 3, {"mood": mood} if mood else None)
            if len(rotation) > 1:
                print(f"\n[ALTERNATIVES]")
                for i, alt in enumerate(rotation[1:], 1):
                    alt_score = self._calculate_platform_score(alt, platform)
                    print(f"  {i}. {alt['title']} by {alt['artist']} (Score: {alt_score:.1f})")

        return track


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Music Library Manager for Epidemic Sound Tracks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan library and build index
  python music_library_manager.py --scan

  # Show library statistics
  python music_library_manager.py --stats

  # Search for tracks
  python music_library_manager.py --find "calm uplifting"

  # Get recommendation for platform
  python music_library_manager.py --recommend youtube --duration 300

  # Get recommendation with mood filter
  python music_library_manager.py --recommend tiktok --mood energetic

  # Get rotation of 5 tracks for YouTube series
  python music_library_manager.py --rotation youtube --count 5
        """
    )

    parser.add_argument('--music-dir', default='background_music',
                       help='Music directory path (default: background_music)')
    parser.add_argument('--metadata-file', default='music_library_metadata.json',
                       help='Metadata file path (default: music_library_metadata.json)')

    parser.add_argument('--scan', action='store_true',
                       help='Scan library and build/update index')
    parser.add_argument('--force-rescan', action='store_true',
                       help='Force rescan all tracks (updates metadata)')

    parser.add_argument('--stats', action='store_true',
                       help='Show library statistics')

    parser.add_argument('--find', type=str,
                       help='Search for tracks by query')

    parser.add_argument('--recommend', type=str, choices=['youtube', 'tiktok', 'instagram', 'podcast', 'shorts'],
                       help='Get track recommendation for platform')
    parser.add_argument('--duration', type=int,
                       help='Target duration in seconds')
    parser.add_argument('--mood', type=str,
                       help='Preferred mood (calm, uplifting, energetic, etc.)')

    parser.add_argument('--rotation', type=str, choices=['youtube', 'tiktok', 'instagram', 'podcast', 'shorts'],
                       help='Get track rotation for platform')
    parser.add_argument('--count', type=int, default=5,
                       help='Number of tracks in rotation (default: 5)')

    parser.add_argument('--list-platforms', action='store_true',
                       help='List all supported platforms and their configurations')

    args = parser.parse_args()

    # Initialize manager
    manager = MusicLibraryManager(
        music_dir=args.music_dir,
        metadata_file=args.metadata_file
    )

    # Execute commands
    if args.scan or args.force_rescan:
        manager.scan_library(force_rescan=args.force_rescan)

    if args.stats:
        manager.print_stats()

    if args.find:
        results = manager.search_tracks(args.find)
        print(f"\n[SEARCH] Found {len(results)} tracks matching '{args.find}'")
        for i, track in enumerate(results, 1):
            print(f"\n{i}. {track['title']} by {track['artist']}")
            print(f"   Mood: {track['mood']} | BPM: {track['bpm']} | Duration: {track['duration']:.1f}s")
            stars = '*' * track['rating']
            print(f"   Usage: {track['usage_count']} | Rating: {stars} ({track['rating']}/5)")

    if args.recommend:
        manager.recommend_track(args.recommend, args.duration, args.mood)

    if args.rotation:
        filters = {}
        if args.mood:
            filters['mood'] = args.mood

        rotation = manager.get_music_rotation(args.rotation, args.count, filters)
        print(f"\n[ROTATION] {len(rotation)} tracks for {args.rotation.upper()}")
        for i, track in enumerate(rotation, 1):
            score = manager._calculate_platform_score(track, args.rotation)
            print(f"\n{i}. {track['title']} by {track['artist']}")
            print(f"   Mood: {track['mood']} | BPM: {track['bpm']} | Score: {score:.1f}")
            print(f"   File: {track['filename']}")

    if args.list_platforms:
        print("\n" + "="*70)
        print("SUPPORTED PLATFORMS")
        print("="*70)
        for platform, config in manager.platform_configs.items():
            print(f"\n{platform.upper()}")
            print(f"  Background Music Volume: {config['bg_music_volume_percent']}% ({config['bg_music_volume_db']} dB)")
            print(f"  Optimal BPM: {config['optimal_bpm'][0]}-{config['optimal_bpm'][1]}")
            print(f"  Preferred Moods: {', '.join(config['preferred_moods'])}")
            print(f"  Energy Level: {config['max_energy']}")
        print("="*70)

    # If no arguments, show help
    if len(vars(args)) == 2:  # Only default args
        parser.print_help()


if __name__ == '__main__':
    main()
