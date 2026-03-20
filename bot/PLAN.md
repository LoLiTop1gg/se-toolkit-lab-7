# Telegram Bot Development Plan

## Overview

This document outlines the development plan for building a Telegram bot that interacts with the LMS backend. The bot will support slash commands like `/start`, `/help`, `/health`, `/labs`, and `/scores`, as well as natural language queries processed by an LLM.

## Task 1: Project Scaffold and Test Mode

Create the basic project structure with a testable handler architecture. Handlers are plain Python functions that take command input and return text responses — they have no dependency on Telegram. This allows testing via `--test` mode without connecting to Telegram. The entry point `bot.py` supports `uv run bot.py --test "/command"` which calls handlers directly and prints results to stdout. Configuration is loaded from `.env.bot.secret` using `python-dotenv`.

## Task 2: Backend Integration

Implement real handlers that call the LMS backend API. Create an HTTP client service using `httpx` with Bearer token authentication. Handlers like `/health`, `/labs`, and `/scores` will make actual API calls to fetch data. Error handling ensures that backend failures produce friendly messages instead of crashes. All API URLs and keys come from environment variables.

## Task 3: Intent-Based Natural Language Routing

Add LLM-powered intent routing. When users send plain text (not slash commands), the bot uses an LLM to determine which tool/action to invoke. Each backend endpoint is wrapped as an LLM tool with a description. The LLM reads tool descriptions to decide which to call — description quality matters more than prompt engineering. This enables queries like "what labs are available?" to route to the `/labs` handler.

## Task 4: Containerization and Deployment

Create a Dockerfile for the bot and add it as a service in `docker-compose.yml`. Configure container networking so the bot can reach the backend via service names. Deploy to the VM and document the deployment process. The bot runs alongside the existing backend, sharing the same Docker network.

## Architecture Principles

- **Separation of concerns**: Handlers don't know about Telegram transport
- **Testability**: `--test` mode works without external services
- **Configuration via environment**: No hardcoded URLs or secrets
- **Graceful degradation**: Backend failures don't crash the bot
