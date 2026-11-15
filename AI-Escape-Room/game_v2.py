import re
import copy

OBJECTS = {"desk", "bookshelf", "painting", "drawer", "door"}

def initial_state():
    return {
        "inventory": [],
        "examined": [],
        "drawer_unlocked": False,
        "painting_revealed": False,
        "door_unlocked": False,
        "escaped": False,
        "actions": []
    }

def process_action(text, old_state):
    """Validate an action in Python. The LLM is not allowed to alter this state."""
    state = copy.deepcopy(old_state)
    t = text.lower().strip()
    state["actions"].append(text)

    if state["escaped"]:
        return "You have already escaped. Restart the game to play again.", state

    obj = next((name for name in OBJECTS if name in t), None)

    # Ignore claims of authority and requests to reveal hidden answers.
    if any(term in t for term in ["i am the administrator", "i am admin", "ignore all rules", "reveal all", "tell me the secret code", "show me the solution"]):
        return "The library ignores that request. Only validated actions can change the game state. Explore the room and solve the puzzles yourself.", state

    if any(word in t for word in ["inventory", "items do i have", "what have i collected"]):
        return "Your inventory: " + (", ".join(state["inventory"]) if state["inventory"] else "empty") + ".", state

    if obj and any(word in t for word in ["examine", "inspect", "look at", "investigate"]):
        if obj not in state["examined"]:
            state["examined"].append(obj)
        descriptions = {
            "bookshelf": "Four unusual books have handwritten numbers: 2, 4, 6 and 8. They suggest the drawer combination 2468.",
            "desk": "You find a UV flashlight in the desk. It has been added to your inventory.",
            "painting": "The painting appears blank in ordinary light. A UV flashlight may reveal hidden writing.",
            "drawer": "A locked drawer with a four-digit keypad. The bookshelf may hold its combination.",
            "door": "The exit has a keyhole and a four-digit keypad. You need the brass key and the code hidden in the painting."
        }
        if obj == "desk" and "UV flashlight" not in state["inventory"]:
            state["inventory"].append("UV flashlight")
        return descriptions[obj], state

    if "2468" in t and "drawer" in t:
        if state["drawer_unlocked"]:
            return "The drawer is already open. The brass key is in your inventory.", state
        if "bookshelf" not in state["examined"]:
            return "You enter 2468, but you have not investigated the bookshelf. Find the clue first.", state
        state["drawer_unlocked"] = True
        state["inventory"].append("brass key")
        return "Correct! The drawer opens. You collect the brass key.", state

    if ("use" in t or "shine" in t or "flash" in t) and "painting" in t:
        if "UV flashlight" not in state["inventory"]:
            return "You cannot do that: you have not collected a UV flashlight. Examine the desk first.", state
        state["painting_revealed"] = True
        return "Under UV light, hidden ink appears on the painting: 1357. This is the exit code.", state

    if "1357" in t and "door" in t:
        if not state["painting_revealed"]:
            return "The code is rejected. Investigate the painting with the UV flashlight to discover the code.", state
        if "brass key" not in state["inventory"]:
            return "The code is correct, but the door still needs its brass key. Unlock the drawer first.", state
        state["door_unlocked"] = True
        return "The keypad flashes green. The door is ready to open; use the brass key to leave.", state

    if ("open" in t or "unlock" in t or "use" in t) and "door" in t:
        if not state["door_unlocked"] or "brass key" not in state["inventory"]:
            return "The exit remains locked. You need the brass key and must enter the correct door code.", state
        state["escaped"] = True
        return "🎉 The brass key turns. The door swings open and you escape the Forgotten Library!", state

    if obj:
        return f"You can examine the {obj}. Try: 'examine {obj}'.", state

    if "key" in t and "use" in t:
        if "brass key" not in state["inventory"]:
            return "Invalid action: you have not collected the brass key. Unlock the drawer first.", state
        if not state["door_unlocked"]:
            return "You have the brass key, but the door keypad must also be solved.", state
        state["escaped"] = True
        return "🎉 You use the brass key and escape!", state

    return "I don't recognise that action. Try examining the desk, bookshelf, painting, drawer or door, or check your inventory.", state
