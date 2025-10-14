# Career Agent with Memory

This project contains a sophisticated AI-powered career agent designed to provide personalized career recommendations. The agent interacts with users to understand their skills, interests, and desired work location, and then uses this information to generate a tailored career plan.

## Features

- **Personalized Career Advice:** The agent asks users for their skills, interests, and desired location to provide relevant career suggestions.
- **Real-time Job Market Data:** It uses Google Search to find up-to-date information on job prospects for specific careers in given locations.
- **Long-Term Memory:** The agent remembers previous interactions to provide a more personalized and continuous experience. If you have a conversation with the agent, it will remember the context for next time.
- **Multi-Agent Architecture:** The system uses a root agent to interact with the user and a dedicated sub-agent for performing web searches, separating concerns and improving reliability.

## How It Works

The career agent is built using a multi-agent architecture:

1.  **Root Agent (`career_advisor_agent_memory`):** This is the primary agent that interacts with the user. It's responsible for:
    - Gathering user information (skills, interests, location).
    - Orchestrating the workflow.
    - Synthesizing information to create a comprehensive career plan.
    - It uses the powerful `gemini-2.5-pro` model for reasoning and planning.

2.  **Search Agent (`career_search_agent_memory`):** This is a specialized sub-agent that is invoked by the root agent. Its sole purpose is to:
    - Search for career options in a specific city or country using Google Search.
    - It uses the `gemini-2.5-flash` model, which is optimized for search-related tasks.

3.  **Memory:** The agent uses the `VertexAiMemoryBankService` to store and retrieve information from past conversations. This allows the agent to have a long-term memory and provide a more contextual and personalized experience over multiple sessions.

## Technology Stack

- **Python:** The core language for the agent's logic.
- **Google ADK (Agent Development Kit):** The framework used to build and orchestrate the agents.
- **Google Vertex AI:** Provides the backend for session management and long-term memory.
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs, which is likely used to serve the agent.
