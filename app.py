import gradio as gr
import os
import re
import json
import spacy
import pandas as pd
from groq import Groq
from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Literal

# --- 1. SETUP ---
print("Initializing NLP models...")
try:
    nlp = spacy.load("en_core_web_trf")
except:
    print("Downloading Spacy Model (en_core_web_trf)...")
    os.system("python -m spacy download en_core_web_trf")
    nlp = spacy.load("en_core_web_trf")

# --- 2. DATA MODELS ---
class Salutation(BaseModel):
    phrase_used: str = Field(..., description="The exact opening phrase.")
    level: Literal["No Salutation", "Normal", "Good", "Excellent"]
    @computed_field
    def sal_score(self) -> int:
        mapping = {"No Salutation": 0, "Normal": 2, "Good": 4, "Excellent": 5}
        return mapping.get(self.level, 0)

class BasicDetails(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    school_class: Optional[List[str]] = None
    family: Optional[str] = None
    hobbies: Optional[List[str]] = None
    @computed_field
    def bd_score(self) -> int:
        found = [self.name, self.age, self.school_class, self.family, self.hobbies]
        return sum(1 for item in found if item) * 4

class ExtraDetails(BaseModel):
    about_family: Optional[str] = None
    origin: Optional[str] = None
    ambition: Optional[str] = None
    unique_fact: Optional[str] = None
    strengths: Optional[List[str]] = None
    @computed_field
    def ed_score(self) -> int:
        found = [self.about_family, self.origin, self.ambition, self.unique_fact, self.strengths]
        return sum(1 for item in found if item) * 2

class FlowSequence(BaseModel):
    is_order_followed: bool
    @computed_field
    def flow_score(self) -> int:
        return 5 if self.is_order_followed else 0

class GrammarError(BaseModel):
    error_text: str
    correction: str
    reason: str

class GrammarAnalysis(BaseModel):
    errors: List[GrammarError] = Field(default_factory=list)
    def calculate_score(self, total_words: int) -> int:
        if total_words == 0: return 0
        raw = 1 - min((10 * len(self.errors)) / total_words, 1)
        if raw >= 0.9: return 10
        elif 0.7 <= raw < 0.9: return 8
        elif 0.5 <= raw < 0.7: return 6
        elif 0.3 <= raw < 0.5: return 4
        return 2

class Engagement(BaseModel):
    sentiment_label: Literal["Positive", "Neutral", "Negative"]
    positivity_probability: float
    @computed_field
    def eng_score(self) -> int:
        val = self.positivity_probability
        if val >= 0.9: return 15
        elif 0.7 <= val < 0.9: return 12
        elif 0.5 <= val < 0.7: return 9
        elif 0.3 <= val < 0.5: return 6
        return 3

class EvaluationResult(BaseModel):
    salutation: Salutation
    basic_details: BasicDetails
    extra_details: ExtraDetails
    flow: FlowSequence
    grammar: GrammarAnalysis
    engagement: Engagement

# --- 3. HTML REPORT GENERATOR ---
def generate_html_report(total_score, wpm, speech_cat, df, analysis_data):
    """
    Generates a single HTML file containing the Scorecard and the formatted Details.
    """
    
    # 1. Generate Score Table Rows
    score_rows = ""
    for _, row in df.iterrows():
        score_rows += f"<tr><td>{row['Category']}</td><td>{row['Metric']}</td><td><strong>{row['Score']}</strong> / {row['Max']}</td></tr>"

    # 2. Format Basic Details Lists
    def format_list(item):
        if isinstance(item, list): return ", ".join(item)
        return item if item else "<em>Not mentioned</em>"

    # 3. Format Grammar Errors
    grammar_html = ""
    if not analysis_data.grammar.errors:
        grammar_html = "<div class='success-box'>✅ Great job! No major grammar errors detected.</div>"
    else:
        for err in analysis_data.grammar.errors:
            grammar_html += f"""
            <div class='grammar-box'>
                <p><strong>❌ Wrong:</strong> <span style="text-decoration: line-through; color: #7f8c8d;">{err.error_text}</span></p>
                <p><strong>✅ Right:</strong> <span style="color: #27ae60; font-weight: bold;">{err.correction}</span></p>
                <p class="reason">💡 {err.reason}</p>
            </div>
            """

    # 4. Build the Full HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Speech Analysis Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px; color: #333; }}
            .container {{ max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            
            /* Header */
            h1 {{ text-align: center; color: #2c3e50; margin-bottom: 10px; }}
            .summary {{ text-align: center; font-size: 1.2em; color: #7f8c8d; margin-bottom: 30px; }}
            
            /* Score Circle */
            .score-container {{ text-align: center; margin-bottom: 40px; }}
            .big-score {{ font-size: 4em; font-weight: 800; color: #6c5ce7; display: block; line-height: 1; }}
            .score-label {{ font-size: 1em; text-transform: uppercase; letter-spacing: 1px; color: #a29bfe; }}

            /* Sections */
            h2 {{ border-bottom: 2px solid #f1f2f6; padding-bottom: 10px; margin-top: 40px; color: #2d3436; }}
            
            /* Table */
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th {{ text-align: left; background: #f8f9fa; padding: 12px; color: #636e72; }}
            td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            
            /* Grid for Details */
            .details-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .detail-card {{ background: #fff; border: 1px solid #dfe6e9; border-radius: 8px; padding: 20px; }}
            .detail-card h3 {{ margin-top: 0; color: #6c5ce7; font-size: 1.1em; }}
            .detail-row {{ margin-bottom: 10px; display: flex; justify-content: space-between; }}
            .detail-label {{ font-weight: 600; color: #636e72; }}
            .detail-val {{ text-align: right; color: #2d3436; max-width: 60%; }}

            /* Grammar */
            .grammar-box {{ background: #fff0f0; border-left: 4px solid #ff7675; padding: 15px; margin-bottom: 15px; border-radius: 4px; }}
            .success-box {{ background: #e3fcef; border-left: 4px solid #00b894; padding: 15px; color: #00b894; font-weight: bold; }}
            .reason {{ font-style: italic; color: #636e72; font-size: 0.9em; margin-top: 5px; }}

            /* Tags */
            .tag {{ background: #dfe6e9; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; margin-left: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Speech Analysis Report</h1>
            <div class="summary">
                Speed: <strong>{wpm} WPM</strong> ({speech_cat}) &bull; Tone: <strong>{analysis_data.engagement.sentiment_label}</strong>
            </div>

            <div class="score-container">
                <span class="big-score">{total_score}</span>
                <span class="score-label">Total Score / 100</span>
            </div>

            <h2>📊 Score Breakdown</h2>
            <table>
                <thead><tr><th>Category</th><th>Metric</th><th>Score</th></tr></thead>
                <tbody>{score_rows}</tbody>
            </table>

            <h2>📝 Content Details</h2>
            <div class="details-grid">
                <div class="detail-card">
                    <h3>👤 Basic Information</h3>
                    <div class="detail-row"><span class="detail-label">Opening:</span> <span class="detail-val">{analysis_data.salutation.phrase_used}</span></div>
                    <div class="detail-row"><span class="detail-label">Name:</span> <span class="detail-val">{format_list(analysis_data.basic_details.name)}</span></div>
                    <div class="detail-row"><span class="detail-label">Age:</span> <span class="detail-val">{format_list(analysis_data.basic_details.age)}</span></div>
                    <div class="detail-row"><span class="detail-label">Class/Job:</span> <span class="detail-val">{format_list(analysis_data.basic_details.school_class)}</span></div>
                    <div class="detail-row"><span class="detail-label">Hobbies:</span> <span class="detail-val">{format_list(analysis_data.basic_details.hobbies)}</span></div>
                </div>

                <div class="detail-card">
                    <h3>🌟 Deeper Insights</h3>
                    <div class="detail-row"><span class="detail-label">Family Context:</span> <span class="detail-val">{format_list(analysis_data.basic_details.family)}</span></div>
                    <div class="detail-row"><span class="detail-label">About Family:</span> <span class="detail-val">{format_list(analysis_data.extra_details.about_family)}</span></div>
                    <div class="detail-row"><span class="detail-label">Ambition:</span> <span class="detail-val">{format_list(analysis_data.extra_details.ambition)}</span></div>
                    <div class="detail-row"><span class="detail-label">Unique Fact:</span> <span class="detail-val">{format_list(analysis_data.extra_details.unique_fact)}</span></div>
                </div>
            </div>

            <h2>🛠️ Grammar Feedback</h2>
            {grammar_html}

        </div>
    </body>
    </html>
    """
    return html

# --- 4. MAIN LOGIC ---
def clean_json_text(text):
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != -1: return text[start:end]
        return text
    except: return text

def analyze_speech(api_key, transcript, duration_seconds):
    empty_df = pd.DataFrame(columns=["Category", "Metric", "Score", "Max"])
    
    if not api_key or api_key.strip() == "":
        return "⚠️ Error: Please enter your Groq API Key.", empty_df, None
    
    try:
        # --- SPACY METRICS ---
        doc = nlp(transcript)
        words = [token.text for token in doc if token.is_alpha]
        word_count = len(words)
        
        wpm = round((word_count / duration_seconds) * 60) if duration_seconds > 0 else 0
        if wpm > 161: speech_cat, speech_score = "Too Fast", 2
        elif 141 <= wpm <= 160: speech_cat, speech_score = "Fast", 6
        elif 111 <= wpm <= 140: speech_cat, speech_score = "Ideal", 10
        elif 81 <= wpm <= 110: speech_cat, speech_score = "Slow", 6
        else: speech_cat, speech_score = "Too Slow", 2

        ttr = len(set(w.lower() for w in words)) / word_count if word_count > 0 else 0
        vocab_score = 10 if ttr >= 0.9 else 8 if ttr >= 0.7 else 6
        
        fillers = ["um", "uh", "like", "you know", "so", "actually"]
        found_fillers = []
        for f in fillers:
            found_fillers.extend(re.findall(rf"\b{f}\b", transcript, re.IGNORECASE))
        filler_rate = round((len(found_fillers)/word_count)*100, 2) if word_count > 0 else 0
        clarity_score = 15 if filler_rate <= 3 else 12

        # --- GROQ LLM CALL ---
        SYSTEM_PROMPT = """
        You are an expert Linguistic Evaluator and Speech Coach AI. 
        Your task is to analyze the provided speech transcript and extract structured data regarding the speaker's content, grammar, and engagement.
        You must output a JSON object that strictly adheres to the schema provided below.
        ### OUTPUT SCHEMA:
        {schema}
        """.format(schema=json.dumps(EvaluationResult.model_json_schema(), indent=2))
        
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript}
            ],
        )
        
        cleaned_content = clean_json_text(completion.choices[0].message.content)
        data = EvaluationResult.model_validate_json(cleaned_content)

        # --- SCORING ---
        grammar_score = data.grammar.calculate_score(word_count)
        sal_score = data.salutation.sal_score
        kw_score = data.basic_details.bd_score + data.extra_details.ed_score
        flow_score = data.flow.flow_score
        
        df_data = [
            ["Content", "Salutation", sal_score, 5],
            ["Content", "Key Details", kw_score, 20],
            ["Content", "Flow", flow_score, 5],
            ["Speech Rate", f"{wpm} WPM ({speech_cat})", speech_score, 10],
            ["Language", "Grammar", grammar_score, 10],
            ["Language", "Vocabulary", vocab_score, 10],
            ["Clarity", "Fillers", clarity_score, 15],
            ["Engagement", data.engagement.sentiment_label, data.engagement.eng_score, 15],
        ]
        df = pd.DataFrame(df_data, columns=["Category", "Metric", "Score", "Max"])
        total_score = int(df["Score"].sum())
        
        # --- HTML GENERATION ---
        html_content = generate_html_report(total_score, wpm, speech_cat, df, data)
        
        filename = "Speech_Analysis_Report.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        report_text = f"""## 🏆 Final Score: {total_score}/100
        **Speed:** {wpm} WPM ({speech_cat})
        **Tone:** {data.engagement.sentiment_label}
        """
        
        return report_text, df, filename

    except Exception as e:
        return f"❌ Error: {str(e)}", empty_df, None

# --- 5. UI ---
with gr.Blocks(theme=gr.themes.Soft(), title="AI Speech Coach") as demo:
    gr.Markdown("# 🎤 AI Speech Coach (Local)")
    gr.Markdown("Paste your speech, enter your Groq API Key, and get a professional HTML report.")
    
    with gr.Row():
        with gr.Column(scale=1):
            api_input = gr.Textbox(label="🔑 Groq API Key", placeholder="gsk_...", type="password")
            dur_input = gr.Number(label="⏱️ Speech Duration (seconds)", value=60, minimum=1)
            txt_input = gr.Textbox(label="📝 Speech Transcript", lines=10, 
                                   value="Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. I am 13 years old. Thank you.")
            btn = gr.Button("🚀 Analyze Speech", variant="primary")
            
        with gr.Column(scale=1):
            report_output = gr.Markdown(label="Summary")
            df_output = gr.Dataframe(label="Score Breakdown")
            file_output = gr.File(label="📥 Download Full Report (.html)")
            
    btn.click(analyze_speech, inputs=[api_input, txt_input, dur_input], outputs=[report_output, df_output, file_output])

if __name__ == "__main__":
    demo.launch(share=False)
