# backend/agent.py
import re
from datetime import datetime, timedelta
from langgraph.graph import StateGraph
from tools import tools

class AgentState(dict):
    pass

def parse_hcp_name(text):
    match = re.search(r"(Dr\.?\s*[A-Za-z]+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    match2 = re.search(r"meet\s+([A-Z][a-z]+)", text, re.IGNORECASE)
    if match2:
        return "Dr " + match2.group(1)
    return "Unknown"

def parse_sentiment(text):
    if any(word in text.lower() for word in ["interested", "positive", "excited"]):
        return "positive"
    elif any(word in text.lower() for word in ["neutral", "ok"]):
        return "neutral"
    else:
        return "negative"

def parse_datetime(text):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d") if "today" in text.lower() else now.strftime("%Y-%m-%d")
    time_match = re.search(r"(\d{1,2}[:.]?\d{0,2}\s*(am|pm)?)", text, re.IGNORECASE)
    if time_match:
        t = time_match.group(1).replace(".", ":")
        try:
            time_obj = datetime.strptime(t.strip(), "%I:%M %p")
            time_str = time_obj.strftime("%H:%M")
        except:
            try:
                time_obj = datetime.strptime(t.strip(), "%I %p")
                time_str = time_obj.strftime("%H:%M")
            except:
                time_str = "00:00"
    else:
        time_str = "00:00"
    return f"{date} {time_str}", date, time_str

def parse_interaction_type(text):
    for t in ["face-to-face", "virtual", "call", "email"]:
        if t in text.lower():
            return t.title()
    return "Meeting"

def agent_node(state: AgentState):
    text = state.get("input", "")
    if not text:
        state["entities"] = {}
        state["summary"] = "No input received"
        state["tools"] = {}
        return state

    hcp_name = parse_hcp_name(text)
    sentiment = parse_sentiment(text)
    dt_str, date, time = parse_datetime(text)
    interaction_type = parse_interaction_type(text)

    # Outcomes & follow-up
    if sentiment in ["positive", "neutral"]:
        outcomes = "Follow-up required"
        followup_date = datetime.now() + timedelta(days=14)
        followup = f"Follow-up on {followup_date.strftime('%Y-%m-%d %H:%M')}"
    else:
        outcomes = "Needs attention"
        followup_date = datetime.now() + timedelta(days=3)
        followup = f"Follow-up on {followup_date.strftime('%Y-%m-%d %H:%M')}"

    state["entities"] = {
        "hcp_name": hcp_name,
        "sentiment": sentiment,
        "date": date,
        "time": time,
        "interaction_type": interaction_type,
        "topics": text,
        "outcomes": outcomes,
        "followup": followup
    }

    # Run all tools
    state["tools"] = {name: func(text) for name, func in tools.items()}

    state["summary"] = f"{hcp_name} {interaction_type} at {time}: {text}"
    return state

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.set_finish_point("agent")
agent = graph.compile()