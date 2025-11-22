# 🎤 AI Speech Coach

A Python-based tool that evaluates speech transcripts for content, grammar, pacing, and engagement using LLMs (Groq/Llama-3) and NLP (Spacy).

## 🌟 Features
- **Automated Scoring:** Scores speeches out of 100 based on predefined metrics.
- **Speech Rate Analysis:** Calculates Words Per Minute (WPM).
- **Grammar Check:** Identifies errors and suggests corrections.
- **Detailed Reporting:** Generates a downloadable HTML report with raw JSON data embedded.

## 🧠 Scoring Formula (Total: 100 Points)

The final score is an aggregate of the following 5 categories:

### 1. Content & Structure (30 Points)
- **Salutation (5 pts):** Rated on warmth/professionalism (e.g., "Hello everyone" vs none).
- **Key Details (20 pts):** +4 points for each detail found (Name, Age, Class, Family, Hobbies).
- **Flow (5 pts):** +5 if speech follows a logical order (Intro -> Body -> Outro).

### 2. Speech Rate (10 Points)
Calculated as `(Word Count / Duration in Seconds) * 60`.
- **Ideal (111-140 WPM):** 10 pts
- **Fast/Slow (141-160 or 81-110 WPM):** 6 pts
- **Too Fast/Too Slow (>160 or <80 WPM):** 2 pts

### 3. Language & Grammar (20 Points)
- **Vocabulary (10 pts):** Based on Type-Token Ratio (Unique words / Total words).
- **Grammar (10 pts):** Deductions based on the density of grammatical errors found.

### 4. Clarity (15 Points)
- **Filler Words:** Checks for "um", "uh", "like", etc.
- **Score:** 15 pts if fillers are <3% of total words; otherwise 12 pts.

### 5. Engagement (15 Points)
- **Sentiment Analysis:** 15 pts for Positive/Enthusiastic tone, lower for Neutral/Negative.

## 🛠️ Tech Stack
- **Frontend:** Gradio
- **LLM:** Llama-3-70b via Groq API
- **NLP:** Spacy (`en_core_web_trf`)
- **Data Validation:** Pydantic
