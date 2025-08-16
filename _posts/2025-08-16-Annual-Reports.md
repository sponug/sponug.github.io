---
layout: post
title: Extracting Business Model Canvas Insights from Annual Reports (A Weekend Experiment)
---

**Disclaimer**  
This is a personal technical experiment that I conducted independently and is not associated with, endorsed by, or representative of my employer in any way. It should not be considered financial advice or commentary of any kind. The experiment was performed using publicly available documents from the bank where I work. Any errors or omissions are solely my responsibility.

# Table of contents
1. [Introduction](#introduction)
2. [PDF's Into Searchable DB](#tech1)
3. [Are there any surprises?](#tech2)
4. [Interface for querying](#tech3)

## Introduction <a name="introduction"></a>
Annual reports are rich in information but notoriously hard to mine for structured insights. I wanted to see if modern AI tooling could automatically map 10 years of annual reports into the well-known Business Model Canvas (BMC) framework.

The primary **goals** were:
- Work within a strict time frame (4–5 hours).
- Process last 10 years of annual reports.
- Build with a minimal tech stack.
- Generate insights using BMC.
- Focus on learning over perfection

## PDF's Into Searchable DB <a name="tech1"></a>

This script’s job is to **read all your PDF reports, chop them into small chunks of text, generate AI embeddings, and save them into a Chroma database** so you can later query them with an LLM.

Ingestion (one-time)
--------------------
[ingest](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/ingest.png)
   
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

[query](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/query.png)

[Source code for app.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/app.py)

