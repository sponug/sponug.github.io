---
layout: post
title: My First Agent
---

Page to hold the weekly progress made on the blog

# Table of contents
1. [Goals](#goals)
2. [Pre-requisites](#prereqs)
3. [Problem](#problem)
4. [Why it matters](#why)
5. [Story Evaluation](#eval)
6. [Solution Approach](#sol)
7. [Implementation](#implementation)

## Goals of This Exercise <a name="goals"></a>
This project was my **first attempt at building an agent**. The primary goals were:

1. **Learn to work with basic "vibe" coding** – focus on getting something functional rather than over-engineered.
2. **Build the most minimal agent possible**:
   - Command-Line Interface (CLI) based  
   - No fancy user interface (UI) or visual components  
   - Keep dependencies minimal  
3. **Integrate with Jira Cloud** to read and update issues via API.
4. **Work within a strict time frame** – complete the entire process, including this write-up, in **4–5 hours**.
5. **Focus on learning over perfection** – prioritize understanding the workflow of creating and testing an agent over building a production-ready tool.

   
## Prerequisites <a name="prereqs"></a>
Before starting, complete the following setup steps:

---

### 1. Get an OpenAI API Key
1. Sign up for an OpenAI account: [https://platform.openai.com/](https://platform.openai.com/).  
2. Choose the **pay-as-you-go** plan.  
3. Preload **$5 credit** to cover API usage for this experiment.  
4. Go to **View API Keys** in your OpenAI dashboard.  
5. Click **Create New Secret Key**, copy it, and store it securely — you’ll need it in your code.

---

### 2. Create a Free Jira Cloud Account
1. Sign up at: [https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free).  
2. Choose **Jira Software (Scrum)** during setup.  
3. Create a new project — for example, `WozProject`.  
4. Create at least one story/issue.  
   - Example: **Story Name:** `Connectivity_Story`  
   - **Issue ID:** `SCRUM-1`

---

### 3. Generate a Jira API Token
1. Go to: [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens).  
2. Click **Create API Token**.  
3. Copy the token and store it securely — you’ll use it with your Jira email for API requests.

---

### 4. Install the `jq` JSON Processor
1. Check if `jq` is already installed by running:  
   ```bash
   jq --version
if not installed run - winget install jqlang.jq

---

### 5. Install Visual Studio Code with Python
Download VS Code: https://code.visualstudio.com/.
Install the Python extension for VS Code from the Extensions Marketplace.
Ensure Python 3.10 or later is installed:

---
## Problem Statement <a name="problem"></a>

In many enterprises, user stories are often written with vague language, missing details, or ambiguous acceptance criteria.  
While these stories may pass initial review, their lack of clarity frequently leads to:
- Misinterpretation by developers and testers
- Misaligned expectations between business and technical teams
- Increased rework and costly delays in delivery

Poorly defined user stories can result in:
- Features that do not meet business needs
- Gaps in test coverage due to unclear acceptance criteria
- Unnecessary churn in sprint planning and backlog refinement

This project explores how even a simple AI-driven agent can help assess user story quality against objective measures, identify weaknesses early, and provide actionable feedback — reducing the risk of costly downstream errors.

## Why This Matters <a name="why"></a>

The quality of user stories directly impacts delivery timelines, development costs, and product quality.  
A single poorly written story can trigger a chain reaction of misunderstandings, rework, and missed deadlines — all of which increase project risk and cost.

By introducing automated story evaluation:
- **Clarity issues** can be caught before sprint commitment.
- **Ambiguous acceptance criteria** can be flagged for refinement.
- **Consistency** in story quality can be maintained across teams and geographies.
- **Data-driven feedback** can help product owners and business analysts improve over time.

---

## Evaluation Criteria <a name="eval"></a>

For this experiment, I had the AI agent evaluated stories against the following key quality dimensions:

1. **Readable** – Is the story and its acceptance criteria easy to understand?  
2. **Testable** – Can the acceptance criteria be verified through testing?  
3. **Implementation Agnostic** – Does the story describe *what* to achieve, not *how* to do it?  
4. **Actionable When Statement** – Are the criteria tied to clear conditions for action?  
5. **Strong Verb Usage** – Are specific, active verbs used instead of vague terms like “should be”?  
6. **Specific to the Story** – Do the criteria directly relate to the story’s scope?  
7. **Tell a Story** – Does the acceptance criteria provide enough context to understand the user’s journey?

Each dimension was scored individually, and the total score provided a quick measure of overall quality, along with targeted improvement suggestions.

## Solution Approach <a name="sol"></a>

To address the problem of substandard user stories, I built a minimal AI-driven agent capable of:
- Reading a Jira story and its acceptance criteria.
- Evaluating the story against predefined quality dimensions.
- Suggesting improvements based on the evaluation.

### Key Design Principles
1. **Simplicity First** – The agent is CLI-based, keeping the UI and dependencies minimal.
2. **Speed of Implementation** – The entire build and documentation process was limited to 4–5 hours.
3. **API-Driven** – The solution relies on Jira's REST API for story retrieval and updates, and OpenAI’s API for evaluation logic.

### High-Level Workflow
1. **Retrieve Story Data** – Connect to Jira Cloud and read the story’s summary and acceptance criteria.
2. **AI Evaluation** – Send the text to the OpenAI API for scoring against the seven quality dimensions.
3. **Improvement Suggestions** – Generate actionable feedback for each dimension.
4. **Optional Update** – Push updated acceptance criteria or comments back into Jira.

![Solution Diagram](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/Solution.png)

## Implementation <a name="implementation"></a>
This Python script is the fourth iteration of a project where I built the functionality step by step, adding each piece incrementally to create a robust tool.

The script:
- Loads environment variables for Jira and OpenAI API credentials securely.
- Fetches a Jira story by its issue key using Jira's REST API.
- Extracts the acceptance criteria description from Jira's rich text format.
- Sends this description to OpenAI’s GPT-4 API to score it on key quality patterns and provide improvement feedback.
- Adds the AI-generated score and feedback as a comment on the Jira issue.
- Includes error handling and user-friendly command-line usage.
- Each iteration introduced new capabilities, making the script more functional and reliable

```
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///

import os
import sys
import requests
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.') / '.env'
print(f"Loading env from {dotenv_path.resolve()}")
load_dotenv(dotenv_path)

# -----------------------------
# Config: Set these as environment variables before running
# -----------------------------
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")  # e.g. "https://yourdomain.atlassian.net"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, OPENAI_API_KEY]):
    print("Error: Missing one or more environment variables: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, OPENAI_API_KEY")
    sys.exit(1)

# -----------------------------
# Jira API Functions
# -----------------------------

def get_jira_story(issue_key: str) -> Dict:
    """Fetch Jira story data."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers, auth=auth)
    r.raise_for_status()
    return r.json()

def update_jira_story_comment(issue_key: str, comment: str):
    """Add a comment to the Jira story."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    }
    r = requests.post(url, headers=headers, auth=auth, json=payload)
    r.raise_for_status()


# -----------------------------
# Helper to extract plain text from Jira rich text format
# -----------------------------

def extract_text_from_content(content: List[Dict]) -> str:
    text = ""
    for block in content:
        if "content" in block:
            for inner in block["content"]:
                text += inner.get("text", "") + "\n"
    return text

# -----------------------------
# OpenAI API Function
# -----------------------------

def score_description_with_openai(story: str) -> str:
    """Score the story and provide improvement feedback."""

    system_prompt = (
        "You are an expert in software requirements analysis with a focus on agile methodologies. "
        "Evaluate the acceptance criteria for the user story below based on these patterns:\n\n"
        "1. Readable\n2. Testable\n3. Implementation Agnostic\n4. Actionable When Statement\n"
        "5. Strong Verb Usage\n6. Specific to the Story\n7. Tell a Story\n\n"
        "Please provide:\n"
        "- A numeric score from 1 to 10 for each of the seven patterns listed,\n"
        "- A summary of overall score,\n"
        "- Specific suggestions for improvement to make the acceptance criteria better."
        "\n\nAcceptance Criteria:\n"
        f"{story}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4",
        "messages": messages,
        "temperature": 0
    }

    print("Sending acceptance criteria to OpenAI...")
    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# -----------------------------
# Main
# -----------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python jira_score_story.py ISSUE_KEY")
        sys.exit(1)

    issue_key = sys.argv[1]

    try:
        story = get_jira_story(issue_key)
    except requests.HTTPError as e:
        print(f"Failed to fetch Jira issue {issue_key}: {e}")
        sys.exit(1)

    description_field = story["fields"].get("description", "")

    if isinstance(description_field, dict) and "content" in description_field:
        description_text = extract_text_from_content(description_field["content"]).strip()
    elif isinstance(description_field, str):
        description_text = description_field
    else:
        description_text = ""

    if not description_text:
        print(f"No description found for {issue_key}")
        sys.exit(1)

    print(f"Scoring Jira story {issue_key}...")
    score_text = score_description_with_openai(description_text)
    print(f"\nScore & Feedback:\n{score_text}")

    print("\nAdding score and feedback as a comment on the Jira story...")
    try:
        update_jira_story_comment(issue_key, f"### AI Acceptance Criteria Review\n\n{score_text}")
    except requests.HTTPError as e:
        print(f"Failed to update Jira issue {issue_key} comment: {e}")
        sys.exit(1)

    print("Done.")

if __name__ == "__main__":
    main()
