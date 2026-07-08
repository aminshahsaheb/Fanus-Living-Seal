# Fanus API Documentation

Base URL: https://web-production-924a5.up.railway.app

## Core Endpoints

GET /          - Status check
GET /status    - Cognitive state
POST /chat     - Main chat (requires X-API-Key header)

## Demo Endpoints (No Auth)

POST /demo/chat   - Public demo, 10 req/hour
GET /demo/status  - Public status

## Knowledge Endpoints

POST /knowledge/search    - Search 6 sources
POST /knowledge/validate  - Validate a claim

## Reasoning Endpoints

POST /reason/analyze     - Detect Negar
POST /reason/contradict  - Check contradictions
POST /reason/hypothesize - Generate questions

## Memory Endpoints

POST /memory/store   - Store claim
GET /memory/ledger   - Last 20 entries
GET /memory/beliefs  - Belief stats

## Decision Endpoints

POST /decision/goal    - Add goal
GET /decision/goals    - Active goals
GET /decision/governance - Autonomy state

## Automation

POST /auto/research - Run research cycle

## Response Fields

negar: bool         - Flattery detected
hayrat_score: float - Epistemic humility (0-1)
fi_score: int       - Flattery index (0-3)
mode: str           - Cognitive mode
stability: float    - System stability (0-1)
sources: int        - Knowledge sources used
