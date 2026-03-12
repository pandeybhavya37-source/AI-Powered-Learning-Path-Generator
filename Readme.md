# AI-Powered Learning Path Generator

A lightweight AI-inspired tool that generates personalized learning paths based on:
- your **career goals**,
- your **current skills**,
- and **recommended technologies**.

The generator prioritizes skill gaps, proposes modules with estimated learning hours, and builds week-by-week milestones.

## Quick Start

```bash
python learning_path_generator.py \
  --goals "become data scientist" \
  --skills "python" \
  --tech "docker"
```

## Example Output

```json
{
  "goals": ["become data scientist"],
  "current_skills": ["python"],
  "recommended_technologies": ["docker"],
  "learning_modules": [
    {
      "name": "SQL Basics",
      "level": "beginner",
      "estimated_hours": 10,
      "outcome": "Query relational data with SELECT and JOIN"
    }
  ]
}
```

## Running Tests

```bash
python -m pytest -q
```
