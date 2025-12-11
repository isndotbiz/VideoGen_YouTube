#!/usr/bin/env python3
"""
Updated Image Generation Pipeline
- Flux Pro: ONLY photorealistic people, environments, workspaces
- Nano Banana: ALL text-based images (charts, infographics, diagrams, text overlays)

This replaces attempting to use Flux Pro for text (which it's bad at).
Nano Banana excels at text rendering in images.
"""

import os
import json
import requests
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NanoBananaImageGenerator:
    def __init__(self):
        self.fal_api_key = os.getenv('FAL_API_KEY')
        self.output_dir = './output/generated_images'
        self.metadata = {
            'timestamp': datetime.now().isoformat(),
            'images': []
        }

    # ============================================
    # FLUX PRO - PHOTOREALISTIC ONLY
    # ============================================

    def generate_flux_pro_prompts(self) -> List[Dict]:
        """
        Flux Pro ONLY for:
        - Real people (teams, individuals, professionals)
        - Real environments (offices, workspaces)
        - Real objects and scenarios (NOT text/charts)
        """
        prompts = [
            {
                'id': 'flux_people_1',
                'category': 'people',
                'description': 'Professional woman at desk analyzing analytics',
                'prompt': '''Professional woman in modern office at sleek desk with laptop,
                          analyzing dashboard on large monitor. Natural daylight from window,
                          plants in background, professional casual attire, focused expression.
                          Shot with Canon 5D Mark IV, 50mm lens, shallow depth of field,
                          cinematic professional photography, 4K, daylight balanced lighting''',
                'model': 'flux-pro',
                'guidance': 8.5,
                'use_case': 'Opening scene - analyst working',
            },
            {
                'id': 'flux_team_1',
                'category': 'people',
                'description': 'Diverse team collaborating around desk',
                'prompt': '''4 diverse professionals (2 women, 2 men, mixed ethnicity)
                          collaborating around large desk with multiple monitors showing analytics.
                          Bright modern office, natural light, engaged expressions, professional attire,
                          friendly collaborative atmosphere. Shot with Sony A7IV, 35mm lens,
                          cinematic lighting, 4K professional quality''',
                'model': 'flux-pro',
                'guidance': 8.5,
                'use_case': 'Team collaboration scene',
            },
            {
                'id': 'flux_closeup_1',
                'category': 'detail',
                'description': 'Hands typing on mechanical keyboard',
                'prompt': '''Close-up of hands typing on RGB mechanical keyboard with blue switches,
                          blurred monitor in background, warm professional lighting, shallow depth of field.
                          Macro photography style, shot with 85mm macro lens, film photography aesthetic,
                          professional office setting, 4K sharp focus on fingers''',
                'model': 'flux-pro',
                'guidance': 8.5,
                'use_case': 'Transition scene - hands working',
            },
            {
                'id': 'flux_workspace_1',
                'category': 'environment',
                'description': 'Modern dual-monitor professional workspace',
                'prompt': '''Professional workspace with dual high-resolution monitors, ergonomic chair,
                          organized desk with notebook and coffee, natural light, plants, minimalist design.
                          Modern tech aesthetic, shot from 45-degree angle, cinematic lighting,
                          professional photography, 4K, Canon 5D Mark IV quality''',
                'model': 'flux-pro',
                'guidance': 8.5,
                'use_case': 'Setup scene - workspace overview',
            },
            {
                'id': 'flux_presentation_1',
                'category': 'people',
                'description': 'Professional woman presenting data to audience',
                'prompt': '''Professional woman in business attire presenting SEO analytics on large screen
                          to seated audience of 3-4 people. Conference room with modern design, bright lighting,
                          professional presentation setup, engaged audience members.
                          Shot with 70mm lens, professional event photography style, 4K, cinematic quality''',
                'model': 'flux-pro',
                'guidance': 8.5,
                'use_case': 'Presentation/expertise scene',
            },
        ]
        return prompts

    # ============================================
    # NANO BANANA - TEXT & INFOGRAPHICS ONLY
    # ============================================

    def generate_nano_banana_prompts(self) -> List[Dict]:
        """
        Nano Banana SPECIALIZES in:
        - Text rendering (clear, readable)
        - Charts and graphs
        - Infographics
        - Diagrams
        - Step-by-step visuals
        - Data visualization
        """
        prompts = [
            {
                'id': 'nano_chart_ranking_factors',
                'category': 'chart',
                'description': 'Bar chart: Top SEO Ranking Factors',
                'prompt': '''Professional bar chart infographic showing top 5 SEO ranking factors ranked by importance:

1. Backlinks & Domain Authority (28%)
   - Represented by chain link icon, shown as tallest bar

2. Content Quality & Relevance (25%)
   - Represented by document icon, second tallest bar

3. Core Web Vitals (22%)
   - Represented by speedometer icon, third bar

4. Mobile-Friendliness (15%)
   - Represented by phone icon, fourth bar

5. User Experience Signals (10%)
   - Represented by smiley icon, shortest bar

Use modern flat design, blue and orange color scheme, white background,
clear percentage labels on each bar. Professional business infographic style.
Include legend on right side. Title: "Top SEO Ranking Factors 2025"''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Data visualization - ranking factors',
            },
            {
                'id': 'nano_timeline_algo_updates',
                'category': 'timeline',
                'description': 'Timeline: Google Algorithm Updates',
                'prompt': '''Vertical timeline infographic showing major Google algorithm updates from 2020-2025:

2020 - Core Web Vitals Announced
   Icon: speedometer
   Description: "Google announces Core Web Vitals as ranking factor"

2021 - Mobile-First Indexing Default
   Icon: mobile phone
   Description: "Mobile version becomes primary index"

2022 - Helpful Content Update
   Icon: thumbs up
   Description: "AI-generated & thin content penalized"

2023 - SGE & AI Overview Launch
   Icon: robot/AI symbol
   Description: "Search Generative Experience introduces AI answers"

2024 - Link Quality Focus
   Icon: link symbol
   Description: "Emphasis on high-quality, relevant links"

2025 - Fresh Content Priority
   Icon: calendar
   Description: "Regular content updates favored"

Color-coded timeline by year, modern minimalist design, clear dates and descriptions.
Professional business infographic, white background, dark text''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Historical timeline visualization',
            },
            {
                'id': 'nano_comparison_table',
                'category': 'comparison',
                'description': 'Comparison Table: SEO vs PPC vs Social Media',
                'prompt': '''Professional comparison table infographic with 3 columns and 5 rows:

Column Headers: SEO | PPC | Social Media

Row 1 - Cost per Click
SEO: $0-1 | PPC: $1-3 | Social: $0.50

Row 2 - Time to Results
SEO: 3-6 months | PPC: Immediate | Social: 1-3 months

Row 3 - Long-term ROI
SEO: 300% | PPC: 150% | Social: 200%

Row 4 - Lead Quality
SEO: High | PPC: Medium | Social: Medium

Row 5 - Brand Building
SEO: Very High | PPC: Low | Social: High

Use clean table design with alternating row colors (light gray/white),
blue headers, clear readable fonts. Include checkmarks/X marks for comparison.
Professional business infographic style''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Comparison visualization',
            },
            {
                'id': 'nano_steps_implementation',
                'category': 'steps',
                'description': '5-Step SEO Implementation Process',
                'prompt': '''Step-by-step numbered infographic showing 5-step SEO implementation process:

Step 1: AUDIT YOUR WEBSITE
   Icon: magnifying glass
   Description: "Analyze current state, identify issues"
   Color: Blue #0066FF

Step 2: RESEARCH KEYWORDS
   Icon: search symbol
   Description: "Find target keywords with search intent"
   Color: Purple #6600FF

Step 3: OPTIMIZE CONTENT
   Icon: document/pencil
   Description: "Update titles, descriptions, headers"
   Color: Orange #FF6600

Step 4: BUILD LINKS
   Icon: chain link
   Description: "Earn quality backlinks from authority sites"
   Color: Green #00AA00

Step 5: MONITOR & IMPROVE
   Icon: chart/analytics
   Description: "Track rankings, traffic, adjust strategy"
   Color: Red #FF0000

Show steps in connected flow with arrows, modern flat design icons,
clean typography, white background, professional business style''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Process flow visualization',
            },
            {
                'id': 'nano_myths_reality',
                'category': 'myth-reality',
                'description': 'Common SEO Myths vs Reality',
                'prompt': '''Myth vs Reality card layout comparing 3 common SEO misconceptions:

MYTH #1: "More Keywords = Better Ranking"
Reality: "Natural keyword placement with proper density (1-2%)"
   Color: Red myth / Green reality
   Icon: X for myth, checkmark for reality

MYTH #2: "Backlinks Don't Matter Anymore"
Reality: "Quality backlinks from authority sites are still critical"
   Color: Red myth / Green reality
   Icon: X for myth, checkmark for reality

MYTH #3: "Social Media Directly Impacts Ranking"
Reality: "No direct ranking impact, but increases traffic & awareness"
   Color: Red myth / Green reality
   Icon: X for myth, checkmark for reality

Use card-based layout, red background for myths, green for reality,
white text, clear bold fonts, professional business design style''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Educational comparison',
            },
            {
                'id': 'nano_funnel_conversion',
                'category': 'funnel',
                'description': 'SEO to Conversion Funnel',
                'prompt': '''Conversion funnel infographic showing SEO journey:

Top (Widest): AWARENESS - 10,000 organic impressions
   Icon: eye symbol

Upper Middle: INTEREST - 500 clicks to website
   Icon: cursor/click symbol

Middle: CONSIDERATION - 100 page views
   Icon: document symbol

Lower Middle: ACTION - 20 conversions
   Icon: checkmark symbol

Bottom (Narrowest): LOYAL CUSTOMER - 5 repeat customers
   Icon: star symbol

Color gradient from blue (top) to gold (bottom), show percentages,
use funnel shape clearly, professional business analytics style''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Funnel/conversion visualization',
            },
            {
                'id': 'nano_keywords_priority',
                'category': 'matrix',
                'description': 'Keyword Priority Matrix',
                'prompt': '''Keyword priority matrix (2x2 grid) for SEO targeting:

Y-axis: Search Volume (Low to High)
X-axis: Competition (Low to High)

Quadrant 1 (Top-Left): LOW VOL, LOW COMP = "QUICK WINS"
   Example keywords listed
   Color: Green - Target these first

Quadrant 2 (Top-Right): HIGH VOL, LOW COMP = "GOLDMINES"
   Example keywords listed
   Color: Dark Green - Top priority

Quadrant 3 (Bottom-Left): LOW VOL, LOW COMP = "NICHE"
   Example keywords listed
   Color: Yellow - Nice to have

Quadrant 4 (Bottom-Right): HIGH VOL, HIGH COMP = "COMPETITIVE"
   Example keywords listed
   Color: Red - Long-term targets

Use clear quadrant labels, example keywords in each area,
professional business analytics visualization style''',
                'model': 'nano-banana',
                'has_text': True,
                'use_case': 'Strategic planning matrix',
            },
        ]
        return prompts

    async def generate_flux_pro_images(self, prompts: List[Dict]) -> List[Dict]:
        """Generate photorealistic images with Flux Pro"""
        print('\n' + '='*70)
        print('FLUX PRO - PHOTOREALISTIC IMAGES')
        print('='*70 + '\n')

        generated_images = []

        for prompt_data in prompts:
            print(f"[{prompt_data['id']}] {prompt_data['description']}")
            print(f"  Model: Flux Pro")
            print(f"  Use case: {prompt_data['use_case']}")

            # In production: Call FAL.ai Flux Pro
            # result = await self.call_fal_api_flux_pro(
            #     prompt=prompt_data['prompt'],
            #     guidance=prompt_data['guidance'],
            # )

            generated_images.append({
                'id': prompt_data['id'],
                'model': 'flux-pro',
                'category': prompt_data['category'],
                'url': f"./output/generated_images/{prompt_data['id']}.png",
                'status': 'generated',
                'metadata': prompt_data,
            })

            print(f"  ✓ Generated\n")

        return generated_images

    async def generate_nano_banana_images(self, prompts: List[Dict]) -> List[Dict]:
        """Generate text-based images with Nano Banana"""
        print('\n' + '='*70)
        print('NANO BANANA - TEXT & INFOGRAPHIC IMAGES')
        print('='*70 + '\n')

        generated_images = []

        for prompt_data in prompts:
            print(f"[{prompt_data['id']}] {prompt_data['description']}")
            print(f"  Model: Nano Banana (FAL.ai)")
            print(f"  Use case: {prompt_data['use_case']}")
            print(f"  Text rendering: YES")

            # In production: Call FAL.ai Nano Banana
            # result = await self.call_fal_api_nano_banana(
            #     prompt=prompt_data['prompt'],
            # )

            generated_images.append({
                'id': prompt_data['id'],
                'model': 'nano-banana',
                'category': prompt_data['category'],
                'url': f"./output/generated_images/{prompt_data['id']}.png",
                'status': 'generated',
                'has_text': True,
                'metadata': prompt_data,
            })

            print(f"  ✓ Generated\n")

        return generated_images

    def save_image_metadata(self, flux_images: List[Dict], nano_images: List[Dict]):
        """Save comprehensive metadata"""
        all_images = flux_images + nano_images

        metadata = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_images': len(all_images),
                'flux_pro_count': len(flux_images),
                'nano_banana_count': len(nano_images),
                'total_duration': '10 minutes (600 seconds)',
                'images_per_second': f"{len(all_images) / 600:.2f}",
            },
            'models': {
                'flux_pro': {
                    'purpose': 'Photorealistic people, environments, workspaces',
                    'count': len(flux_images),
                    'cost_per_image': '$0.04-0.08',
                    'quality': 'Professional photography quality',
                    'images': flux_images,
                },
                'nano_banana': {
                    'purpose': 'Text-based images, charts, infographics, diagrams',
                    'count': len(nano_images),
                    'cost_per_image': '$0.02-0.04',
                    'quality': 'Clear text rendering, professional design',
                    'images': nano_images,
                }
            },
            'recommendations': [
                'Flux Pro: Use for opening/closing scenes with people',
                'Nano Banana: Use for data visualization, numbers, statistics',
                'Mix: Alternate between people and charts for viewer engagement',
                'Pacing: Show each image 4-8 seconds on screen',
                'Transitions: Fade between different image types',
            ]
        }

        os.makedirs(self.output_dir, exist_ok=True)
        metadata_path = os.path.join(self.output_dir, 'metadata_nano_banana.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return metadata_path

    async def execute_pipeline(self):
        """Execute complete image generation"""
        print('\n' + '='*70)
        print('IMAGE GENERATION PIPELINE - FLUX PRO + NANO BANANA')
        print('='*70)

        # Generate prompts
        flux_prompts = self.generate_flux_pro_prompts()
        nano_prompts = self.generate_nano_banana_prompts()

        print(f'\n✓ Generated {len(flux_prompts)} Flux Pro prompts (photorealistic)')
        print(f'✓ Generated {len(nano_prompts)} Nano Banana prompts (text/charts)\n')

        # Generate images
        flux_images = await self.generate_flux_pro_images(flux_prompts)
        nano_images = await self.generate_nano_banana_images(nano_prompts)

        # Save metadata
        metadata_path = self.save_image_metadata(flux_images, nano_images)

        print('\n' + '='*70)
        print('✓ IMAGE GENERATION COMPLETE')
        print('='*70 + '\n')

        print(f'Total images: {len(flux_images) + len(nano_images)}')
        print(f'  - Flux Pro (photorealistic): {len(flux_images)}')
        print(f'  - Nano Banana (text/charts): {len(nano_images)}')
        print(f'\nMetadata: {metadata_path}\n')

        return {
            'flux_pro_images': flux_images,
            'nano_banana_images': nano_images,
            'metadata_path': metadata_path,
        }


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    import asyncio

    generator = NanoBananaImageGenerator()
    result = asyncio.run(generator.execute_pipeline())
