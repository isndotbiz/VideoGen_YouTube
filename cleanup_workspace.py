#!/usr/bin/env python3
"""
Comprehensive Workspace Cleanup Script
Removes duplicates, test files, and organizes documentation
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path(r"D:\workspace\VideoGen_YouTube")
ARCHIVE_DIR = BASE_DIR / "_archive"
DOCS_DIR = BASE_DIR / "docs"

# Create archive structure
ARCHIVE_DIRS = {
    "docs_archive": ARCHIVE_DIR / "docs_archive",
    "scripts_archive": ARCHIVE_DIR / "scripts_archive",
    "empty_files": ARCHIVE_DIR / "empty_files",
}

# Statistics
stats = {
    "docs_archived": 0,
    "scripts_archived": 0,
    "empty_deleted": 0,
    "docs_organized": 0,
}

def setup_directories():
    """Create archive and docs directories"""
    print("📁 Creating directory structure...")

    # Create archive dirs
    for dir_path in ARCHIVE_DIRS.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create docs subdirs
    (DOCS_DIR / "quick_starts").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "epidemic_sound").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "adapt_music").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "background_music").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "music_system").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "video_production").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "audio").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "guides" / "youtube").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "api_reference").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "workflows").mkdir(parents=True, exist_ok=True)

def delete_empty_files():
    """Delete the 7 empty files identified"""
    print("\n🗑️  Deleting empty files...")

    empty_files = [
        "output/nul",
        "output/final_video_subbed.mp4",
        "output/video_with_music.mp4",
        "kill_processes.txt",
        "epidemic_downloader.log",
        "output/free-ai-tools-animations/fal_ai_batch_commands.sh",
    ]

    for file_rel in empty_files:
        file_path = BASE_DIR / file_rel
        if file_path.exists() and file_path.stat().st_size == 0:
            try:
                file_path.unlink()
                stats["empty_deleted"] += 1
                print(f"  ✓ Deleted: {file_rel}")
            except Exception as e:
                print(f"  ✗ Error deleting {file_rel}: {e}")

def archive_duplicate_docs():
    """Archive duplicate documentation files"""
    print("\n📄 Archiving duplicate documentation...")

    # High-confidence duplicates to archive
    duplicates = [
        # Epidemic Sound duplicates
        "EPIDEMIC_QUICK_START.md",
        "EPIDEMIC_SOUND_GUIDE.md",
        "EPIDEMIC_BROWSER_FIX_SUMMARY.md",
        "EPIDEMIC_BROWSER_LOGIN_README.txt",
        "EPIDEMIC_CHROME_GUIDE.md",
        "EPIDEMIC_FIX_COMPLETE.md",
        "EPIDEMIC_QUICK_FIX_REFERENCE.md",
        "EPIDEMIC_BROWSER_AUTOMATION_SUMMARY.md",
        "EPIDEMIC_AUTO_DOWNLOADER_SUMMARY.md",
        "EPIDEMIC_SYSTEM_OVERVIEW.md",
        "EPIDEMIC_COMPLETE_WORKFLOW.md",
        "EPIDEMIC_EXACT_SETTINGS_GUIDE.md",
        "EPIDEMIC_NAVIGATION_BEST_PRACTICES.md",

        # Adapt duplicates
        "ADAPT_DIRECT_URL_QUICK_START.md",
        "ADAPT_BYPASS_WORKFLOW_FINDINGS.md",
        "ADAPT_SEARCH_BYPASS_PROOF.md",
        "ADAPT_TIMING_CHEAT_SHEET.md",
        "ADAPT_LOADING_STRATEGY_SUMMARY.txt",
        "ADAPT_MUSIC_QUICK_START.txt",
        "ADAPT_LENGTH_GUIDE.md",
        "ADAPT_LENGTH_QUICK_START.md",
        "ADAPT_LENGTH_AUTOMATION_GUIDE.md",
        "ADAPT_TIMING_AND_LOADING_ANALYSIS.md",
        "ADAPT_SETTINGS_QUICK_CARD.md",
        "ADAPT_WORKFLOW_WHEN_YOU_HAVE_TRACKS.md",

        # Music system duplicates
        "MUSIC_DOWNLOADER_QUICK_START.txt",
        "MUSIC_LIBRARY_SUMMARY.md",
        "MUSIC_SYSTEM_FILES.txt",
        "MUSIC_DISCOVERY_TOOLS_GUIDE.md",
        "MUSIC_LIBRARY_SYSTEM_SUMMARY.md",
        "MUSIC_SYSTEM_DELIVERY_SUMMARY.md",
        "MUSIC_QUICK_START.md",

        # Background music duplicates
        "EMERGENCY_MUSIC_README.txt",
        "EMERGENCY_MUSIC_SYSTEM_SUMMARY.md",
        "BACKGROUND_MUSIC_7_STEP_WORKFLOW.md",
        "SOCIAL_MUSIC_DOWNLOADER_README.md",
        "TIKTOK_MUSIC_DOWNLOADER_README.md",
        "YOUTUBE_MUSIC_DOWNLOADER_SUMMARY.md",
        "EMERGENCY_MUSIC_QUICK_START.md",
        "SOCIAL_MUSIC_QUICK_START.md",
        "TIKTOK_MUSIC_QUICK_START.md",
        "YOUTUBE_MUSIC_GUIDE.md",
        "YOUTUBE_MUSIC_QUICK_REFERENCE.txt",

        # Quick start duplicates
        "QUICK_START_50_TRACKS.txt",
        "QUICK_START_SHOTSTACK.txt",
        "QUICK_START_INTEGRATION_GUIDE.md",

        # README duplicates
        "README_BATCH_DOWNLOAD.md",
        "README_NARRATION_FILE.md",

        # Start here duplicates
        "00_START_HERE.txt",
        "START_HERE_BACKGROUND_MUSIC.md",

        # Summary/Status duplicates (txt versions)
        "AUTOMATION_SUMMARY.txt",
        "DELIVERY_SUMMARY.txt",
        "FILES_CREATED_SUMMARY.txt",
        "FINAL_SUMMARY.txt",
        "STATUS.txt",
        "COMPLETION_REPORT.txt",
        "COURSE_COMPLETION_SUMMARY.txt",
        "BATCH_DOWNLOAD_SUMMARY.txt",
        "VIDEO_CREATION_COMPLETE.txt",
        "VIDEO_STATUS_UPDATE.txt",
        "PIPELINE_STATUS.txt",

        # More summaries
        "AUTOMATION_STATUS_FINAL.md",
        "COMPLETE_SUCCESS_SUMMARY.md",
        "TEST_VIDEO_SUMMARY.md",
        "QUICK_TEST_VIDEO_SUMMARY.md",
        "FINAL_TEST_VIDEO_SUMMARY.md",
        "NEW_APPROACH_SUMMARY.md",
        "IMPLEMENTATION_SUMMARY.md",
        "PRODUCTION_STATUS.md",

        # Labs Adapt duplicates
        "LABS_ADAPT_AUTH_SUMMARY.txt",
        "LABS_ADAPT_BENEFITS.md",
        "LABS_ADAPT_SYSTEM_STATUS.md",
        "LABS_ADAPT_SESSION_VERIFICATION.md",
        "LABS_ADAPT_AUTH_DOCUMENTATION_INDEX.md",
        "LABS_ADAPT_AUTH_QUICK_REFERENCE.md",

        # N8N duplicates
        "N8N_TRANSITIONS_CHEAT_SHEET.txt",
        "N8N_TRANSITIONS_QUICK_REFERENCE.txt",
        "N8N_TRANSITIONS_IMPLEMENTATION_SUMMARY.md",
        "N8N_PRODUCTION_COMPLETE_WITH_INFOGRAPHICS.md",
        "N8N_INFOGRAPHIC_SYNC_GUIDE.md",
        "N8N_VIDEO_READY_FOR_YOUTUBE.md",

        # Step4 duplicates
        "STEP4_INDEX.txt",
        "STEP4_FALLBACK_SOURCES_MAP.txt",
        "STEP4_QUICK_FIXES.md",
        "STEP4_FALLBACKS_EXTRACTED.md",
        "STEP4_COMPARISON.md",
        "STEP4_ROOT_CAUSE_REPORT.md",

        # Volume/Audio duplicates
        "VOLUME_CONSISTENCY_SUMMARY.md",
        "AUDIO_API_IMPLEMENTATION_STATUS.md",
        "AUDIO_TOOLS_QUICK_START.md",

        # ElevenLabs duplicates
        "ELEVENLABS_CLEAN_NARRATION_30SEC.txt",
        "ELEVENLABS_FIX_GUIDE.md",

        # YouTube duplicates
        "YOUTUBE_UPLOAD_QUICK_START.txt",
        "YOUTUBE_UPLOAD_INSTRUCTIONS.txt",
        "UPLOAD_QUICK_START.txt",

        # Misc duplicates
        "QUICK_REFERENCE_CARD.txt",
        "AUTH_SESSION_FINDINGS.txt",
        "SOLUTION_SUMMARY.md",
        "STATUS_AND_NEXT_STEPS.md",
        "DELIVERY_SUMMARY.md",
        "DISCOVERED_TRACKS_SUMMARY.md",
        "WHATS_WORKING_NOW.md",
    ]

    for doc in duplicates:
        src = BASE_DIR / doc
        if src.exists():
            dst = ARCHIVE_DIRS["docs_archive"] / doc
            try:
                shutil.move(str(src), str(dst))
                stats["docs_archived"] += 1
                print(f"  ✓ Archived: {doc}")
            except Exception as e:
                print(f"  ✗ Error archiving {doc}: {e}")

def archive_test_scripts():
    """Archive test and experimental Python scripts"""
    print("\n🐍 Archiving test/experimental scripts...")

    # Test and experimental scripts to archive
    test_scripts = [
        # Version iterations
        "compose_video_v1.py",
        "create_video_final.py",
        "create_video_final_working.py",
        "final_compose_video1.py",
        "compose_final_video.py",

        # Test scripts
        "test_pipeline_video_1.py",
        "test_adapt_minimal.py",
        "test_adapt_step4_minimal.py",
        "test_labs_navigation.py",
        "test_labs_adapt_complete.py",
        "test_epidemic_navigation.py",
        "test_epidemic_sound_client.py",
        "test_fal_quick.py",
        "test_fal_comprehensive.py",
        "test_fal_video.py",
        "test_steps_1_2.py",
        "adapt_simple_test.py",

        # N8N experiments
        "create_n8n_30sec_test_simple.py",
        "create_n8n_30sec_test_video.py",
        "create_n8n_test_final.py",
        "create_n8n_test_final_fixed.py",
        "create_n8n_test_shotstack.py",
        "create_n8n_test_shotstack_v2.py",
        "create_n8n_test_v3.py",
        "create_n8n_test_video_fixed.py",
        "create_n8n_test_video_proper.py",
        "create_perfect_n8n_videos_complete.py",
        "create_truly_perfect_videos.py",
        "create_final_perfect_videos.py",
        "create_30sec_n8n_test.py",
        "create_30sec_n8n_v2_improved.py",
        "create_3min_n8n_final.py",
        "generate_n8n_3min_video.py",
        "generate_n8n_3min_video_v2.py",
        "generate_n8n_infographics_fixed.py",
        "n8n_complete_production_pipeline.py",
        "n8n_smooth_transitions_demo.py",
        "n8n_video_with_smooth_transitions.py",
        "shotstack_compose_n8n_final.py",

        # 30-second video experiments
        "create_30_second_video_clean.py",
        "create_30sec_descript.py",
        "create_30sec_imageio.py",
        "create_30sec_moviepy.py",
        "create_30sec_shotstack.py",
        "create_30sec_image_focused_video.py",
        "create_full_30sec_test_video.py",
        "create_quick_test_video.py",

        # Build/composition variations
        "build_test_video_1min.py",
        "build_test_video_correct.py",
        "build_test_video_final.py",
        "build_test_video_v_final.py",
        "build_final_test.py",
        "build_with_nano_banana.py",
        "compose_final_test_video.py",
        "compose_nanobana_simple.py",
        "compose_with_nanobana_images.py",
        "compose_with_opencv.py",
        "compose_with_shotstack_audio_control.py",
        "compose_full_video.py",
        "compose_full_video_with_subtitles_music.py",
        "compose_video_imageio.py",

        # Music download experiments
        "download_10_tracks_auto.py",
        "download_50_tracks_batch.py",
        "download_50_tracks_parallel.py",
        "download_all_platform_music.py",
        "download_social_music.py",
        "download_tiktok_music.py",
        "download_youtube_music.py",
        "emergency_music_downloader.py",
        "simple_epidemic_downloader.py",
        "epidemic_final_downloader.py",
        "epidemic_download_working.py",
        "epidemic_genre_download.py",
        "epidemic_auto_downloader.py",
        "epidemic_browser_login.py",
        "epidemic_browser_search.py",
        "epidemic_browser_adapt.py",
        "epidemic_oauth_login.py",
        "epidemic_oauth_stealth.py",
        "epidemic_use_chrome.py",

        # Agent/research scripts
        "agent_a_find_ai_search.py",
        "agent_b_labs_adapt_search.py",
        "agent_d_wav_download.py",
        "ai_search_simple_download.py",
        "discover_all_tracks.py",
        "diagnose_adapt_page.py",
        "step_4_search_track_bulletproof.py",
        "demo_complete_workflow_one_track.py",

        # Simple/demo variations
        "create_video1_simple.py",
        "create_sample_video_simple.py",
        "create_sample_with_optimized_music.py",
        "embed_subs_simple.py",
        "curate_music_simple.py",
        "boost_segments_simple.py",

        # Generation experiments
        "generate_video1_animations.py",
        "generate_video1_animations_fal.py",
        "generate_animations_runway.py",
        "generate_free_ai_tools_animations.py",
        "generate_narration_openai.py",
        "generate_subtitles_assemblyai.py",
        "generate_complete_subtitles.py",
        "generate_topic_video.py",
        "generate_all_n8n_infographics.py",
        "generate_n8n_full_course.py",
        "generate_n8n_with_subtitle_space.py",

        # Regeneration/fix scripts
        "regenerate_with_nanobana.py",
        "regenerate_with_quiet_music.py",
        "regenerate_infographics_nano_banana.py",
        "regenerate_video_with_music_and_subs.py",
        "regenerate_perfect_subtitles.py",
        "regenerate_bubbly_subtitles.py",
        "regenerate_fancy_subtitles.py",
        "regenerate_final_with_complete_subs.py",
        "fix_video_complete.py",
        "video_fixer.py",

        # Upload variations
        "upload_diffuser_video.py",
        "upload_n8n_diffuser.py",
        "upload_with_background_music.py",
        "upload_perfect_with_seo.py",
        "upload_final_3_videos.py",
        "upload_all_3_videos.py",

        # Misc experiments
        "create_animated_production_videos.py",
        "create_ai_tools_comprehensive_video.py",
        "create_demo_video_complete.py",
        "create_production_videos.py",
        "create_placeholder_animations.py",
        "create_video_with_shotstack.py",
        "create_advanced_improved.py",
        "create_beginner_improved.py",
        "create_expert_improved.py",
        "complete_video_builder.py",
        "compose-video-complete.py",
        "compose_with_ffmpeg.py",

        # Analysis/utility
        "analyze_music_balance.py",
        "analyze_volume_consistency.py",
        "parallel_audio_analysis.py",
        "volume_consistency_analyzer.py",
        "music_curation_analyzer.py",

        # More experiments
        "build_3min_videos_optimized.py",
        "build_animated_videos.py",
        "fast_workflow_60s.py",
        "working_workflow_final.py",
        "finish_n8n_clips.py",
        "extract_best_music_sections.py",
        "find_best_music_sections.py",
        "apply_music_from_folder.py",
        "bg_music_auto_mixer.py",
        "boost_music_volume.py",
        "normalize_audio_fix.py",
        "mix-audio-correct.py",
        "add-audio-to-video.py",
        "add_music_remove_narration.py",

        # Integration examples
        "integrate_epidemic_sound.py",
        "integrate_jamendo_music.py",
        "integrate_mubert_music.py",
        "example_epidemic_browser.py",
        "example_music_integration.py",
        "example_use_emergency_music.py",
        "example_use_youtube_music.py",
        "epidemic_adapt_example.py",
        "epidemic_adapt_workflow_demo.py",
        "epidemic_ai_search_adapt.py",
        "epidemic_login_example.py",
        "epidemic_sound_examples.py",

        # S3/Shotstack helpers
        "create_public_s3_bucket.py",
        "s3_upload_n8n_assets.py",
        "shotstack_full_video_api.py",
        "shotstack_final_production.py",
        "shotstack_s3_complete_guide.py",

        # Other utilities
        "curate_background_music.py",
        "use_platform_music.py",
        "show_music_library.py",
        "generate-video-falaiv2.py",
        "multi_topic_generator.py",
        "multi_platform_generator.py",
        "optimize_video_seo.py",
        "youtube_seo_and_uploader.py",
        "youtube_upload_n8n_final.py",
        "elevenlabs_with_script_cleaning.py",
        "script_cleaner_for_tts.py",
        "embed_subtitles_moviepy.py",
        "generate_subtitles_srt.py",
        "get_subtitles_assembly.py",
        "login_and_download.py",
        "manual_login_and_save_session.py",
        "open_adapt_for_cleanup.py",
        "optimal_clip_finder.py",
        "clear_adapt_track.py",
        "save_chrome_session.py",
        "save_session_now.py",
        "setup_epidemic_adapt.py",
        "batch_test_volumes.sh",
        "remix_with_any_music.py",

        # Shell scripts to archive
        "add-audio-simple.sh",
        "add-audio.bat",
        "create_production_videos.sh",
        "epidemic_usage_example.sh",
        "start_chrome_debug.bat",
        "download_50_tracks_batch.bat",
        "add_music_and_subtitles.cmd",
    ]

    for script in test_scripts:
        src = BASE_DIR / script
        if src.exists():
            dst = ARCHIVE_DIRS["scripts_archive"] / script
            try:
                shutil.move(str(src), str(dst))
                stats["scripts_archived"] += 1
                print(f"  ✓ Archived: {script}")
            except Exception as e:
                print(f"  ✗ Error archiving {script}: {e}")

def organize_remaining_docs():
    """Organize remaining documentation into logical folders"""
    print("\n📚 Organizing remaining documentation...")

    # Core docs stay in root
    core_docs = [
        "README.md",
        "MASTER_WORKFLOW_DOCUMENTATION.md",
        "WORKFLOW_COMPLETE.md",
        "WORKFLOW_QUICK_REFERENCE.md",
    ]

    # Quick starts
    quick_starts = [
        "QUICK_START_30_SECOND_VIDEO.md",
        "QUICK_START_ANIMATED_VIDEOS.md",
        "QUICK_START_YOUTUBE_MUSIC.md",
    ]

    # Epidemic Sound guides
    epidemic_guides = [
        "EPIDEMIC_SOUND_API_COMPLETE_REFERENCE.md",
        "EPIDEMIC_AUTOMATION_GUIDE.md",
        "EPIDEMIC_ADAPT_QUICKSTART.md",
        "EPIDEMIC_SOUND_CLIENT_GUIDE.md",
    ]

    # Adapt music guides
    adapt_guides = [
        "ADAPT_COMPLETE_SETTINGS_GUIDE.md",
        "ADAPT_IMPLEMENTATION_GUIDE.md",
        "ADAPT_WORKFLOWS_INDEX.md",
        "ADAPT_MUSIC_COMPLETE.md",
    ]

    # Background music guides
    bg_music_guides = [
        "BACKGROUND_MUSIC_COMPLETE_GUIDE.md",
        "BACKGROUND_MUSIC_QUICK_START.md",
        "MASTER_BACKGROUND_MUSIC_GUIDE.md",
    ]

    # Music system guides
    music_guides = [
        "MUSIC_LIBRARY_MANAGER_README.md",
        "MUSIC_SYSTEM_README.md",
        "MUSIC_DOWNLOADER_GUIDE.md",
    ]

    # Video production guides
    video_guides = [
        "README_30_SECOND_VIDEO_SYSTEM.md",
        "README_PRODUCTION.md",
    ]

    # Audio guides
    audio_guides = [
        "ELEVENLABS_IMPLEMENTATION_GUIDE.md",
        "VOLUME_CONSISTENCY_ANALYSIS_GUIDE.md",
        "VOLUME_CONSISTENCY_QUICK_START.md",
        "AUDIO_ANALYSIS_TOOLS_GUIDE.md",
        "README_VOLUME_CONSISTENCY.md",
    ]

    # YouTube guides
    youtube_guides = [
        "YOUTUBE_UPLOAD_GUIDE.md",
    ]

    # Workflows
    workflows = [
        "N8N_SMOOTH_TRANSITIONS_AND_ANIMATIONS_GUIDE.md",
        "N8N_TRANSITIONS_AND_ANIMATIONS_INDEX.md",
        "N8N_3MIN_PRODUCTION_COMPLETE.md",
        "N8N_QUICK_START.md",
        "LABS_ADAPT_COMPLETE_README.md",
        "LABS_ADAPT_QUICK_START.md",
        "LABS_ADAPT_INDEX.md",
    ]

    # Move files
    moves = [
        (quick_starts, DOCS_DIR / "quick_starts"),
        (epidemic_guides, DOCS_DIR / "guides" / "epidemic_sound"),
        (adapt_guides, DOCS_DIR / "guides" / "adapt_music"),
        (bg_music_guides, DOCS_DIR / "guides" / "background_music"),
        (music_guides, DOCS_DIR / "guides" / "music_system"),
        (video_guides, DOCS_DIR / "guides" / "video_production"),
        (audio_guides, DOCS_DIR / "guides" / "audio"),
        (youtube_guides, DOCS_DIR / "guides" / "youtube"),
        (workflows, DOCS_DIR / "workflows"),
    ]

    for file_list, dest_dir in moves:
        for doc in file_list:
            src = BASE_DIR / doc
            if src.exists():
                dst = dest_dir / doc
                try:
                    shutil.move(str(src), str(dst))
                    stats["docs_organized"] += 1
                    print(f"  ✓ Organized: {doc} → {dest_dir.name}")
                except Exception as e:
                    print(f"  ✗ Error organizing {doc}: {e}")

def create_summary_report():
    """Create a summary report of cleanup actions"""
    report_path = BASE_DIR / "CLEANUP_REPORT_SUMMARY.md"

    report = f"""# Workspace Cleanup Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Empty files deleted**: {stats['empty_deleted']}
