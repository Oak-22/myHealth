Instructions for VS Code Agent

Objective

Instructions for Agents to guide them when reformatting Markdown files to maximize readability on GitHub while preserving all existing content. Do not change the meaning of the text—only adjust formatting and structure.

Follow the formatting rules below.

1. Heading Hierarchy

Use a consistent 3-level structure maximum.

# Title (H1)

## Major Sections (H2)

### Subsections (H3)

Rules:
	•	Only one H1 in the document (the title - case study)
	•	All main sections should be H2.
	•	Subsections inside those should be H3.

example: 
# Case Study: Designing a Baseline Image Normalization Pipeline for Heterogeneous Input Conditions

## Executive Summary

## Problem

## Key Constraints

## Architecture

### Pipeline Overview

### Stage 1: Global Luminance Normalization

### Stage 2: Semantic Segmentation (Feature Generation)

### Stage 3: Exemplar-Based Canonical Color Calibration

## Observability & Validation

## Failure Modes & Edge Cases

## Design Tradeoffs

## Results

## System Concepts & Definitions

## Key Design Principles

2. Paragraph Width (Prevent Reader Fatigue)

Wrap lines so that no line exceeds ~90 characters.

Example:

Bad:

Large photo datasets captured across time-of-day variations introduce large exposure and color tone variance which can cause inconsistent results across galleries even when the subject matter is identical.

Good:

Large photo datasets captured across time-of-day variations introduce
significant exposure and color tone variance. This often produces
inconsistent results across galleries even when the subject matter
is identical.

3. Section Spacing

Add whitespace to reduce visual density.

Rules:
	•	One blank line after headings
	•	One blank line between paragraphs
	•	One blank line before bullet lists
	•	One blank line after bullet lists

    Example:

    ## Problem

Large datasets often contain heterogeneous lighting conditions.

Example conditions include:

- midday sunlight
- shaded environments
- evening lighting

4. Bullet Lists (Limit Cognitive Load)

Rules:
	•	Maximum 6 bullets per list
	•	Each bullet should be one short line
	•	Use bullets for enumeration instead of paragraphs

Example:

Lighting variation introduces shifts in:

- exposure
- contrast
- color temperature
- foliage tones
- skin tone rendering

5. Code Blocks for Pipelines and Diagrams

Use triple backticks for:
	•	pipeline diagrams
	•	architecture flow
	•	command examples

    Example:

    ```text
RAW Images (dataset)
   ↓
Global luminance normalization
   ↓
Semantic segmentation (mask generation)
   ↓
Exemplar-based canonical color calibration
```

Use text as the language label.

6. Highlight Important Concepts with Bold

Use bold to emphasize key system ideas.

Example:

This stage establishes a **dataset-wide luminance baseline**.

The segmentation masks act as **precomputed editing regions**.

Do not overuse bold.

7. Use Horizontal Dividers Between Major Sections

Insert horizontal rules between major conceptual sections.

---

Example:

## Pipeline Design

content

---

## Resulting Benefits

8. Add Small Intro Lines for Sections

Each major section should begin with one short orienting sentence.

Example:

## Architecture

The pipeline is composed of two deterministic stages followed by
optional local refinement.

This helps readers scan quickly.

9. Ensure GitHub-Friendly Rendering

Verify:
	•	headings render correctly
	•	diagrams stay aligned
	•	bullet indentation is correct
	•	code blocks use triple backticks
	•	no lines exceed ~90 characters

    12. Final Readability Goal

After formatting, the document should:
	•	be scannable in under 2 minutes
	•	show clear visual hierarchy
	•	avoid large text walls
	•	resemble a technical architecture document

    Optional (Nice Enhancement)

At the top of the file, insert a small metadata block:

Author: Julian Buccat
Date: 2026-02-26
Category: Systems Design Case Study
Domain: Image Processing Pipeline