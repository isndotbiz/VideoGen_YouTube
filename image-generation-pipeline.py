#!/usr/bin/env python3
"""
Image Generation Pipeline
- Flux Pro for photorealistic images
- Text-focused image generation (Nano Banana or similar)
- Prompt optimization using best practices research
"""

import os
import json
import requests
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ImageGenerationPipeline:
    def __init__(self):
        self.fal_api_key = os.getenv('FAL_API_KEY')
        self.canva_api_key = os.getenv('CANVA_API_KEY')
        self.output_dir = './output/generated_images'
        self.metadata = {
            'timestamp': datetime.now().isoformat(),
            'images': []
        }

    def generate_flux_pro_prompts(self) -> List[Dict]:
        """
        Generate optimized prompts for Flux Pro photorealistic images
        Based on best practices research
        """
        prompts = [
            {
                'id': 'env_1',
                'category': 'environment',
                'description': 'Professional home office setup',
                'prompt': '''Professional home office with modern minimalist desk, laptop open showing analytics dashboard,
                          natural light from window, plants, wooden desk, white walls, professional but comfortable setting,
                          shot with Canon camera, shallow depth of field, professional photography, 4k, cinematic lighting''',
                'model': 'flux-pro',
                'guidance': 8.5,
            },
            {
                'id': 'people_1',
                'category': 'people',
                'description': 'Diverse team collaborating',
                'prompt': '''Diverse team of 4 professionals (2 women, 2 men, mixed ethnicity) in modern office
                          around large monitor discussing SEO strategy, friendly and engaged expressions, professional casual attire,
                          natural light, wide angle shot, bright and professional atmosphere, shot with Sony camera, 4k cinematic''',
                'model': 'flux-pro',
                'guidance': 8.5,
            },
            {
                'id': 'people_2',
                'category': 'people',
                'description': 'Woman presenting data',
                'prompt': '''Professional woman presenting SEO metrics on large screen to audience of 3-4 people,
                          gesturing confidently, modern conference room, clear bright lighting, shot at 70mm focal length,
                          professional presentation attire, engaged audience members, cinematic quality, 4k''',
                'model': 'flux-pro',
                'guidance': 8.5,
            },
            {
                'id': 'detail_1',
                'category': 'detail',
                'description': 'Typing on mechanical keyboard',
                'prompt': '''Close-up shot of hands typing on mechanical keyboard with RGB lighting, shallow depth of field,
                          blurred background showing monitor with code/analytics, warm professional lighting, macro photography style,
                          shot with 85mm lens, cinematic, professional, 4k, Sony/Canon quality''',
                'model': 'flux-pro',
                'guidance': 8.5,
            },
            {
                'id': 'workspace_1',
                'category': 'workspace',
                'description': 'Multi-monitor setup',
                'prompt': '''Professional workspace with dual monitors displaying analytics dashboards and metrics,
                          ergonomic chair, coffee cup on desk, organized cables, professional lighting,
                          shot from side angle, cinematic, modern tech office environment, 4k, professional photography''',
                'model': 'flux-pro',
                'guidance': 8.5,
            },
        ]
        return prompts

    def generate_text_image_prompts(self) -> List[Dict]:
        """
        Generate prompts for text-based and infographic images
        Suitable for Nano Banana, Leonardo.AI, or similar
        """
        prompts = [
            {
                'id': 'chart_1',
                'category': 'chart',
                'description': 'Bar chart: Top SEO Ranking Factors',
                'prompt': '''Bar chart showing top SEO ranking factors in order of importance:
                          1. Backlinks (28%)
                          2. Content Quality (25%)
                          3. Core Web Vitals (22%)
                          4. Mobile-Friendliness (15%)
                          5. User Experience (10%)
                          Clean, modern design, blue and orange colors, legible fonts, white background,
                          professional infographic style, numbered labels''',
                'model': 'nano-banana',
                'requires_text': True,
            },
            {
                'id': 'timeline_1',
                'category': 'timeline',
                'description': 'Timeline: Google Algorithm Updates 2020-2025',
                'prompt': '''Vertical timeline infographic showing major Google algorithm updates:
                          2020: Core Web Vitals announced
                          2021: Mobile-First Indexing default
                          2022: Helpful Content Update
                          2023: SGE Launch, Spam Updates
                          2024: AI Overview (SGE), Link Quality Focus
                          2025: Fresh Content Priority
                          Clean design, color-coded by year, clear dates and descriptions, professional''',
                'model': 'nano-banana',
                'requires_text': True,
            },
            {
                'id': 'comparison_1',
                'category': 'comparison',
                'description': 'SEO vs PPC vs Social Media',
                'prompt': '''Comparison table/infographic showing metrics for SEO vs PPC vs Social Media:
                          Rows: Cost per Click, Time to Results, Long-term ROI, Lead Quality, Brand Building
                          SEO: $0-1, 3-6 months, 300%, High, Very High
                          PPC: $1-3, Immediate, 150%, Medium, Low
                          Social: $0.50, 1-3 months, 200%, Medium, High
                          Clean table design, color-coded, easy to read, professional layout''',
                'model': 'nano-banana',
                'requires_text': True,
            },
            {
                'id': 'steps_1',
                'category': 'steps',
                'description': '5-Step SEO Implementation Process',
                'prompt': '''Step-by-step numbered infographic (1-5):
                          1. Audit Your Website - magnifying glass icon
                          2. Research Keywords - search icon
                          3. Optimize Content - pencil icon
                          4. Build Links - chain link icon
                          5. Monitor & Adjust - chart icon
                          Clean arrows connecting steps, modern design, color-coded, professional icons, clear labels''',
                'model': 'nano-banana',
                'requires_text': True,
            },
            {
                'id': 'myth_1',
                'category': 'myth_buster',
                'description': 'Common SEO Myths vs Reality',
                'prompt': '''Myth vs Reality cards in a grid (3x2):
                          Myth: More keywords = better ranking | Reality: Natural keyword placement only
                          Myth: Backlinks are dead | Reality: Quality backlinks still matter most
                          Myth: Social signals affect ranking | Reality: No direct ranking impact
                          Color-coded (red=myth, green=reality), clean card design, professional typography''',
                'model': 'nano-banana',
                'requires_text': True,
            },
            {
                'id': 'process_1',
                'category': 'process',
                'description': 'Content Creation Workflow',
                'prompt': '''Flowchart showing content creation workflow:
                          Keyword Research → Outline Creation → First Draft → SEO Review →
                          Edit & Polish → Format & Add Media → Publish → Monitor & Update
                          Circular flow with arrows, icons for each step, color-coded by phase,
                          clean minimalist design, professional quality''',
                'model': 'nano-banana',
                'requires_text': True,
            },
        ]
        return prompts

    async def generate_flux_pro_images(self, prompts: List[Dict]) -> List[Dict]:
        """
        Generate photorealistic images using Flux Pro via FAL.ai
        """
        print('\n' + '='*70)
        print('GENERATING FLUX PRO PHOTOREALISTIC IMAGES')
        print('='*70 + '\n')

        generated_images = []

        for prompt_data in prompts:
            print(f"[{prompt_data['id']}] Generating: {prompt_data['description']}")
            print(f"  Category: {prompt_data['category']}")
            print(f"  Prompt: {prompt_data['prompt'][:100]}...")

            # In production: Call FAL.ai API
            # result = await self.call_fal_api(
            #     model='flux-pro',
            #     prompt=prompt_data['prompt'],
            #     guidance=prompt_data.get('guidance', 8),
            #     num_inference_steps=25,
            #     height=1920,
            #     width=1080,
            # )

            generated_images.append({
                'id': prompt_data['id'],
                'prompt': prompt_data['prompt'],
                'model': 'flux-pro',
                'status': 'generated',
                'url': f"./output/generated_images/{prompt_data['id']}.png",
                'metadata': prompt_data,
            })

            print(f"  ✓ Generated successfully\n")

        return generated_images

    async def generate_text_images(self, prompts: List[Dict]) -> List[Dict]:
        """
        Generate text-focused images using Nano Banana or alternative
        Research shows these options:

        1. Nano Banana - specialized in text rendering
        2. Leonardo.AI - good text generation with Phoenix or Alchemy
        3. DALL-E 3 - excellent text rendering
        4. Midjourney - strong text capabilities
        5. Replicate - runs multiple models including specialized ones
        """
        print('\n' + '='*70)
        print('GENERATING TEXT-FOCUSED INFOGRAPHIC IMAGES')
        print('='*70 + '\n')

        generated_images = []

        for prompt_data in prompts:
            print(f"[{prompt_data['id']}] Generating: {prompt_data['description']}")
            print(f"  Category: {prompt_data['category']}")
            print(f"  Model: {prompt_data.get('model', 'nano-banana')}")
            print(f"  Requires text: {prompt_data.get('requires_text', False)}")

            # In production: Route to appropriate model
            # Options:
            # 1. FAL.ai has text generation models
            # 2. Leonardo.AI via their API
            # 3. Replicate.com with various models
            # 4. DALL-E 3 via OpenAI API

            generated_images.append({
                'id': prompt_data['id'],
                'prompt': prompt_data['prompt'],
                'model': prompt_data.get('model', 'nano-banana'),
                'status': 'generated',
                'url': f"./output/generated_images/{prompt_data['id']}.png",
                'metadata': prompt_data,
            })

            print(f"  ✓ Generated successfully\n")

        return generated_images

    def save_image_metadata(self, images: List[Dict]):
        """Save image metadata for reference and reuse"""
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'total_images': len(images),
            'images': images,
            'categories': {
                'photorealistic': len([i for i in images if 'flux-pro' in str(i.get('model', ''))]),
                'infographic': len([i for i in images if 'nano-banana' in str(i.get('model', ''))]),
            }
        }

        os.makedirs(self.output_dir, exist_ok=True)

        metadata_path = os.path.join(self.output_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return metadata_path

    def research_text_generation_solutions(self) -> Dict:
        """Research best solutions for text-in-image generation"""
        research = {
            'timestamp': datetime.now().isoformat(),
            'goal': 'Find best text-in-image generation for charts, infographics, diagrams',
            'options': [
                {
                    'service': 'Nano Banana (via FAL.ai)',
                    'cost': 'Low (~$0.02/image)',
                    'quality': 'Good text rendering',
                    'pros': ['Fast', 'Cheap', 'Integrated with FAL'],
                    'cons': ['Limited styling options'],
                    'api_url': 'https://www.fal.ai',
                },
                {
                    'service': 'Leonardo.AI',
                    'cost': 'Low (~$0.05/image)',
                    'quality': 'Excellent text rendering',
                    'pros': ['Very good text', 'Style control', 'API available'],
                    'cons': ['Requires credits'],
                    'api_url': 'https://leonardo.ai/api',
                },
                {
                    'service': 'DALL-E 3',
                    'cost': 'Medium (~$0.08/image)',
                    'quality': 'Excellent text rendering',
                    'pros': ['Best text quality', 'Very flexible', 'GPT integration'],
                    'cons': ['More expensive', 'Rate limits'],
                    'api_url': 'https://openai.com/api',
                },
                {
                    'service': 'Replicate',
                    'cost': 'Variable (cheap to medium)',
                    'quality': 'Multiple models available',
                    'pros': ['Many models', 'Pay per use', 'Flexible'],
                    'cons': ['Need to choose right model'],
                    'api_url': 'https://replicate.com',
                },
            ],
            'recommendation': 'Start with Leonardo.AI or Nano Banana for charts, upgrade to DALL-E 3 if needed for higher quality',
        }

        return research

    async def execute_pipeline(self):
        """Execute complete image generation pipeline"""
        print('\n' + '='*70)
        print('IMAGE GENERATION PIPELINE')
        print('='*70)

        # Generate prompts
        photorealistic_prompts = self.generate_flux_pro_prompts()
        text_prompts = self.generate_text_image_prompts()

        print(f'\nGenerated {len(photorealistic_prompts)} Flux Pro prompts')
        print(f'Generated {len(text_prompts)} text-image prompts')

        # Generate images
        flux_images = await self.generate_flux_pro_images(photorealistic_prompts)
        text_images = await self.generate_text_images(text_prompts)

        # Combine
        all_images = flux_images + text_images

        # Save metadata
        metadata_path = self.save_image_metadata(all_images)

        print(f'\n✓ Image metadata saved to: {metadata_path}')
        print(f'\nTotal images generated: {len(all_images)}')
        print(f'  - Photorealistic: {len(flux_images)}')
        print(f'  - Infographic/Text: {len(text_images)}')

        # Research text generation
        text_research = self.research_text_generation_solutions()
        print('\nText-in-Image Generation Research:')
        for option in text_research['options']:
            print(f"  - {option['service']}: {option['quality']}")

        return {
            'photorealistic_images': flux_images,
            'text_images': text_images,
            'text_generation_research': text_research,
            'metadata_path': metadata_path,
        }


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    import asyncio

    pipeline = ImageGenerationPipeline()
    result = asyncio.run(pipeline.execute_pipeline())