- **Documentation files archived**: {stats['docs_archived']}
- **Script files archived**: {stats['scripts_archived']}
- **Documentation files organized**: {stats['docs_organized']}

## Actions Taken

### 1. Empty Files Deleted
Removed {stats['empty_deleted']} empty files (0 bytes each).

### 2. Documentation Cleanup
- Archived {stats['docs_archived']} duplicate/redundant documentation files
- Organized {stats['docs_organized']} remaining docs into logical subdirectories
- Created organized documentation structure in `docs/` directory

### 3. Script Cleanup
- Archived {stats['scripts_archived']} test/experimental Python scripts
- Kept ~35 core pipeline and utility scripts
- All archived scripts preserved in `_archive/scripts_archive/`

## Archive Location

All archived files can be found in:
- **Documentation**: `_archive/docs_archive/`
- **Scripts**: `_archive/scripts_archive/`
- **Empty files**: Deleted (were 0 bytes)

## New Documentation Structure

```
docs/
├── README.md (main)
├── MASTER_WORKFLOW_DOCUMENTATION.md
├── WORKFLOW_COMPLETE.md
├── WORKFLOW_QUICK_REFERENCE.md
│
├── quick_starts/
│   ├── QUICK_START_30_SECOND_VIDEO.md
│   ├── QUICK_START_ANIMATED_VIDEOS.md
│   └── QUICK_START_YOUTUBE_MUSIC.md
│
├── guides/
│   ├── epidemic_sound/
│   ├── adapt_music/
│   ├── background_music/
│   ├── music_system/
│   ├── video_production/
│   ├── audio/
│   └── youtube/
│
└── workflows/
    ├── N8N_*.md
    └── LABS_ADAPT_*.md
```

