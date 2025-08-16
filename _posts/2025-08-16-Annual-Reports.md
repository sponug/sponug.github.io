---
layout: post
title: Business Model Canvas from Annual Reports - An experiment
---

Warning - this is a technical experiment and should not be considered financial advice or commentary of any kind

# Table of contents
1. [Introduction](#introduction)
2. [PDF's Into Searchable DB](#tech1)
3. [Another paragraph](#paragraph2)

## This is the introduction <a name="introduction"></a>
The primary **goals** were:
1. Process last 10 years of annual reports
2. Build something working with a minimal tech stack
3. Generate insights into the business using business model canvas
4. Work within a strict time frame – complete the entire process, including this write-up, in **4–5 hours**.
5. Focus on learning over perfection – prioritize understanding the workflow of creating and testing an agent over building a production-ready tool.

## PDF's Into Searchable DB <a name="tech1"></a>

This script’s job is to **read all your PDF reports, chop them into small chunks of text, generate AI embeddings, and save them into a Chroma database** so you can later query them with an LLM.

---
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
---

## In Simple Terms
This script **turns your PDFs into a searchable database** by chopping them into small pieces, converting them into AI-friendly vectors, and storing them in Chroma. Later, you can use this database to **ask questions across all your PDFs** instead of reading them manually.

[Source code for ingest.py](images/ingest.py) 

### Sub paragraph <a name="subparagraph1"></a>
This is a sub paragraph, formatted in heading 3 style

## Another paragraph <a name="paragraph2"></a>
The second paragraph text

