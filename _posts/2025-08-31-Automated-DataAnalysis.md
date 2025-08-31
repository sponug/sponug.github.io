---
layout: post
title: Automated Data Analysis
---

Automating Exploratory Data analysis using PandasAI and chatGPT.

![latency](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/automated_eda.png)

# Table of contents
1. [Introduction](#introduction)
2. [Solution Scope](#scope)
3. [Tech Stack](#techstack)
4. [Work flow](#workflow)
5. [Source Code](#code)


## Introduction <a name="introduction"></a>
In modern data analytics, one of the most time-consuming tasks is exploratory data analysis (EDA) — understanding the structure, patterns, and insights hidden in datasets. Analysts often spend significant effort generating meaningful questions and summarizing data.

This project leverages PandasAI and OpenAI’s language models to automate the EDA process. It allows users to drop CSV files into a folder and automatically:
- Generate insightful analytical questions.
- Produce textual, tabular, or visual answers.
- Summarize categorical distributions safely.
- Save results for further analysis or reporting.
- This is designed to be continuous, extensible, and robust, providing a foundation for AI-assisted data analytics workflows.

## Scope <a name="scope"></a>
***In Scope***:
  - Reading CSV files dropped into a designated folder.
  - Using PandasAI and OpenAI LLM to generate questions and answers.
  - Summarizing distributions of categorical variables as text.
  - Generating charts for numeric variables (optional enhancement).
  - Saving results in JSON format.
    
***Out of Scope***:
  - Modifying original datasets.
  - Handling real-time streaming outside the watched folder.
  - Deploying as a full web application (optional future enhancement).

## Tech Stack <a name="techstack"></a>
  - Python	3.11	Main programming language
  - Pandas	1.x	Data manipulation
  - PandasAI	2.0+	AI-assisted data analysis
  - OpenAI LLM	GPT (via OpenAI API)	Generate questions, answers, and summaries
  - Watchdog	Python library	Folder/file watcher for automatic CSV ingestion

## Work Flow <a name="workflow"></a>
  - File ingestion: Users drop CSV files into a watched folder.
  - File detection: Watchdog triggers the analysis automatically.
  - PandasAI analysis: The AI examines the DataFrame columns and content.
  - Question generation: The LLM generates 5–10 insightful questions.
  - Answer generation: The AI provides answers, textual summaries, or charts.
  - Results storage: All results are saved as JSON and optionally charts in PNG format.
  - Reporting: Users can view results in the console or process saved files.

## Source Code <a name="code"></a>
  This Python script provides an automated, AI-powered data analysis pipeline for CSV files. It leverages PandasAI with OpenAI’s LLM to generate analytical insights, combined with Watchdog to detect new files in real-time.

Workflow Overview:
- **Real-Time data Monitoring**: Continuously watches a folder (data_folder) for new CSV files and triggers processing automatically.
- **Data Loading**: Reads the CSV into a Pandas DataFrame and handles any file errors gracefully.
- **Question Generation**: Uses PandasAI to generate 5–10 insightful analytical questions about the dataset without executing any analysis.
- **Answer Generation**: Answers each question safely, providing textual summaries, tables, or plots (saved as PNGs) while avoiding direct code execution on sensitive categorical columns.
- **Result Output**: Prints all question-answer pairs to the console and saves them as JSON files in qa_results.
- **Continuous Operation**: The script keeps running, allowing ongoing monitoring and analysis of newly added CSV files.
In short: the script transforms raw CSV data into actionable insights automatically, making exploratory data analysis faster, safer, and more consistent

[Soure Code](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/pandasai_filewatcher.py)

[Sample Results](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/Titanic_dataset_qa.json)
