# System Architecture

## Version 1 — LLM-led
```mermaid
flowchart TD
    Player --> StreamlitUI[Streamlit chat interface]
    StreamlitUI --> History[Conversation history]
    History --> Gemini[Gemini Game Master]
    Gemini --> StreamlitUI
```
The model interprets player actions and narrates game progress. This is flexible but may forget state or invent outcomes.

## Version 2 — Python-led
```mermaid
flowchart TD
    Player --> UI[Streamlit interface]
    UI --> Parser[Action parser]
    Parser --> Validator[Python rule validator]
    Validator --> State[Structured game state]
    State --> Narration[Validated response]
    Narration --> UI
```
Python decides whether actions are valid and updates state. The response is generated only after validation. This separation reduces hallucinated game progress.
