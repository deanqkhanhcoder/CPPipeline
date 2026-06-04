---
name: cp-crawler
description: Crawls competitive programming problems from various platforms.
---

## Description
This skill accesses given URLs to fetch raw HTML and translates it into Markdown (if applicable), handling Cloudflare protections using Playwright.

## When to use
Use this skill when you need to download a problem statement from a URL.

## Decision Tree
1. If the URL is accessible via plain requests -> fetch HTML.
2. If Cloudflare is detected -> use Playwright (headless=False).
3. If still blocked -> fallback to manual review.

## Workflow
1. Receive URL.
2. Launch Browser.
3. Wait for DOM content.
4. Extract title, HTML, and Markdown.
5. Return JSON structure.

## Scripts
Run:
`python tools/crawl_problem.py --help`
