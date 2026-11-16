import os
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent ## => New Added

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

## => New Added. Defines the remote agent server.
remote_country_agent = RemoteA2aAgent(
    name="country_agent",
    description="An agent that gives information about the country",
    agent_card=(
        f"http://localhost:8001"
    ),
)

travel_agent = Agent(
    name="travel_agent",
    model="gemini-3.5-flash-lite",
    description=(
        "A smart travel assistant that connects users with specialized sub-agents..."
    ),
    instruction=("""
        You are a travel assistant. When a user’s request relates to flights, bookings, visas, or country-specific information, delegate the conversation to the appropriate sub-agent:
        ...
        country_agent for local information, culture, and travel tips
        """),
    sub_agents=[remote_country_agent]
)

root_agent=travel_agent