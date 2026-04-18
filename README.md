# AI-driven Healthcare Marketing Pipeline

A data-driven system that transforms social media user demand into AI-generated healthcare marketing content.

---

## Overview

This project builds an end-to-end pipeline:

Data → Analysis → AI Content → Image → Publishing

It uses social media data (Reddit, X, YouTube) to:
- Identify real user concerns (cost, trust, screening, etc.)
- Generate platform-specific marketing content using LLMs
- Produce ad-ready creatives (text + image)
- Support semi-automated publishing workflows

---

## Project Structure

data/
- raw/ (not included)
- cleaned/

analyze/
- analyze_and_split_corpus.py
- promo_outputs/
- analysis_outputs/

content/
- deepseek_marketing_generator_v5b_platform_split.py
- semi_auto_publish.py
- generated_images/
- final_creatives/

---

## Pipeline

1. Data Collection  
Run crawler scripts for Reddit / X / YouTube  
(Requires logged-in browser and API keys)

2. Data Cleaning  
python data/clean_all_data.py  

3. Data Analysis  
python analyze/analyze_and_split_corpus.py  

4. AI Content Generation  
python content/deepseek_marketing_generator_v5b_platform_split.py  

5. Publishing  
python content/semi_auto_publish.py prepare  
python content/semi_auto_publish.py export  

---

## Environment Variables

Create a `.env` file based on `.env.example`:

DEEPSEEK_API_KEY=your_key  
HF_TOKEN=your_token  
YOUTUBE_API_KEY=your_key  

---

## Notes

- Crawling scripts require a logged-in browser (Reddit / X)  
- API keys are required for DeepSeek, Hugging Face, and YouTube  
- Raw data is not included  
- Some scripts are environment-dependent and may not run directly  

---

## Tech Stack

Python, Pandas, NLP, DeepSeek (LLM), Hugging Face, Selenium, Playwright

---

## License

For academic and portfolio use.
