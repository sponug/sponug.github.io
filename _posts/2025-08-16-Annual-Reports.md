---
layout: post
title: Extracting Business Model Canvas Insights from Annual Reports (A Weekend Experiment)
---

**Disclaimer**  
This is a personal technical experiment that I conducted independently and is not associated with, endorsed by, or representative of my employer in any way. It should not be considered financial advice or commentary of any kind. The experiment was performed using publicly available documents from the bank where I work. Any errors or omissions are solely my responsibility.

# Table of contents
1. [Introduction](#introduction)
2. [PDF's Into Searchable DB](#tech1)
3. [Topics Across 10 Years](#tech2)
4. [Querying with the Business Model Canvas](#tech3)
5. [Business Model Canvas](#business)
   1. [Customer Segments](#customer)
   2. [Value Propositions](#valprops)
   3. [Channels](#Channels)
   4. [Customer Relationships - revisit](#custrel)
   5. [Revenue Streams - revisit](#rev)
   6. [Key Resources - revisit](#res)
   7. [Key Activities - revisit](#activities)
   8. [Key Partnerships - revisit](#part)
   9. [Cost Structure - revisit](#cost)
6. [Conclusion](#conclusion)

## Introduction <a name="introduction"></a>
Annual reports are rich in information but notoriously hard to mine for structured insights. I wanted to see if modern AI tooling could automatically map 10 years of annual reports into the well-known Business Model Canvas (BMC) framework.

The primary **goals** were:
- Work within a strict time frame (4–5 hours).
- Process last 10 years of annual reports.
- Build with a minimal tech stack.
- Generate insights using BMC.
- Focus on learning over perfection

## PDF's Into Searchable DB<a name="tech1"></a>

This script’s job is to **read all your PDF reports, chop them into small chunks of text, generate AI embeddings, and save them into a Chroma database** so you can later query them with an LLM.

Ingestion (one-time)
--------------------
![ingest](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/ingestion.png)
   
This script **turns your PDFs into a searchable database** by chopping them into small pieces, converting them into AI-friendly vectors, and storing them in Chroma. Later, you can use this database to **ask questions across all your PDFs** instead of reading them manually.

[Source code for ingest.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/ingest.py) 

I did this experiment on publicly available annual reports from 2015-2024

## Topics Across 10 Years <a name="tech2"></a>
After clustering 10 years of reports, here are the most common recurring themes -

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
    
Most of these are expected for a major bank: customer service, financial performance, and regulatory matters dominate. The most interesting theme for me was CEO Transition and Leadership Strategy, which shows up strongly even though leadership changes are relatively rare.

[Source code for topics.py](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/topics.py)

This script takes all the AI-embedded chunks from your reports, groups them into clusters of related content, then uses GPT to give each cluster a human-readable topic name. Finally, it shows you the top recurring themes across the reports.

## Querying with the Business Model Canvas<a name="tech3"></a>
This script builds a Q&A app for your annual reports.You ask a business question (freeform or guided by BMC blocks).
It searches the last 10 years of reports. GPT summarizes the findings into a clean, source-cited answer. The streamlit interface looks like below -

![query](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/query.png)



## Business Model Canvas<a name="business"></a>
The Business Model Canvas (BMC) is a strategic management tool that helps you visualize, design, and analyze a company’s business model. Created by Alexander Osterwalder, it breaks a business down into nine building blocks that capture how the organization creates, delivers, and captures value.

![bmc](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/bmc.PNG)

I have highlighted sample questions and responses across all the 9 areas of the business model canvas below

### Customer Segments <a name="customer"></a>
> **Who are the company’s main customer groups?**
> Based on the provided context, the company's main customer groups are geographically segmented, with the majority of revenue coming from Australia and New  Zealand. Specifically, Australia consistently contributes the largest portion of revenue, ranging from 78.6% to 87.3% over the years 2013 to 2022 [S1, S4, S6]. New Zealand is the second-largest geographic segment, contributing between 11.3% and 19.5% of revenue during the same period [S1, S4, S6]. There is also a smaller segment labeled "Other overseas," which contributes a minor portion of the revenue [S1, S4]. Additionally, the company has a substantial number of total customers, with figures ranging from 12.7 million to 14.2 million over the years 2014 to 2022 [S2, S3, S5]. A significant portion of these customers are digitally active, indicating a focus on digital engagement [S2, S3, S5]. However, no single customer accounts for more than 10% of the company's revenue, suggesting a diverse customer base [S1, S4, S6].

> **Have the customer priorities changed over time?**
> Based on the context provided, there is limited information specifically addressing changes in customer priorities over the last 10 fiscal years (2013–2022). However, some insights can be inferred from the data on customer behavior and company operations:
Increase in Digitally Active Customers: From 2014 to 2018, there was a noticeable increase in the number of digitally active customers, rising from 4.7 million in 2014 to 5.6 million in 2018 [S2, S3]. This suggests a shift in customer priorities towards digital engagement and online services.
Decrease in Physical Branches: During the same period, the number of branches decreased from 1,534 in 2014 to 1,204 in 2018 [S2, S3]. This reduction in physical branches could indicate a response to changing customer preferences, with more customers opting for digital interactions over in-person visits.
These trends suggest a shift in customer priorities towards digital services and away from traditional branch-based interactions. However, without additional data from 2019 to 2022, it is difficult to provide a comprehensive analysis of customer priority changes over the entire 10-year period.

### Value Propositions <a name="valprops"></a>
> **How does the company claim to solve customer problems?**
> The company claims to solve customer problems by improving the management of customer complaints and addressing root cause issues. They have implemented several initiatives, such as complaints skilling sessions for bankers to focus on first point resolution, updating their Complaints Management Standard, and making information more accessible. These efforts have led to significant improvements, including reducing the average time to resolve complaints, decreasing the number of long-dated complaints, and increasing the percentage of complaints solved on the same day. Additionally, insights from better complaint management have led to process improvements that reduce pain points for customers [S1][S2][S3].

>**Customer value**
>The context provided does not include specific information on customer value for the last 10 fiscal years (2013–2022). However, it does provide some data on customer metrics for a subset of those years:
Total customers increased from 12.9 million in 2014 to 14.2 million in 2018 [S3, S5].
Digitally active customers grew from 4.7 million in 2014 to 5.6 million in 2018 [S3, S5].
The number of branches decreased from 1,534 in 2014 to 1,204 in 2018 [S3, S5].
These metrics suggest a trend towards digital engagement with customers, as the number of digitally active customers increased while the number of physical branches decreased. This shift could imply an increased focus on digital customer value over the years. However, without more detailed financial or qualitative data on customer value, a comprehensive analysis cannot be provided based on the given context.

### Channels <a name="Channels"></a>
>**How does the company deliver products or services to customers?**
> The company delivers products or services to customers through a combination of physical branches and digital platforms. Over the last ten fiscal years, there has been a noticeable trend towards digital engagement, as evidenced by the increase in digitally active customers from 4.7 million in 2014 to 5.6 million in 2018 [S1 2018.pdf p.134]. Despite this digital shift, the company still maintains a significant number of physical branches, although the number has decreased from 1,534 in 2014 to 1,204 in 2018 [S1 2018.pdf p.134]. This indicates a dual approach to delivering services, balancing between traditional branch-based services and digital platforms to cater to a broad customer base.

## Conclusion <a name="conclusion"></a>
**Conclusion**
This experiment demonstrates how AI and structured frameworks like the Business Model Canvas can transform raw annual reports into actionable insights. By combining PDF ingestion, embeddings, and LLM-powered analysis, I was able to extract recurring themes, map strategic priorities, and answer targeted business questions across a decade of reports.

