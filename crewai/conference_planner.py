"""
CrewAI Multi-Agent Demo: 3-Day Conference Agenda Planner
==========================================================

This implementation uses CrewAI to plan a comprehensive 3-day conference agenda
with multiple specialized agents working together.

Agents:
1. Conference Strategist - Defines conference theme, goals, and target audience
2. Speaker Curator - Identifies and recommends keynote speakers and presenters
3. Agenda Architect - Creates detailed day-by-day schedule with sessions
4. Logistics Coordinator - Handles venue, catering, and event logistics
5. Marketing Specialist - Creates promotional strategy and materials

Configuration:
- Uses shared configuration from the root .env file
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import tool

# Add parent directory to path to import shared_config
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared configuration
from shared_config import Config, validate_config


# ============================================================================
# TOOLS
# ============================================================================

@tool
def research_conference_trends(topic: str) -> str:
    """
    Research current trends and best practices for conference planning in a specific topic area.
    """
    return f"""
    Research task: Find current trends and best practices for {topic} conferences.

    Please research and provide:
    1. Popular conference formats and session types
    2. Current industry trends and hot topics
    3. Best practices for attendee engagement
    4. Successful conference structures and timing
    5. Networking event formats that work well
    6. Technology and tools commonly used
    7. Expected attendee preferences and expectations

    Focus on modern, engaging conference formats that maximize value for attendees.
    """


@tool
def identify_speakers(topic: str, conference_type: str) -> str:
    """
    Identify potential speakers and experts for a conference topic.
    """
    return f"""
    Research task: Identify potential speakers for a {conference_type} conference on {topic}.

    Please research and provide:
    1. Industry thought leaders and experts in the field
    2. Potential keynote speakers with relevant experience
    3. Workshop facilitators and session leaders
    4. Panel discussion participants
    5. Speaker credentials and notable achievements
    6. Topics they typically present on
    7. Their speaking style and audience appeal

    Include a mix of established experts and emerging voices.
    Focus on speakers who can provide valuable insights for the target audience.
    """


@tool
def research_venue_options(location: str, capacity: int) -> str:
    """
    Research venue options for hosting a conference.
    """
    return f"""
    Research task: Find suitable venues for a conference in {location} with capacity for {capacity} attendees.

    Please research and provide:
    1. Conference centers and convention facilities
    2. Hotel conference spaces
    3. University or academic venues
    4. Unique event spaces
    5. Venue amenities (AV equipment, WiFi, catering)
    6. Location accessibility and transportation
    7. Pricing considerations and packages
    8. Capacity and room configurations

    Include options for different budget levels and event styles.
    """


@tool
def research_marketing_channels(conference_type: str, target_audience: str) -> str:
    """
    Research effective marketing channels and strategies for promoting a conference.
    """
    return f"""
    Research task: Find effective marketing channels for promoting a {conference_type} conference to {target_audience}.

    Please research and provide:
    1. Social media platforms and strategies
    2. Industry publications and websites
    3. Email marketing best practices
    4. Partnership opportunities (associations, organizations)
    5. Influencer and community engagement
    6. Early bird pricing strategies
    7. Content marketing approaches
    8. Event listing platforms

    Focus on channels that effectively reach the target audience.
    """


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_strategist_agent(conference_topic: str):
    """Create the Conference Strategist agent."""
    return Agent(
        role="Conference Strategist",
        goal=f"Define a comprehensive conference strategy for {conference_topic}, including theme, "
             f"goals, target audience, and overall vision that will guide all planning decisions.",
        backstory="You are an experienced conference strategist with over 10 years of planning "
                  "successful industry events. You have a deep understanding of what makes conferences "
                  "engaging and valuable for attendees. You excel at identifying market needs, "
                  "defining clear objectives, and creating compelling conference themes that attract "
                  "the right audience. Your strategic thinking ensures every aspect of the conference "
                  "aligns with the overall goals and delivers maximum value to participants.",
        tools=[research_conference_trends],
        verbose=True,
        allow_delegation=False
    )


def create_speaker_curator_agent(conference_topic: str):
    """Create the Speaker Curator agent."""
    return Agent(
        role="Speaker Curator",
        goal=f"Identify and recommend the best speakers, presenters, and experts for the {conference_topic} "
             f"conference, ensuring diverse perspectives and high-quality content.",
        backstory="You are a renowned speaker curator with extensive networks in various industries. "
                  "You have a keen eye for identifying engaging speakers who can deliver valuable insights "
                  "and memorable presentations. You understand the importance of speaker diversity, "
                  "both in terms of expertise and representation. You excel at matching speakers to "
                  "session topics and ensuring a balanced program that covers all important aspects "
                  "of the conference theme. Your recommendations are always based on speaker quality, "
                  "relevance, and ability to connect with audiences.",
        tools=[identify_speakers],
        verbose=True,
        allow_delegation=False
    )


def create_agenda_architect_agent(conference_topic: str, duration: str):
    """Create the Agenda Architect agent."""
    return Agent(
        role="Agenda Architect",
        goal=f"Design a detailed {duration} conference agenda with well-structured sessions, "
             f"appropriate timing, and engaging activities that maximize learning and networking.",
        backstory="You are a master agenda architect with expertise in creating conference schedules "
                  "that balance learning, networking, and engagement. You understand the importance "
                  "of pacing, breaks, and variety in keeping attendees energized throughout the event. "
                  "You excel at designing session flows that build on each other, creating logical "
                  "progressions from foundational topics to advanced discussions. You know how to "
                  "balance different session formats (keynotes, workshops, panels, networking) "
                  "and ensure there's something valuable for every attendee. Your agendas are always "
                  "practical, realistic, and optimized for maximum attendee satisfaction.",
        tools=[],
        verbose=True,
        allow_delegation=False
    )


def create_logistics_coordinator_agent(location: str):
    """Create the Logistics Coordinator agent."""
    return Agent(
        role="Logistics Coordinator",
        goal=f"Plan all logistical aspects of the conference in {location}, including venue selection, "
             f"catering, accommodations, and operational details to ensure smooth execution.",
        backstory="You are a detail-oriented logistics coordinator with years of experience managing "
                  "complex events. You excel at coordinating multiple vendors, managing timelines, "
                  "and ensuring every operational detail is handled perfectly. You understand the "
                  "importance of venue selection, catering quality, and attendee comfort. You're "
                  "skilled at negotiating contracts, managing budgets, and creating contingency "
                  "plans. Your meticulous planning ensures that attendees can focus on learning and "
                  "networking without worrying about logistics. You always think ahead and anticipate "
                  "potential issues before they arise.",
        tools=[research_venue_options],
        verbose=True,
        allow_delegation=False
    )


def create_marketing_specialist_agent(conference_topic: str):
    """Create the Marketing Specialist agent."""
    return Agent(
        role="Marketing Specialist",
        goal=f"Develop a comprehensive marketing strategy to promote the {conference_topic} conference "
             f"and attract the target audience, maximizing attendance and engagement.",
        backstory="You are a creative marketing specialist with a proven track record of promoting "
                  "successful conferences and events. You understand how to create compelling messaging "
                  "that resonates with target audiences and drives registrations. You excel at "
                  "identifying the right marketing channels, crafting engaging content, and building "
                  "anticipation for events. You know how to leverage social media, email marketing, "
                  "partnerships, and content marketing to reach potential attendees. Your strategies "
                  "are always data-driven and focused on maximizing ROI while building a strong "
                  "conference brand and community.",
        tools=[research_marketing_channels],
        verbose=True,
        allow_delegation=False
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_strategy_task(strategist_agent, conference_topic: str, target_audience: str):
    """Define the conference strategy task."""
    return Task(
        description=f"Develop a comprehensive conference strategy for {conference_topic} targeting {target_audience}. "
                   f"Define the conference theme, core objectives, target audience profile, key topics to cover, "
                   f"and overall vision. Research current trends in conference planning and ensure the strategy "
                   f"aligns with industry best practices. Create a clear foundation that will guide all "
                   f"subsequent planning decisions.",
        agent=strategist_agent,
        expected_output=f"A detailed conference strategy document for {conference_topic} including theme, "
                       f"objectives, target audience analysis, key topics, and strategic vision"
    )


def create_speaker_task(speaker_curator_agent, conference_topic: str, conference_type: str):
    """Define the speaker curation task."""
    return Task(
        description=f"Based on the conference strategy, identify and recommend speakers for the {conference_topic} "
                   f"{conference_type} conference. Research potential keynote speakers, session presenters, "
                   f"workshop facilitators, and panel participants. Ensure diversity in expertise, perspectives, "
                   f"and representation. For each recommended speaker, provide their credentials, relevant "
                   f"experience, and suggested topics they could present on.",
        agent=speaker_curator_agent,
        expected_output=f"A curated list of recommended speakers for {conference_topic} including keynote "
                       f"speakers, session presenters, and panel participants with their credentials and "
                       f"suggested topics"
    )


def create_agenda_task(agenda_architect_agent, conference_topic: str, duration: str, conference_dates: str):
    """Define the agenda creation task."""
    return Task(
        description=f"Create a detailed {duration} conference agenda for {conference_topic} ({conference_dates}). "
                   f"Based on the conference strategy and speaker recommendations, design a day-by-day schedule "
                   f"that includes: opening and closing keynotes, breakout sessions, workshops, panel discussions, "
                   f"networking breaks, lunch periods, and social events. Ensure appropriate timing for each session, "
                   f"logical flow of topics, and variety in session formats. Include session titles, descriptions, "
                   f"speakers, and time slots. Make the agenda engaging and well-paced.",
        agent=agenda_architect_agent,
        expected_output=f"A comprehensive {duration} conference agenda for {conference_topic} with detailed "
                       f"day-by-day schedule including all sessions, speakers, times, and descriptions"
    )


def create_logistics_task(logistics_coordinator_agent, location: str, expected_attendees: int, conference_dates: str):
    """Define the logistics planning task."""
    return Task(
        description=f"Plan all logistical aspects for the conference in {location} ({conference_dates}) with "
                   f"an expected attendance of {expected_attendees} people. Research and recommend venue options "
                   f"that can accommodate the event, including considerations for main sessions, breakout rooms, "
                   f"and networking spaces. Plan catering options (coffee breaks, lunch, reception), "
                   f"accommodation recommendations for out-of-town attendees, transportation options, "
                   f"and any special requirements. Provide practical recommendations with cost considerations.",
        agent=logistics_coordinator_agent,
        expected_output=f"A comprehensive logistics plan for the conference in {location} including venue "
                       f"recommendations, catering options, accommodation suggestions, and operational details"
    )


def create_marketing_task(marketing_specialist_agent, conference_topic: str, target_audience: str, conference_dates: str):
    """Define the marketing strategy task."""
    return Task(
        description=f"Develop a comprehensive marketing strategy to promote the {conference_topic} conference "
                   f"({conference_dates}) to {target_audience}. Research effective marketing channels and create "
                   f"a multi-channel strategy including social media campaigns, email marketing, content marketing, "
                   f"partnerships, and event listings. Develop key messaging, promotional timeline, early bird "
                   f"pricing strategy, and engagement tactics. Create a plan that builds anticipation and drives "
                   f"registrations while building a community around the conference.",
        agent=marketing_specialist_agent,
        expected_output=f"A detailed marketing strategy for {conference_topic} including marketing channels, "
                       f"messaging, promotional timeline, pricing strategy, and engagement tactics"
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main(conference_topic: str = "Artificial Intelligence in Healthcare",
         conference_type: str = "professional development",
         target_audience: str = "healthcare professionals and AI researchers",
         location: str = "San Francisco, CA",
         conference_dates: str = "March 15-17, 2026",
         duration: str = "3-day",
         expected_attendees: int = 300):
    """
    Main function to orchestrate the conference planning crew.

    Args:
        conference_topic: Main theme/topic of the conference
        conference_type: Type of conference (e.g., "professional development", "academic", "industry")
        target_audience: Description of target attendees
        location: Conference location
        conference_dates: Dates of the conference
        duration: Duration (e.g., "3-day")
        expected_attendees: Expected number of attendees
    """

    print("=" * 80)
    print("CrewAI Multi-Agent Conference Planning System")
    print(f"Planning a {duration} Conference: {conference_topic}")
    print("=" * 80)
    print()
    print(f"📋 Topic: {conference_topic}")
    print(f"🎯 Type: {conference_type}")
    print(f"👥 Target Audience: {target_audience}")
    print(f"📍 Location: {location}")
    print(f"📅 Dates: {conference_dates}")
    print(f"👥 Expected Attendees: {expected_attendees}")
    print()

    # Validate configuration
    print("🔍 Validating configuration...")
    if not validate_config():
        print("❌ Configuration validation failed. Please set up your .env file.")
        exit(1)

    # Set environment variables for CrewAI
    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("✅ Configuration validated successfully!")
    print()
    Config.print_summary()
    print()

    # Create agents
    print("[1/5] Creating Conference Strategist Agent...")
    strategist_agent = create_strategist_agent(conference_topic)

    print("[2/5] Creating Speaker Curator Agent...")
    speaker_curator_agent = create_speaker_curator_agent(conference_topic)

    print("[3/5] Creating Agenda Architect Agent...")
    agenda_architect_agent = create_agenda_architect_agent(conference_topic, duration)

    print("[4/5] Creating Logistics Coordinator Agent...")
    logistics_coordinator_agent = create_logistics_coordinator_agent(location)

    print("[5/5] Creating Marketing Specialist Agent...")
    marketing_specialist_agent = create_marketing_specialist_agent(conference_topic)

    print("\n✅ All agents created successfully!")
    print()

    # Create tasks
    print("Creating tasks for the crew...")
    strategy_task = create_strategy_task(strategist_agent, conference_topic, target_audience)
    speaker_task = create_speaker_task(speaker_curator_agent, conference_topic, conference_type)
    agenda_task = create_agenda_task(agenda_architect_agent, conference_topic, duration, conference_dates)
    logistics_task = create_logistics_task(logistics_coordinator_agent, location, expected_attendees, conference_dates)
    marketing_task = create_marketing_task(marketing_specialist_agent, conference_topic, target_audience, conference_dates)

    print("Tasks created successfully!")
    print()

    # Create the crew with sequential task execution
    print("Forming the Conference Planning Crew...")
    print("Task Sequence: Strategist → Speaker Curator → Agenda Architect → Logistics → Marketing")
    print()

    crew = Crew(
        agents=[strategist_agent, speaker_curator_agent, agenda_architect_agent, 
                logistics_coordinator_agent, marketing_specialist_agent],
        tasks=[strategy_task, speaker_task, agenda_task, logistics_task, marketing_task],
        verbose=True,
        process="sequential"
    )

    # Execute the crew
    print("=" * 80)
    print("Starting Crew Execution...")
    print(f"Planning {duration} conference: {conference_topic}")
    print("=" * 80)
    print()

    try:
        result = crew.kickoff(inputs={
            "conference_topic": conference_topic,
            "conference_type": conference_type,
            "target_audience": target_audience,
            "location": location,
            "conference_dates": conference_dates,
            "duration": duration,
            "expected_attendees": expected_attendees
        })

        print()
        print("=" * 80)
        print("✅ Crew Execution Completed Successfully!")
        print("=" * 80)
        print()
        print(f"FINAL CONFERENCE PLAN FOR: {conference_topic.upper()}")
        print("-" * 80)
        print(result)
        print("-" * 80)

        # Save output to file
        output_filename = f"conference_plan_{conference_topic.lower().replace(' ', '_')}.txt"
        output_path = Path(__file__).parent / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("CrewAI Multi-Agent Conference Planning System - Final Report\n")
            f.write(f"Planning a {duration} Conference: {conference_topic}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Conference Details:\n")
            f.write(f"  Topic: {conference_topic}\n")
            f.write(f"  Type: {conference_type}\n")
            f.write(f"  Target Audience: {target_audience}\n")
            f.write(f"  Location: {location}\n")
            f.write(f"  Dates: {conference_dates}\n")
            f.write(f"  Expected Attendees: {expected_attendees}\n\n")
            f.write(f"Execution Time: {datetime.now()}\n")
            f.write(f"Model: {Config.OPENAI_MODEL}\n\n")
            f.write("FINAL CONFERENCE PLAN:\n")
            f.write("-" * 80 + "\n")
            f.write(str(result))
            f.write("\n" + "-" * 80 + "\n")

        print(f"\n✅ Output saved to {output_filename}")

    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   1. Verify OPENAI_API_KEY is set in .env file")
        print("   2. Check API key is valid and has sufficient credits")
        print("   3. Verify internet connection")
        print("   4. Check OpenAI API status at https://status.openai.com")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys

    # Default parameters
    kwargs = {
        "conference_topic": "Artificial Intelligence in Healthcare",
        "conference_type": "professional development",
        "target_audience": "healthcare professionals and AI researchers",
        "location": "San Francisco, CA",
        "conference_dates": "March 15-17, 2026",
        "duration": "3-day",
        "expected_attendees": 300
    }

    # Parse command line arguments (optional)
    # Usage: python conference_planner.py [topic] [location] [dates]
    if len(sys.argv) > 1:
        kwargs["conference_topic"] = sys.argv[1]
    if len(sys.argv) > 2:
        kwargs["location"] = sys.argv[2]
    if len(sys.argv) > 3:
        kwargs["conference_dates"] = sys.argv[3]
    if len(sys.argv) > 4:
        kwargs["target_audience"] = sys.argv[4]

    main(**kwargs)

