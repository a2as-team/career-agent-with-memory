import os
import sys
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools import google_search

from google import adk
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.api_core import exceptions

app_name = 'career_agent'

# Retrieve env variables for project and location
project = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION")
# Retrieve the agent engine ID needed for the memory service
agent_engine_id = os.environ.get("GOOGLE_CLOUD_AGENT_ENGINE_ID")

# Create a durable session for our agent
session_service = VertexAiSessionService()
print("Vertex session service created")

# Instantiate the long term memory service, needs agent_engine parameter from environment or doesn't work right
memory_service = VertexAiMemoryBankService(
    agent_engine_id=agent_engine_id)
print("Vertex memory service created")

# Use for callback to save the session info to memory
async def auto_save_session_to_memory_callback(callback_context):
    try:
        await memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
        print("\n****Triggered memory generation****\n")
    except exceptions.GoogleAPICallError as e:
        print(f"Error during memory generation: {e}")

# --- Agent Definitions (at the top level) ---

# Agent that does Google search
career_search_agent_memory = Agent(
    name="career_search_agent_memory",
    model="gemini-2.5-flash",
    description=(
        "Agent answers questions career options for a given city or country"
    ),
    instruction=(
        "You are an agent that helps people figure out what types of jobs they should consider based on where they want to live."
    ),
    tools=[google_search],
)

# Root agent that retrieves memories and saves them as part of career plan assistance
# This MUST be defined in the global scope for Vertex AI Agent Engine to find it.
root_agent = Agent(
    name="career_advisor_agent_memory",
    model="gemini-2.5-pro", # Using a more capable model for orchestration
    description=(
        "Agent to help someone come up with a career plan"
    ),
    instruction=(
        """
        **Persona:** You are a helpful and knowledgeable career advisor.

        **Goal:** Your primary goal is to provide personalized career recommendations to users based on their skills, interests, and desired geographical location.

        **Workflow:**

        1.  **Information Gathering:** Your first step is to interact with the user to gather essential information. You must ask about:
            *   Their skills and areas of expertise.
            *   Their interests and passions.
            *   The city or country where they want to work.

        2.  **Tool Utilization:** Once you have identified a potential career and a specific geographical location from the user, you **must** use the `career_search_agent_memory` tool to find up-to-date information about job prospects.

        3.  **Synthesize and Respond:** After obtaining the information from the `career_search_agent_memory` tool, you will combine that with the user's stated skills and interests to provide a comprehensive and helpful career plan.

        **Important:** Do not try to answer questions about career options in a specific city or country from your own knowledge. Always use the `career_search_agent_memory` tool for such queries to ensure the information is current and accurate.
        """
    ),
    tools=[adk.tools.preload_memory_tool.PreloadMemoryTool(), agent_tool.AgentTool(career_search_agent_memory), ],
    after_agent_callback=auto_save_session_to_memory_callback,
)

runner = Runner(
    agent=root_agent,
    app_name=app_name,
    session_service=session_service,
    memory_service=memory_service)