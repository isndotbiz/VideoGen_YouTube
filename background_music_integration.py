#!/usr/bin/env python3
"""
Background Music Integration Module
Integrates optimal background music into video generation pipeline
"""

import os
from pathlib import Path
from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips
from optimal_clip_finder import OptimalClipFinder
import json

class BackgroundMusicIntegration:
    """
    Integrate optimal background music into video pipeline
    """

    def __init__(self, music_library_path="./cached_music"):
        """
        Initialize the integration module

        Args:
            music_library_path: Directory for caching processed music clips
        """
        self.music_library = music_library_path
        os.makedirs(music_library_path, exist_ok=True)

        # Initialize clip finder
        self.clip_finder = OptimalClipFinder(target_duration=82.0)

    def find_and_extract_best_clip(self, source_audio: str, target_duration: float,
                                   force_reanalyze=False):
        """
        Find and extract the best clip for given duration

        Args:
            source_audio: Path to long-form background music
            target_duration: Required duration in seconds
            force_reanalyze: If True, re-analyze even if cached clip exists

        Returns:
            clip_path: Path to extracted optimal clip
        """
        # Check for cached clip
        cache_key = f"{Path(source_audio).stem}_optimal_{int(target_duration)}s.mp3"
        cache_path = os.path.join(self.music_library, cache_key)

        if os.path.exists(cache_path) and not force_reanalyze:
            print(f"\n[CACHED] Using existing clip: {cache_path}")
            return cache_path

        print(f"\n[ANALYZING] Finding optimal {target_duration}s clip from {Path(source_audio).name}")

        # Update target duration
        self.clip_finder.target_duration = target_duration

        # Analyze
        analysis = self.clip_finder.analyze_audio(source_audio)

        # Find clips
        clips = self.clip_finder.find_optimal_clips(analysis, num_clips=1)

        if not clips:
            raise ValueError("No suitable clips found")

        # Extract best clip
        best_clip = clips[0]
        self.clip_finder.extract_clip(source_audio, best_clip['start'], cache_path)

        # Save analysis metadata
        metadata_path = os.path.join(
            self.music_library,
            f"{Path(source_audio).stem}_optimal_{int(target_duration)}s_metadata.json"
        )

        with open(metadata_path, 'w') as f:
            json.dump({
                'source': source_audio,
                'clip_start': best_clip['start'],
                'clip_duration': target_duration,
                'score': best_clip['score'],
                'score_breakdown': best_clip['score_breakdown']
            }, f, indent=2)

        return cache_path

    def mix_with_narration(self, narration_path: str, bg_music_path: str,
                          output_path: str, bg_volume=0.15, fade_duration=2.0):
        """
        Mix background music with narration

        Args:
            narration_path: Path to narration audio
            bg_music_path: Path to background music
            output_path: Output path for mixed audio
            bg_volume: Background music volume (0.0-1.0, default: 0.15)
            fade_duration: Duration of fade in/out in seconds (default: 2.0)

        Returns:
            output_path: Path to mixed audio
        """
        print(f"\n{'='*80}")
        print("MIXING AUDIO")
        print(f"{'='*80}")
        print(f"  Narration: {Path(narration_path).name}")
        print(f"  Background: {Path(bg_music_path).name}")
        print(f"  BG Volume: {bg_volume*100:.0f}%")
        print(f"  Fade duration: {fade_duration}s")

        # Load audio
        narration = AudioFileClip(narration_path)
        bg_music = AudioFileClip(bg_music_path)

        # Match duration
        if bg_music.duration < narration.duration:
            # Loop music if needed
            loops = int(narration.duration / bg_music.duration) + 1
            print(f"  Looping background music {loops} times")
            bg_music = concatenate_audioclips([bg_music] * loops)

        # Trim to exact duration
        bg_music = bg_music.subclip(0, narration.duration)

        # Apply volume
        bg_music = bg_music.volumex(bg_volume)

        # Apply fade in/out to background music
        if fade_duration > 0:
            bg_music = bg_music.audio_fadein(fade_duration).audio_fadeout(fade_duration)

        # Composite (background first, then narration on top)
        final = CompositeAudioClip([bg_music, narration])

        # Export with high quality
        print(f"  Exporting mixed audio...")
        final.write_audiofile(
            output_path,
            bitrate='192k',
            fps=44100,
            nbytes=2,
            codec='libmp3lame',
            verbose=False,
            logger=None
        )

        # Cleanup
        narration.close()
        bg_music.close()
        final.close()

        print(f"  Mixed audio saved: {output_path}")
        print(f"{'='*80}\n")

        return output_path

    def auto_process_for_video(self, narration_path: str,
                               source_music_path: str,
                               output_path: str,
                               bg_volume=0.15,
                               fade_duration=2.0):
        """
        Automatic processing: analyze, extract, and mix

        Args:
            narration_path: Path to narration
            source_music_path: Path to long-form background music
            output_path: Output path for final mixed audio
            bg_volume: Background volume (default: 0.15 = 15%)
            fade_duration: Fade in/out duration in seconds

        Returns:
            output_path: Path to final audio
        """
        print(f"\n{'='*80}")
        print("AUTO-PROCESSING BACKGROUND MUSIC")
        print(f"{'='*80}\n")

        # Get narration duration
        narration = AudioFileClip(narration_path)
        duration = narration.duration
        narration.close()

        print(f"Target duration: {duration:.2f}s")

        # Find and extract optimal clip
        clip_path = self.find_and_extract_best_clip(source_music_path, duration)

        # Mix with narration
        final_path = self.mix_with_narration(
            narration_path,
            clip_path,
            output_path,
            bg_volume=bg_volume,
            fade_duration=fade_duration
        )

        print(f"[SUCCESS] Final audio with background music: {final_path}")

        return final_path

    def analyze_music_library(self, music_directory: str):
        """
        Analyze all music files in a directory and cache analysis results

        Args:
            music_directory: Directory containing music files

        Returns:
            analysis_results: Dictionary of analysis results by file
        """
        print(f"\n{'='*80}")
        print(f"ANALYZING MUSIC LIBRARY: {music_directory}")
        print(f"{'='*80}\n")

        music_dir = Path(music_directory)
        if not music_dir.exists():
            print(f"Error: Directory not found: {music_directory}")
            return {}

        # Find all audio files
        audio_files = []
        for ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
            audio_files.extend(music_dir.glob(f"**/*{ext}"))

        print(f"Found {len(audio_files)} audio files\n")

        analysis_results = {}

        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n[{i}/{len(audio_files)}] Analyzing {audio_file.name}...")

            try:
                # Analyze
                analysis = self.clip_finder.analyze_audio(str(audio_file))

                # Save analysis
                analysis_file = os.path.join(
                    self.music_library,
                    f"{audio_file.stem}_full_analysis.json"
                )

                with open(analysis_file, 'w') as f:
                    json.dump(analysis, f, indent=2)

                analysis_results[str(audio_file)] = analysis

                print(f"  Analysis saved: {analysis_file}")

            except Exception as e:
                print(f"  Error analyzing {audio_file.name}: {e}")
                continue

        # Save summary
        summary_file = os.path.join(self.music_library, "library_analysis_summary.json")
        summary = {
            'total_files': len(audio_files),
            'analyzed': len(analysis_results),
            'files': {
                Path(k).name: {
                    'duration': v['duration'],
                    'tempo': v['tempo'],
                    'frequency_score': v['frequency_analysis']['conflict_score'],
                    'recommendation': v['frequency_analysis']['recommendation']
                }
                for k, v in analysis_results.items()
            }
        }

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n{'='*80}")
        print(f"LIBRARY ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"Analyzed: {len(analysis_results)}/{len(audio_files)} files")
        print(f"Summary saved: {summary_file}\n")

        return analysis_results

    def get_best_music_for_narration(self, music_directory: str, narration_path: str,
                                    num_recommendations=3):
        """
        Recommend best music tracks for a specific narration

        Args:
            music_directory: Directory containing music files
            narration_path: Path to narration file
            num_recommendations: Number of recommendations to return

        Returns:
            recommendations: List of recommended music files with scores
        """
        # Get narration duration
        narration = AudioFileClip(narration_path)
        duration = narration.duration
        narration.close()

        print(f"\nFinding best music for narration ({duration:.2f}s)...")

        # Check for cached library analysis
        summary_file = os.path.join(self.music_library, "library_analysis_summary.json")

        if not os.path.exists(summary_file):
            print("No cached analysis found. Analyzing music library...")
            self.analyze_music_library(music_directory)

        # Load summary
        with open(summary_file, 'r') as f:
            summary = json.load(f)

        # Score each track
        recommendations = []
        music_dir = Path(music_directory)

        for filename, info in summary['files'].items():
            # Find full path
            candidates = list(music_dir.glob(f"**/{filename}"))

            if not candidates:
                continue

            file_path = str(candidates[0])

            # Score based on:
            # 1. Duration (prefer longer than narration)
            # 2. Low speech frequency conflict
            # 3. Moderate tempo (80-140 BPM)

            duration_score = 100 if info['duration'] >= duration else 50
            frequency_score = 100 - info['frequency_score']
            tempo_score = 100 * (1 - min(abs(info['tempo'] - 110) / 50, 1.0))

            total_score = (
                duration_score * 0.4 +
                frequency_score * 0.4 +
                tempo_score * 0.2
            )

            recommendations.append({
                'file': filename,
                'path': file_path,
                'score': total_score,
                'duration': info['duration'],
                'tempo': info['tempo'],
                'frequency_conflict': info['frequency_score'],
                'recommendation': info['recommendation']
            })

        # Sort by score
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)

        # Print top recommendations
        print(f"\nTop {num_recommendations} recommendations:")
        for i, rec in enumerate(recommendations[:num_recommendations], 1):
            print(f"\n{i}. {rec['file']}")
            print(f"   Score: {rec['score']:.2f}")
            print(f"   Duration: {rec['duration']:.2f}s")
            print(f"   Tempo: {rec['tempo']:.2f} BPM")
            print(f"   Frequency conflict: {rec['frequency_conflict']:.2f}%")

        return recommendations[:num_recommendations]


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Integrate background music into video pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-process: analyze, extract, and mix
  python background_music_integration.py \\
    --narration narration.mp3 \\
    --music background_music.mp3 \\
    --output final_audio.mp3

  # Analyze entire music library
  python background_music_integration.py \\
    --analyze-library ./background_music

  # Get recommendations for specific narration
  python background_music_integration.py \\
    --recommend \\
    --narration narration.mp3 \\
    --music-library ./background_music
        """
    )

    parser.add_argument('--narration', help='Path to narration audio file')
    parser.add_argument('--music', help='Path to background music file')
    parser.add_argument('--output', help='Output path for mixed audio')
    parser.add_argument('--volume', type=float, default=0.15,
                       help='Background music volume (0.0-1.0, default: 0.15)')
    parser.add_argument('--fade', type=float, default=2.0,
                       help='Fade in/out duration in seconds (default: 2.0)')
    parser.add_argument('--analyze-library', help='Analyze all music in directory')
    parser.add_argument('--recommend', action='store_true',
                       help='Get music recommendations for narration')
    parser.add_argument('--music-library', help='Path to music library directory')
    parser.add_argument('--cache-dir', default='./cached_music',
                       help='Cache directory (default: ./cached_music)')

    args = parser.parse_args()

    # Initialize
    integrator = BackgroundMusicIntegration(music_library_path=args.cache_dir)

    # Analyze library mode
    if args.analyze_library:
        integrator.analyze_music_library(args.analyze_library)
        return

    # Recommendation mode
    if args.recommend:
        if not args.narration or not args.music_library:
            print("Error: --recommend requires --narration and --music-library")
            return

        integrator.get_best_music_for_narration(
            args.music_library,
            args.narration,
            num_recommendations=5
        )
        return

    # Auto-process mode
    if args.narration and args.music:
        if not args.output:
            args.output = f"{Path(args.narration).stem}_with_bgm.mp3"

        integrator.auto_process_for_video(
            narration_path=args.narration,
            source_music_path=args.music,
            output_path=args.output,
            bg_volume=args.volume,
            fade_duration=args.fade
        )
        return

    # No valid mode specified
    parser.print_help()


if __name__ == '__main__':
    main()
