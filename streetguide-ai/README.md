# StreetGuide AI

A multi-agent application that analyzes street sign images, extracts visible text via OCR, transliterates it into a target language, and provides navigation-related guidance — built with **Google ADK**, **FastAPI**, and **Gemini 2.5 Flash**.

---

## Overview

StreetGuide AI helps travelers and residents understand street signs written in unfamiliar scripts. Upload a photo of a street sign, and the pipeline will:

1. Validate the image and extract the visible text (OCR)
2. Detect the source language and transliterate the text into your target language

---

## Architecture

```
User Uploads Image
        │
        ▼
   Vision Agent          → validates image, extracts OCR text
        │
        ▼
Text Processing Agent     → detects language, transliterates text
        │
        ▼
   FastAPI Response  →  Frontend
```

The two agents run as a Google ADK `SequentialAgent` workflow, each writing its output into shared session state via `output_key`.

> **Note:** A Navigation Agent (sign classification / navigation guidance) exists in the codebase but is currently **not part of the active pipeline**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI |
| Agent orchestration | Google ADK (Agent Development Kit) |
| LLM | Gemini 2.5 Flash |
| Session management | ADK `InMemorySessionService` |
| Frontend | HTML / CSS / vanilla JavaScript |

---

## Project Structure

```
streetguide-ai/
├── agents/
│   ├── core/                 # Session/runner core utilities, callbacks
│   ├── models/                # Pydantic schemas for structured agent output
│   ├── prompts/               # Agent instruction prompts (.md files)
│   │   ├── vision.md
│   │   ├── text_processing.md
│   │   ├── navigation.md
│   │   ├── language.md
│   │   └── transliteration.md
│   ├── sub_agents/            # Individual agent definitions
│   │   ├── vision_agent.py
│   │   ├── text_processing_agent.py
│   │   ├── navigation_agent.py   # present but not wired into the active workflow
│   │   └── language_agent.py
│   ├── tools/                  # Function tools (image validation, navigation classifier)
│   ├── workflow/
│   │   └── sequential_workflow.py   # SequentialAgent pipeline (Vision + Text Processing)
│   └── agent.py                # root_agent entry point
├── app/
│   ├── adk_runner.py           # Wraps ADK Runner + session lifecycle
│   ├── config.py               # App configuration (e.g. USE_MOCK)
│   ├── main.py                  # FastAPI app entry point
│   ├── mocks.py                 # Mock responses for offline/UI development
│   ├── parsers/
│   │   └── workflow_parser.py   # Parses ADK session state into API response shape
│   ├── routes.py                # API route definitions
│   ├── schemas.py               # Pydantic response models
│   └── services.py              # Orchestrates the ADK run + response building
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── js/api.js
├── uploads/                     # Uploaded image storage
├── sample_images/                # Example street sign images for testing
├── tests/
├── requirements.txt
├── .env                          # API keys (not committed)
└── README.md
```

---

## Prerequisites

- Python 3.11+
- A Google AI Studio account with a Gemini API key
- (Recommended) A dedicated Google Cloud project for this app, to keep its API quota isolated

---

## Setup

1. **Clone the repository and create a virtual environment**

   ```bash
   git clone <repo-url>
   cd streetguide-ai
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   > Get your key from [Google AI Studio](https://aistudio.google.com). Rate limits and quotas are tied to the **Google Cloud project**, not the individual key — see [Known Limitations](#known-limitations) below.

4. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

   The app will be available at `http://127.0.0.1:8000`.

---

## API

### `POST /process-image`

Uploads a street sign image and runs it through the full agent pipeline.

**Request:** `multipart/form-data`
| Field | Type | Description |
|---|---|---|
| `image` | file | The street sign image |
| `source_language` | string | Language of the sign text |
| `target_language` | string | Language to transliterate into |

**Response:**

```json
{
  "success": true,
  "processing_time": 6.4,
  "ocr_text": "சென்னை\nமாநகராட்சி",
  "language": "Tamil",
  "transliterated_text": "Chennai\nMaanagaratchi",
  "agent_status": {
    "vision": "completed",
    "text_processing": "completed"
  }
}
```

On failure or partial completion (e.g. quota exhaustion mid-pipeline), the endpoint still returns `200` with whatever data was successfully processed.

---

## Development Mode (Mock Responses)

To develop or test the frontend without burning Gemini API quota, enable mock mode in `app/config.py`:

```python
USE_MOCK = True
```

This returns a canned response from `app/mocks.py` instead of running the real agent pipeline.

---

## Known Limitations

- **Gemini free-tier quota is tight for a multi-agent pipeline.** Each agent (in ADK task-mode) requires roughly two model turns to complete, so even the current two-agent pipeline can use 4+ calls per request — easy to exceed a 5 RPM free-tier ceiling. Recommended: enable billing on your Google Cloud project for reliable operation, or space out test requests by 60–90 seconds.
- **Rate limits and daily quotas are tied to the Google Cloud project**, not the API key. Generating a new key in the same project does not reset quota; a new project is required for a fresh allocation.
- **ADK's experimental task-mode (`mode="task"`) output wiring is unreliable** in some ADK versions — the auto-injected `finish_task` tool does not always trigger a `state_delta` the way the standard `output_key` mechanism does for plain text responses. This project works around it with a manual `after_tool_callback` (see `agents/core/callbacks.py`) that captures `finish_task`'s arguments directly into session state.
- The shape of `finish_task`'s arguments can vary between runs (structured fields directly, or wrapped in a single `result` key containing a JSON string). Both shapes are normalized in the callback and in the state parser.

---

## Troubleshooting

| Symptom | Likely Cause |
|---|---|
| `429 RESOURCE_EXHAUSTED` in logs | Gemini API quota exhausted — check [ai.dev/rate-limit](https://ai.dev/rate-limit) for your project |
| UI shows "No OCR text" / "No transliteration" | Either quota was hit mid-run, or session state wasn't captured correctly — check terminal logs for `state_delta` output |
| `ResponseValidationError` from FastAPI | Should not occur with current schema defaults; if it does, check `app/schemas.py` for missing defaults |
| Frontend status pills show "Completed" regardless of actual outcome | Status pills may be hardcoded rather than reading `agent_status` from the API response — check `frontend/script.js` |
| Frontend still shows a "Navigation Agent" / "Navigation Guidance" panel | The frontend UI has not yet been updated to remove Navigation Agent references now that it's excluded from the backend workflow |

---

## Roadmap / Next Steps

- [ ] Migrate to `DatabaseSessionService` for persistent, queryable session state
- [ ] Add automated tests covering agent output shapes
- [ ] Move off free-tier Gemini quota for production use
- [ ] Wire `agent_status` fully into the frontend status indicators
- [ ] Decide whether to re-integrate Navigation Agent into the active workflow or remove it from the codebase entirely
- [ ] Update frontend to remove Navigation Agent UI panel if it will remain unused

---

