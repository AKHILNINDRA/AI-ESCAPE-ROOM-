import os

SYSTEM_PROMPT = """
You are the Game Master for a text-based escape room called The Forgotten Library.
The player is trapped in a library with five objects: a desk, bookshelf, painting,
locked drawer and exit door. The player must discover clues, open the drawer, obtain
a brass key, reveal a four-digit door code and escape.
Keep the story engaging and respond to natural-language actions. Remember the
conversation. Do not immediately reveal all solutions. Give hints only when asked.
This is Version 1: you may track progress conversationally; strict Python validation
is intentionally not implemented here so the student can compare it with Version 2.
Puzzle design: bookshelf clues point to drawer code 2468. The desk contains a UV
flashlight. Using it on the painting reveals door code 1357. Drawer 2468 contains
the brass key. The exit requires the brass key and code 1357.
"""

def initial_history():
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def reply_v1(user_text, history):
    history.append({"role": "user", "content": user_text})
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        answer = fallback_reply(user_text)
    else:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            contents = []
            for item in history[1:]:
                contents.append({"role": "user" if item["role"] == "user" else "model", "parts": [{"text": item["content"]}]})
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.7}
            )
            answer = response.text or fallback_reply(user_text)
        except Exception as exc:
            answer = fallback_reply(user_text) + f"\n\n_(Gemini API unavailable: {type(exc).__name__}. Check your API key and internet connection.)_"
    history.append({"role": "assistant", "content": answer})
    return answer

def fallback_reply(text):
    t = text.lower()
    if "bookshelf" in t or "book" in t:
        return "Four unusual books stand out. Their handwritten numbers appear in ascending order: 2, 4, 6, 8. Perhaps they relate to the locked drawer."
    if "desk" in t:
        return "Inside the desk you discover a small UV flashlight. It may reveal something invisible."
    if "painting" in t:
        return "The painting looks ordinary, but perhaps a special light would reveal hidden ink."
    if "drawer" in t:
        return "The drawer has a four-digit keypad. The bookshelf may contain the combination."
    if "2468" in t:
        return "The drawer clicks open! Inside is a small brass key."
    if "1357" in t or "door" in t:
        return "The exit door has a keypad and a keyhole. You may need both the brass key and the code hidden on the painting."
    return "The library is quiet. Try examining the desk, bookshelf, painting, drawer or door. What will you investigate?"
