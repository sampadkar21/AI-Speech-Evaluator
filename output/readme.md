![img](output/interface_1.png)


    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Speech Analysis Report</title>
        <style>
            body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
            
            /* Header */
            h1 { text-align: center; color: #2c3e50; margin-bottom: 10px; }
            .summary { text-align: center; font-size: 1.2em; color: #7f8c8d; margin-bottom: 30px; }
            
            /* Score Circle */
            .score-container { text-align: center; margin-bottom: 40px; }
            .big-score { font-size: 4em; font-weight: 800; color: #6c5ce7; display: block; line-height: 1; }
            .score-label { font-size: 1em; text-transform: uppercase; letter-spacing: 1px; color: #a29bfe; }

            /* Sections */
            h2 { border-bottom: 2px solid #f1f2f6; padding-bottom: 10px; margin-top: 40px; color: #2d3436; }
            
            /* Table */
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th { text-align: left; background: #f8f9fa; padding: 12px; color: #636e72; }
            td { padding: 12px; border-bottom: 1px solid #eee; }
            
            /* Grid for Details */
            .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .detail-card { background: #fff; border: 1px solid #dfe6e9; border-radius: 8px; padding: 20px; }
            .detail-card h3 { margin-top: 0; color: #6c5ce7; font-size: 1.1em; }
            .detail-row { margin-bottom: 10px; display: flex; justify-content: space-between; }
            .detail-label { font-weight: 600; color: #636e72; }
            .detail-val { text-align: right; color: #2d3436; max-width: 60%; }

            /* Grammar */
            .grammar-box { background: #fff0f0; border-left: 4px solid #ff7675; padding: 15px; margin-bottom: 15px; border-radius: 4px; }
            .success-box { background: #e3fcef; border-left: 4px solid #00b894; padding: 15px; color: #00b894; font-weight: bold; }
            .reason { font-style: italic; color: #636e72; font-size: 0.9em; margin-top: 5px; }

            /* Tags */
            .tag { background: #dfe6e9; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; margin-left: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Speech Analysis Report</h1>
            <div class="summary">
                Speed: <strong>150 WPM</strong> (Fast) &bull; Tone: <strong>Positive</strong>
            </div>

            <div class="score-container">
                <span class="big-score">82</span>
                <span class="score-label">Total Score / 100</span>
            </div>

            <h2>📊 Score Breakdown</h2>
            <table>
                <thead><tr><th>Category</th><th>Metric</th><th>Score</th></tr></thead>
                <tbody><tr><td>Content</td><td>Salutation</td><td><strong>4</strong> / 5</td></tr><tr><td>Content</td><td>Key Details</td><td><strong>26</strong> / 30</td></tr><tr><td>Content</td><td>Flow</td><td><strong>5</strong> / 5</td></tr><tr><td>Speech Rate</td><td>150 WPM (Fast)</td><td><strong>6</strong> / 10</td></tr><tr><td>Language</td><td>Grammar</td><td><strong>8</strong> / 10</td></tr><tr><td>Language</td><td>Vocabulary</td><td><strong>6</strong> / 10</td></tr><tr><td>Clarity</td><td>Fillers</td><td><strong>15</strong> / 15</td></tr><tr><td>Engagement</td><td>Positive</td><td><strong>12</strong> / 15</td></tr></tbody>
            </table>

            <h2>📝 Content Details</h2>
            <div class="details-grid">
                <div class="detail-card">
                    <h3>👤 Basic Information</h3>
                    <div class="detail-row"><span class="detail-label">Opening:</span> <span class="detail-val">Hello everyone</span></div>
                    <div class="detail-row"><span class="detail-label">Name:</span> <span class="detail-val">Muskan</span></div>
                    <div class="detail-row"><span class="detail-label">Age:</span> <span class="detail-val">13 years old</span></div>
                    <div class="detail-row"><span class="detail-label">Class/Job:</span> <span class="detail-val">Class 8th B section, Christ Public School</span></div>
                    <div class="detail-row"><span class="detail-label">Hobbies:</span> <span class="detail-val">playing cricket</span></div>
                </div>

                <div class="detail-card">
                    <h3>🌟 Deeper Insights</h3>
                    <div class="detail-row"><span class="detail-label">Family Context:</span> <span class="detail-val">me, my mother and my father</span></div>
                    <div class="detail-row"><span class="detail-label">About Family:</span> <span class="detail-val">very kind hearted to everyone and soft spoken</span></div>
                    <div class="detail-row"><span class="detail-label">Ambition:</span> <span class="detail-val"><em>Not mentioned</em></span></div>
                    <div class="detail-row"><span class="detail-label">Unique Fact:</span> <span class="detail-val">I see in mirror and talk by myself</span></div>
                </div>
            </div>

            <h2>🛠️ Grammar Feedback</h2>
            
            <div class='grammar-box'>
                <p><strong>❌ Wrong:</strong> <span style="text-decoration: line-through; color: #7f8c8d;">I see in mirror and talk by myself</span></p>
                <p><strong>✅ Right:</strong> <span style="color: #27ae60; font-weight: bold;">I talk to myself in the mirror</span></p>
                <p class="reason">💡 Incorrect Preposition Usage</p>
            </div>
            
            <div class='grammar-box'>
                <p><strong>❌ Wrong:</strong> <span style="text-decoration: line-through; color: #7f8c8d;">One thing people don't know about me is that I once stole a toy from one of my cousin</span></p>
                <p><strong>✅ Right:</strong> <span style="color: #27ae60; font-weight: bold;">One thing people don't know about me is that I once stole a toy from one of my cousins</span></p>
                <p class="reason">💡 Subject-Verb Agreement</p>
            </div>
            

        </div>
    </body>
    </html>

---

![img](output/interface_2.png)
  
  
