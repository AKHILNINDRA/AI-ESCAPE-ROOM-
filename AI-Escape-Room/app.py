import os
import streamlit as st
from dotenv import load_dotenv
from game_v1 import reply_v1, initial_history
from game_v2 import initial_state, process_action

load_dotenv()
st.set_page_config(page_title="AI Escape Room", page_icon="🗝️", layout="centered")

st.title("🗝️ The Forgotten Library")
st.caption("An AI-powered escape room — investigate, solve puzzles, and escape.")

mode = st.sidebar.radio("Choose application version", ["Version 1 — AI Game Master", "Version 2 — Reliable Game"])
st.sidebar.markdown("---")
st.sidebar.write("**Objective:** Escape the locked library.")
st.sidebar.write("Explore five objects: desk, bookshelf, painting, drawer and door.")
if st.sidebar.button("Restart game"):
    for key in ("v1_messages", "v1_history", "v2_state", "v2_log"):
        st.session_state.pop(key, None)
    st.rerun()

if mode.startswith("Version 1"):
    st.subheader("Version 1: Natural-language AI")
    st.info("Try commands such as “I examine the bookshelf” or “What do I see?” Version 1 relies heavily on the AI Game Master.")
    if "v1_messages" not in st.session_state:
        st.session_state.v1_messages = [{"role": "assistant", "content": "You wake in a silent library. A desk, bookshelf, painting, locked drawer and heavy exit door surround you. Explore by telling me what you want to do. Your goal is to escape."}]
        st.session_state.v1_history = initial_history()
    for msg in st.session_state.v1_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("What do you want to do?")
    if prompt:
        st.session_state.v1_messages.append({"role": "user", "content": prompt})
        answer = reply_v1(prompt, st.session_state.v1_history)
        st.session_state.v1_messages.append({"role": "assistant", "content": answer})
        st.rerun()
else:
    st.subheader("Version 2: Rule-validated game")
    st.info("Python is authoritative in Version 2. The AI can describe outcomes, but cannot change puzzle results or unlock the door.")
    if "v2_state" not in st.session_state:
        st.session_state.v2_state = initial_state()
        st.session_state.v2_log = [("assistant", "You wake in the Forgotten Library. Examine the bookshelf, desk, painting, drawer and door. Find the drawer code, collect the key, reveal the door code with the UV lamp, and escape.")]
    state = st.session_state.v2_state
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Puzzles solved", f"{sum([state['drawer_unlocked'], state['painting_revealed'], state['door_unlocked']])}/3")
    with col2:
        st.metric("Inventory", ", ".join(state["inventory"]) if state["inventory"] else "Empty")
    st.write("**Game status:**", "🎉 Escaped!" if state["escaped"] else "🔒 Still locked")
    for role, content in st.session_state.v2_log:
        with st.chat_message(role):
            st.markdown(content)
    prompt = st.chat_input("Describe an action (e.g. examine bookshelf)")
    if prompt:
        st.session_state.v2_log.append(("user", prompt))
        result, new_state = process_action(prompt, state)
        st.session_state.v2_state = new_state
        st.session_state.v2_log.append(("assistant", result))
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("For coursework: compare how Version 1 uses the LLM for game decisions, while Version 2 validates every important action in Python.")
