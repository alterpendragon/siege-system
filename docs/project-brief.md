# Siege System - Project Brief

## 1. Mission Statement
Siege System is a video game backlog management tool and recommendation engine. The ultimate architectural vision is a full Web Application and an MCP (Model Context Protocol) server. However, **v1.0.0 focuses strictly on building a foundational backend core.**

## 2. The Problem
Gamers often suffer from "backlog paralysis." They accumulate hundreds of unplayed games across multiple storefronts (Steam, Epic, PlayStation, etc.), lacking a unified, store-agnostic, fast, and local system to track ownership, completion status, and filter what to play next.

## 3. Scope Boundaries (What it is NOT)
* **No Web Interface:** UI is strictly Terminal/CLI. Flask, HTML, and CSS are deferred to v2.0.0.
* **No AI Engine:** Anthropic API integration for recommendations is deferred to later versions.
* **No Cloud/DevOps:** No Docker, Redis, or cloud database hosting. Execution and storage are purely local.

## 4. Success Criteria for v1.0.0
* **CLI Architecture:** A modular Python CLI application that operates locally.
* **API Integration:** Secure and successful integration with the RAWG API, using a `.env` file to protect credentials, fetching accurate game metadata (Title, Genre, Platform).
* **Data Persistence:** Atomic CRUD operations utilizing a local SQLite database.
* **Separation of Concerns:** Codebase logic must be decoupled (database, API client, and CLI interface) to ensure a seamless transition to a Web App in v2.0.0.
* **Robustness:** Graceful error handling for API downtime or invalid user input, preventing unhandled exceptions or database corruption.
