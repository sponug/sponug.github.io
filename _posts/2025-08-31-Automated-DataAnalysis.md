---
layout: post
title: Automated Data Analysis
---

Automating Exploratory Data analysis using PandasAI and chatGPT.

# Table of contents
1. [Introduction](#introduction)
2. [Solution Scope](#scope)
3. [Tech Stack](#techstack)
4. [Work flow](#workflow)
5. [Code] (#code)

## Introduction <a name="introduction"></a>
In modern data analytics, one of the most time-consuming tasks is exploratory data analysis (EDA) — understanding the structure, patterns, and insights hidden in datasets. Analysts often spend significant effort generating meaningful questions and summarizing data.

This project leverages PandasAI and OpenAI’s language models to automate the EDA process. It allows users to drop CSV files into a folder and automatically:
- Generate insightful analytical questions.
- Produce textual, tabular, or visual answers.
- Summarize categorical distributions safely.
- Save results for further analysis or reporting.
- This is designed to be continuous, extensible, and robust, providing a foundation for AI-assisted data analytics workflows.

## Scope <a name="scope"></a>
In Scope:
  - Reading CSV files dropped into a designated folder.
  - Using PandasAI and OpenAI LLM to generate questions and answers.
  - Summarizing distributions of categorical variables as text.
  - Generating charts for numeric variables (optional enhancement).
  - Saving results in JSON format.
Out of Scope:
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

## Code <a name="code"></a>
    
