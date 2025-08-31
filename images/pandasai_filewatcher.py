import os
import time
import json
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# -----------------------------
# Step 1: Configure folders
# -----------------------------
WATCH_FOLDER = "data_folder"      # Folder to watch for new CSVs
OUTPUT_FOLDER = "qa_results"      # Folder to save Q&A results
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Step 2: PandasAI analysis function
# -----------------------------
def analyze_csv(file_path):
    print(f"\nProcessing new file: {file_path}")
    
    # Load CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Initialize PandasAI
    llm = OpenAI()  # uses OPENAI_API_KEY from environment
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": True})
    
    # -----------------------------
    # Generate questions
    # -----------------------------
    questions_query = """
    You are a data analyst. Look at the DataFrame columns, types, and content.
    Generate 5–10 insightful analytical questions that could be asked to explore this data.
    Return the questions in Python code that declares a variable 'result' as a dictionary:
    { "type": "string", "value": "numbered list of questions" }
    Do NOT execute any analysis or generate charts.
    """
    
    try:
        questions_result = sdf.chat(questions_query)
        questions_text = questions_result['value'] if isinstance(questions_result, dict) else questions_result
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return
    
    # -----------------------------
    # Answer each question safely
    # -----------------------------
    qa_pairs = []
    for q in questions:
        answer_query = f"""
        You are a data analyst. Using only the DataFrame dfs[0]:
        - Provide a concise answer to the following question.
        - If the question can be answered with text, return a string.
        - If a table is needed, return a dataframe.
        - If a plot is needed, return a plot (PNG).
        - For distributions of categorical variables (like 'Pclass', 'Survived', 'Cabin'), provide a textual summary instead of executing code.
        - Do NOT reference any variable other than dfs[0].
        - Wrap the result in Python code as a dictionary: {{ "type": ..., "value": ... }}.
        Question: "{q}"
        """
        try:
            answer_result = sdf.chat(answer_query)
            answer_value = answer_result['value'] if isinstance(answer_result, dict) else str(answer_result)
            qa_pairs.append((q, answer_value))
        except Exception as e:
            qa_pairs.append((q, f"Could not answer automatically: {str(e)}"))
    
    # -----------------------------
    # Print results
    # -----------------------------
    print("\n=== Questions and Answers ===")
    for i, (question, answer) in enumerate(qa_pairs, start=1):
        print(f"{i}. Q: {question}")
        print(f"   A: {answer}\n")
    
    # -----------------------------
    # Save results to JSON
    # -----------------------------
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_qa.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([{"question": q, "answer": a} for q, a in qa_pairs], f, indent=2)
    print(f"Results saved to {output_file}")

# -----------------------------
# Step 3: Watch folder for new CSV files
# -----------------------------
class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"Detected new CSV: {event.src_path}")
            analyze_csv(event.src_path)

observer = Observer()
observer.schedule(CSVHandler(), WATCH_FOLDER, recursive=False)
observer.start()

print(f"Watching folder '{WATCH_FOLDER}' for new CSV files. Press Ctrl+C to stop.")

# -----------------------------
# Step 4: Keep script alive
# -----------------------------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping observer...")
    observer.stop()
observer.join()
