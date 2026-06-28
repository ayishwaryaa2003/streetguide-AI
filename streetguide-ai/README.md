# StreetGuide AI: A Multi-Agent System for Intelligent Street Sign Transliteration and Navigation

Track: Agents for Good

## Overview
StreetGuide AI is an intelligent, multi-agent system designed to assist users in reading, transliterating, and navigating foreign street signs. By leveraging a network of specialized AI agents coordinated by an ADK Orchestrator, the system seamlessly extracts text from images, converts it to the user's preferred language, and provides contextual navigation guidance.

## Architecture

The system follows a modular, agentic workflow:

```text
                 Browser
                    │
                    ▼
              FastAPI Backend
                    │
             ADK Orchestrator
                    │
 ┌──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │
 ▼          ▼          ▼          ▼          ▼
Vision   OCR      Language   Transliteration  Navigation
Agent    Agent      Agent        Agent         Agent
                    │
                    ▼
             Filesystem MCP
                    │
                    ▼
          Scan History Database
                    │
                    ▼
              Google Maps MCP
```

### Components
- **Browser Frontend**: User interface to upload street sign images and receive real-time translation and navigation guidance.
- **FastAPI Backend**: The core API server that handles requests and serves the frontend.
- **ADK Orchestrator**: Manages the flow of information between the specialized agents.
- **Vision Agent**: Analyzes the visual context of the uploaded image.
- **OCR Agent**: Extracts textual data from the street sign.
- **Language Agent**: Identifies the source language of the text.
- **Transliteration Agent**: Transliterates and translates the text to the target language.
- **Navigation Agent**: Interprets the location and provides navigation instructions based on the transliterated sign.
- **Filesystem MCP**: A Model Context Protocol server that maintains a local database/log of scan history.
- **Google Maps MCP**: A Model Context Protocol server that interfaces with Google Maps to enrich navigation data.

## Prerequisites & Installation

To run this project locally, you will need to install the following Python packages. It is recommended to use a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate # On Windows

# Install the required dependencies
pip install fastapi uvicorn pydantic python-multipart
pip install requests

# Additional dependencies for LLM integration (e.g., Google GenAI) and MCPs
# pip install google-genai
# pip install mcp
```

## Getting Started

*(Instructions for starting the API server and configuring the MCPs will be added as the implementation progresses.)*