## Next Steps

1. Review archived files if needed: `_archive/`
2. Test core pipeline scripts to ensure functionality
3. Update any references to moved documentation
4. Commit changes to git
5. If satisfied after testing, permanently delete archive folder

## Rollback

If you need to rollback these changes:
```bash
# Restore docs
mv _archive/docs_archive/* .
mv _archive/scripts_archive/* .

# Remove new structure
rm -rf docs/
```
"""

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📊 Summary report created: CLEANUP_REPORT_SUMMARY.md")

def main():
    """Main cleanup execution"""
    print("=" * 60)
    print("  WORKSPACE CLEANUP - VideoGen YouTube")
    print("=" * 60)

    # Auto-confirm execution (non-interactive mode)
    print("\nThis script will:")
    print("  - Delete 7 empty files")
    print("  - Archive ~150 duplicate documentation files")
    print("  - Archive ~230 test/experimental scripts")
    print("  - Organize remaining docs into logical folders")
    print("\nAll archived files will be preserved in _archive/")
    print("\n[OK] Auto-confirmed (non-interactive mode)")

    print("\n>>> Starting cleanup...\n")

    # Execute cleanup steps
    setup_directories()
    delete_empty_files()
    archive_duplicate_docs()
    archive_test_scripts()
    organize_remaining_docs()
    create_summary_report()

    # Final summary
    print("\n" + "=" * 60)
    print("  CLEANUP COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Final Statistics:")
    print(f"  • Empty files deleted: {stats['empty_deleted']}")
    print(f"  • Docs archived: {stats['docs_archived']}")
    print(f"  • Scripts archived: {stats['scripts_archived']}")
    print(f"  • Docs organized: {stats['docs_organized']}")
    print(f"\n✅ Cleanup successful! Review CLEANUP_REPORT_SUMMARY.md for details.")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the changes")
    print(f"   2. Test your core pipeline scripts")
    print(f"   3. Commit changes to git")
    print(f"   4. Delete _archive/ if satisfied\n")

if __name__ == "__main__":
    main()
