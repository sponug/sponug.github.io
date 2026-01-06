---
layout: post
title: Fixing Vulnerabilities with Claude Code 
---

# How I Fixed a SQL Injection Vulnerability (Using Claude Code and Systems Thinking)

Most security work looks like this: find vulnerability, patch vulnerability, move on. Repeat until exhausted.

The problem? You're playing whack-a-mole. Fixes don't stick because you never understood *why* the bug existed in the first place.

I used OWASP Juice Shop as a test bed to develop a more systematic approach to vulnerability remediation using Claude Code. Juice Shop is intentionally riddled with security flaws—SQL injection, XSS, broken auth, IDOR, you name it. I wasn't trying to fix all of them. That wasn't the point.

The point was to develop a repeatable framework: a way to approach *any* vulnerability that goes beyond "find bug, patch bug, close ticket."

In this write-up, I'll share:
- A 4-phase framework for systematic vulnerability remediation
- The prompts I used to guide Claude Code through each phase
- How to apply this approach to your own codebase
- Why understanding matters more than coverage

---

## Table of Contents

- [Why Juice Shop?](#why-juice-shop)
- [The goal: a framework, not a fix count](#the-goal-a-framework-not-a-fix-count)
- [A 4-phase framework for security fixes](#a-4-phase-framework-for-security-fixes)
- [Phase 1: Understand the system](#phase-1-understand-the-system)
  - [System Orientation](#system-orientation)
  - [Follow the Data](#follow-the-data)
- [Phase 2: Discover the real problems](#phase-2-discover-the-real-problems)
  - [Convenience vs Correctness](#convenience-vs-correctness)
  - [Hypothesis-Driven Risk](#hypothesis-driven-risk)
- [Phase 3: Make cost-aware decisions](#phase-3-make-cost-aware-decisions)
  - [Cost-Aware Fix](#cost-aware-fix)
  - [What Would Break?](#what-would-break)
- [Phase 4: Verify it's actually fixed](#phase-4-verify-its-actually-fixed)
  - [Apply and Verify](#apply-and-verify)
  - [Measurement](#measurement)
- [What I learned](#what-i-learned)
- [The prompts](#the-prompts)
- [Try it yourself](#try-it-yourself)

---

## Why Juice Shop?

OWASP Juice Shop is a deliberately vulnerable web application. It's designed for security training—every bad practice you can think of is in there somewhere.

That makes it perfect for developing a methodology. I didn't need to hunt for bugs; they're everywhere. Instead, I could focus on *how* to approach one vulnerability end-to-end, knowing the same approach would work on the next one.

I picked SQL injection as my test case. It's well-understood, easy to verify, and common enough that the framework would translate to real-world codebases.

---

## The goal: a framework, not a fix count

Let me be clear about what this is and isn't.

**This is:** A repeatable approach to understanding, fixing, and verifying a vulnerability—demonstrated on one example.

**This is not:** A comprehensive security audit of Juice Shop. There are dozens of vulnerabilities in there. I fixed one. Properly.

Why? Because in real codebases, you rarely have time to fix everything. You need to:
- Prioritize what matters
- Understand root causes
- Make fixes that stick
- Prove they worked

That's what this framework is for.

> The goal isn't to find every bug. It's to fix the ones you find in a way that prevents the same class of bug from coming back.

---

## A 4-phase framework for security fixes

I broke the work into four phases:

| Phase | Goal | Key Questions |
|-------|------|---------------|
| **1. Understand** | Know the system | How does data flow? Where are trust boundaries? |
| **2. Discover** | Find the real problems | What assumptions are violated? What fails silently? |
| **3. Decide** | Make cost-aware fixes | What's the trade-off? What could break? |
| **4. Verify** | Prove it's fixed | How do we know? How do we prevent regression? |

Each phase has specific prompts. The prompts aren't magic—they're a way to be systematic instead of ad-hoc.

Let me walk through how I applied them to the SQL injection vulnerability.

---

## Phase 1: Understand the system

Before looking for bugs, I needed to understand how Juice Shop actually works. This might seem like overkill for a single vulnerability, but it pays off: you start seeing *patterns*, not just individual bugs.

### System Orientation

I started with:

```markdown
Act as a senior engineer performing first-pass system orientation.
Analyze the repository and provide:
- Core user journeys
- Key components
- Data flows
- Trust boundaries
...
```

This gave me a map. I learned that user input enters through REST endpoints, passes through Express middleware, and hits a SQLite database via Sequelize—except in a few places where raw queries are used.

Those raw queries? That's where I'd focus.

### Follow the Data

Next, I traced specific inputs:

```markdown
Pick 2-3 high-risk inputs (login, search, checkout) and map each step:
- Entry point
- Validation
- Transformation
- Usage
- Persistence
```

For the search endpoint, I found: query param → controller → raw SQL string concatenation → database. No parameterization. No escaping.

I didn't need to trace every endpoint. Just enough to understand the pattern.

---

## Phase 2: Discover the real problems

With the system mapped, I looked for patterns—not just individual bugs.

### Convenience vs Correctness

```markdown
Find places where the code chose "easy" over "safe."
Look for:
- Dynamic SQL instead of parameterized queries
- Validation only on frontend
- Overly permissive CORS
...
```

The pattern was clear: raw SQL was used in places where a quick feature was needed. Parameterized queries existed elsewhere—someone knew how to do it right, but didn't always.

This is the insight that matters. It's not "there's a bug on line 42." It's "this codebase has a pattern of using raw SQL when developers are in a hurry."

### Hypothesis-Driven Risk

I then formed specific attack hypotheses:

```markdown
Think like an attacker. What are 3 ways to break this system?
For each:
- Entry point
- Evidence in code
- Impact
- Confidence
```

For SQL injection in search, confidence was high—I could see the string concatenation directly. I didn't need to test every endpoint to know this pattern was exploitable.

---

## Phase 3: Make cost-aware decisions

Finding bugs is easy. Fixing them well is hard.

### Cost-Aware Fix

```markdown
Propose 2-3 fixes ranging from quick patch to proper solution.
For each:
- Risk reduction
- Implementation cost
- Developer impact
- Unintended consequences
```

For the SQL injection, I had three options:

| Option | Cost | Risk Reduction | Trade-off |
|--------|------|----------------|-----------|
| Escape input | 15 min | Medium | Bypass possible |
| Parameterized query | 1-2 hrs | High | Need to update similar queries |
| Move to ORM everywhere | Days | Complete | Big refactor |

I went with parameterized queries—good ROI, standard pattern, no major refactor.

In a real codebase, you'd apply this same analysis. The "right" fix depends on your context, timeline, and risk tolerance.

### What Would Break?

Before applying the fix:

```markdown
If we apply this fix, what could break?
- Backward compatibility
- Performance  
- Developer workflows
- Security trade-offs
```

For this fix, risk was low. But asking the question matters—I've seen "security fixes" that broke production because nobody checked.

---

## Phase 4: Verify it's actually fixed

A fix without verification is just hope.

### Apply and Verify

```markdown
For each file that needs fixing:
- Create a new file with suffix `_new`
- Apply the fix
- Write a test that fails on old code, passes on new
- Log the change to audit.log
```

This gave me:
- `search_new.js` with the parameterized query
- `search_test_new.js` with the attack payload as a test case
- `audit.log` entry documenting what changed

The `_new` suffix pattern keeps the original intact for comparison. In a real project, you'd eventually replace the original and delete the suffix.

### Measurement

```markdown
How do we prove this is fixed—and stays fixed?
- What test cases prove the vulnerability is closed?
- What should we see (or stop seeing) in logs?
- What metrics give us confidence?
```

The test suite now includes the original attack payload. If anyone reintroduces string concatenation, CI fails.

This is the part most teams skip. They fix the bug but don't add the test. Six months later, someone "refactors" the code and reintroduces the same vulnerability.

---

## What I learned

**Depth over breadth.** I fixed one vulnerability properly instead of skimming ten. The framework I developed works on any of them.

**Systems thinking > pattern matching.** Scanners find CVEs. Understanding the system finds *classes* of bugs.

**Prompts are scaffolding, not solutions.** The framework helped me be systematic, but I still had to think. Claude Code accelerated the work—it didn't replace judgment.

**The fix is the easy part.** Understanding why the bug existed, what could break, and how to verify—that's the real work.

**Document everything.** The `audit.log` and `_new` file pattern made it easy to review changes. I'll use this again.

---

## The prompts

I've open-sourced the full prompt set. You don't need to run all 14—pick the ones relevant to your situation.

| # | Prompt | Phase | When to Use |
|---|--------|-------|-------------|
| 1 | [System Orientation](https://gist.github.com/sponug/5211f5fa6f338da9ca24d659875e4b3e#file-system-understanding-md) | Understand | Unfamiliar codebase |
| 2 | [Problem Discovery](https://gist.github.com/sponug/5211f5fa6f338da9ca24d659875e4b3e#file-problem-discovery-md) | Discover | Finding risky shortcuts |
| 3 | [Decision Making](https://gist.github.com/sponug/5211f5fa6f338da9ca24d659875e4b3e#file-decision-making-md) | Decide | Prioritizing what to fix |
| 4 | [Long term](https://gist.github.com/sponug/5211f5fa6f338da9ca24d659875e4b3e#file-long-term-md) | Verify | Proving the fix works |
| 5 | [Audit](https://gist.github.com/sponug/5211f5fa6f338da9ca24d659875e4b3e#file-audit-log) | Verify | what is changing? |

---

## Try it yourself

If you want to practice this approach:

1. Clone [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
2. Pick *one* vulnerability (don't try to fix everything)
3. Run through the 4 phases with the prompts
4. Focus on understanding the system, not just patching the bug

The goal isn't comprehensive coverage. It's building the habit of understanding before fixing—so when you encounter a vulnerability in a real codebase, you have a framework to follow.

---

