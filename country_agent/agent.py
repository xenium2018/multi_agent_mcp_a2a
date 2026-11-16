import os

from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from .instructions import country_agent_instruction, exchange_agent_instruction

tool_set = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://localhost:8002/mcp"  ## => Our MCP Server
    ),
)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

exchange_agent = Agent(
    name="exchange_agent",
    model="gemini-3.5-flash-lite",
    description=("An agent that gives information about the exchange rates"),
    instruction=exchange_agent_instruction,
    tools=[tool_set],
)

country_agent = Agent(
    name="country_agent",
    model="gemini-3.5-flash-lite",
    description="An agent that provides information about the country",
    instruction=country_agent_instruction,
    tools=[tool_set],
    sub_agents=[exchange_agent],
)

root_agent = country_agent

country_agent_server=to_a2a(root_agent,port=8001)
# We have to define it as a root agent.
