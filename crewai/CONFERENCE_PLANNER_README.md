# Conference Planner - CrewAI Multi-Agent System

## Overview

This is a **CrewAI-based Conference Planning System** that uses 5 specialized agents to plan a comprehensive 3-day conference agenda. This demonstrates Exercise 4: Custom Problem solving with multi-agent systems.

## The Team

| Agent | Role | Responsibility |
|-------|------|----------------|
| **Conference Strategist** | 🎯 Strategy Expert | Defines conference theme, goals, and target audience |
| **Speaker Curator** | 🎤 Speaker Specialist | Identifies and recommends keynote speakers and presenters |
| **Agenda Architect** | 📅 Schedule Designer | Creates detailed day-by-day schedule with sessions |
| **Logistics Coordinator** | 🏢 Event Manager | Handles venue, catering, and operational logistics |
| **Marketing Specialist** | 📢 Promotion Expert | Creates marketing strategy and promotional materials |

## Workflow

```
START: Define conference topic
  ↓
Conference Strategist → Defines theme, goals, target audience
  ↓
Speaker Curator → Identifies recommended speakers
  ↓
Agenda Architect → Creates detailed 3-day schedule
  ↓
Logistics Coordinator → Plans venue, catering, accommodations
  ↓
Marketing Specialist → Develops promotional strategy
  ↓
END: Complete Conference Plan
```

## Quick Start

### Basic Usage

```bash
# Plan a default conference (AI in Healthcare)
python conference_planner.py

# Plan a custom conference
python conference_planner.py "Sustainable Energy Solutions" "Boston, MA" "June 10-12, 2026" "engineers and environmental scientists"
```

### Programmatic Usage

```python
from conference_planner import main

main(
    conference_topic="Machine Learning in Finance",
    conference_type="professional development",
    target_audience="financial analysts and data scientists",
    location="New York, NY",
    conference_dates="April 20-22, 2026",
    duration="3-day",
    expected_attendees=250
)
```

## Example Scenarios

### 1. Technology Conference
```python
main(
    conference_topic="Cloud Computing & DevOps",
    target_audience="software engineers and DevOps professionals",
    location="Seattle, WA",
    conference_dates="May 15-17, 2026",
    expected_attendees=500
)
```

### 2. Academic Conference
```python
main(
    conference_topic="Climate Change Research",
    conference_type="academic",
    target_audience="climate scientists and researchers",
    location="Cambridge, MA",
    conference_dates="September 5-7, 2026",
    expected_attendees=200
)
```

### 3. Industry Conference
```python
main(
    conference_topic="Digital Marketing Trends",
    conference_type="industry",
    target_audience="marketing professionals and business leaders",
    location="Chicago, IL",
    conference_dates="July 8-10, 2026",
    expected_attendees=400
)
```

## Output

The system generates a comprehensive conference plan including:

1. **Conference Strategy** - Theme, objectives, target audience analysis
2. **Speaker Recommendations** - Keynote speakers, presenters, panel participants
3. **Detailed Agenda** - Day-by-day schedule with sessions, times, and descriptions
4. **Logistics Plan** - Venue recommendations, catering, accommodations
5. **Marketing Strategy** - Promotion channels, messaging, timeline

Output is saved to: `conference_plan_[topic].txt`

## Customization

### Change Conference Topic
Modify the `conference_topic` parameter to plan any type of conference:
- "Blockchain Technology"
- "Renewable Energy"
- "Healthcare Innovation"
- "Education Technology"

### Adjust Agent Behavior
Edit agent backstories in the `create_*_agent()` functions to change their expertise and approach.

### Add New Agents
Follow the pattern to add new specialized agents:
- Registration Coordinator
- Content Manager
- Technology Coordinator

## Requirements

- Python 3.8+
- CrewAI framework
- OpenAI API key (set in `.env` file)
- Shared configuration from parent directory

## Notes

- This system uses sequential task execution
- Each agent builds on previous agent outputs
- All agents use real API calls (OpenAI)
- Outputs are saved automatically to text files

