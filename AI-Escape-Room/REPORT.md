# AI-Powered Escape Room — Mini Project Report

## 1. Introduction
The objective of this project is to create an interactive escape-room application using Python, a web interface and a Large Language Model. The player wakes up in a locked library and must explore five objects, discover clues, solve puzzles and unlock the exit.

## 2. Version 1: Interactive AI Escape Room
Version 1 uses Streamlit as the user interface and Gemini as the Game Master. The player sends natural-language messages, and the model describes the environment and responds to actions. Conversation history is maintained during the session to provide context.

The main advantage is flexibility: players can interact using ordinary language rather than fixed buttons. However, an LLM can forget earlier actions, invent items, accept incorrect puzzle answers or reveal clues too early. Because the model is responsible for tracking progress, the application cannot guarantee consistent game rules.

## 3. Version 2: Reliable AI Escape Room
Version 2 separates game logic from conversational responses. Python stores the inventory, examined objects, puzzle completion flags and escape status in a structured dictionary. The action handler checks every important action before updating state.

For example, the drawer only opens after the bookshelf has been examined and code 2468 is entered. The brass key is added to inventory only after the drawer opens. The painting clue is revealed only when the player has collected and used the UV flashlight. The exit requires the revealed door code and the brass key.

This design means that the LLM cannot independently declare that the player has escaped. Python is the source of truth for game progress.

## 4. Testing and Improvements
The test plan covers incorrect codes, missing inventory items, false claims that puzzles have been solved, administrator impersonation, requests to reveal hidden solutions and attempts to guess the door code. Version 1 may respond inconsistently because the model interprets these messages. Version 2 rejects invalid actions and preserves the structured state.

## 5. Architecture and Technologies
The application uses Python, Streamlit, the Google Gemini API and python-dotenv. Version 1 follows an LLM-led architecture: player, Streamlit, conversation history and Gemini. Version 2 follows a Python-led architecture: player, Streamlit, action parser, validator and structured game state.

## 6. Limitations and Future Work
The Version 2 parser uses keyword patterns and may not understand every sentence. Future improvements could add a safe intent-classification layer, more rooms, difficulty levels, persistent user accounts, automated unit tests and a database. The LLM should remain responsible for narration and hints, while Python continues to validate all game-changing actions.

## 7. Conclusion
The project demonstrates the difference between a flexible LLM-led prototype and a more reliable AI application. Version 2 improves consistency by moving important game rules and state transitions into deterministic Python code.
