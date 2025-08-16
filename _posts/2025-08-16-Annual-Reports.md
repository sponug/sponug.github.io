---
layout: post
title: Business Model Canvas from Annual Reports - An experiment
---

**Disclaimer**  
This is a personal technical experiment that I conducted independently and is not associated with, endorsed by, or representative of my employer in any way. It should not be considered financial advice or commentary of any kind. The experiment was performed using publicly available documents from the bank where I work. Any errors or omissions are solely my responsibility.

# Table of contents
1. [Introduction](#introduction)
2. [PDF's Into Searchable DB](#tech1)
3. [Are there any surprises?](#tech2)
4. [Interface for querying](#tech3)

## This is the introduction <a name="introduction"></a>
The primary **goals** were:
1. Process last 10 years of annual reports
2. Build something working with a minimal tech stack
3. Generate insights into the business using business model canvas
4. Work within a strict time frame – complete the entire process, including this write-up, in **4–5 hours**.
5. Focus on learning over perfection – prioritize understanding the workflow of creating and testing an agent over building a production-ready tool.

## PDF's Into Searchable DB <a name="tech1"></a>

This script’s job is to **read all your PDF reports, chop them into small chunks of text, generate AI embeddings, and save them into a Chroma database** so you can later query them with an LLM.

### 1. Setup
- Looks for PDFs in a folder called `annual_reports`.  
- Sets up a Chroma database inside `rag_db`.  
- Connects to OpenAI (you need your API key set).

### 2. Chunking the Text
- Each PDF is read page by page.  
- The text is split into overlapping chunks (about 500 characters each, with 50 characters overlap).  
- Overlap ensures no important sentences are cut off in between chunks.  

### 3. Creating Embeddings
- For each chunk, the script calls OpenAI’s `text-embedding-3-small` model.  
- It does this in **batches** (default 50 chunks per request) to save time.  
- Embeddings are just numerical vectors that represent the meaning of the text.  

### 4. Storing in Chroma
- For every chunk, it saves:  
  - the text itself,  
  - metadata (like file name and page number),  
  - the embedding vector.  
- This goes into the Chroma collection called `"annual_reports"`.  

### 5. Error Handling
- If embedding or processing fails, it logs the error in `error.txt` but keeps going with the rest.  

### 6. Logging Progress
- Prints progress as it processes each PDF.  
- Shows how many chunks were stored and how long it took.  
- At the end, gives a summary: how many PDFs succeeded, failed, and where to look for errors.
   
This script **turns your PDFs into a searchable database** by chopping them into small pieces, converting them into AI-friendly vectors, and storing them in Chroma. Later, you can use this database to **ask questions across all your PDFs** instead of reading them manually.

[Source code for ingest.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/ingest.py) 

I did this experiment on publicly available annual reports from 2015-2024

## Are there any surprises <a name="tech2"></a>
Lets now check what some common themes across the 10 years of annual reports are . Ok - no surprises here -
1. Customer-Centric Service Approach (4522 chunks)
2. Westpac Group Annual Report Summary (3994 chunks)
3. Critical Accounting Estimates and Fair Value (3796 chunks)
4. Banking Industry Challenges and Strategies (3086 chunks)  
5. Loans to Directors and KMP (2811 chunks)
6. Capital Management and Shareholder Support (2557 chunks)  
7. Financial Performance Overview (2519 chunks)
8. Economic Outlook and Growth Trends (1935 chunks)
9. Capital Raising and Director Interests (1930 chunks)      
10. CEO Transition and Leadership Strategy (1607 chunks) 

[Source code for topics.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/topics.py)
This script takes all the AI-embedded chunks from your reports, groups them into clusters of related content, then uses GPT to give each cluster a human-readable topic name. Finally, it shows you the top recurring themes across the reports.

## Interface for querying <a name="tech3"></a>
This script builds a Q&A app for your annual reports.You ask a business question (freeform or guided by BMC blocks).
It searches the last 10 years of reports. GPT summarizes the findings into a clean, source-cited answer.

[Source code for app.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/app.py)

