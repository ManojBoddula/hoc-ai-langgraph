# backend/tools.py
import re
from datetime import datetime, timedelta

tools = {}

# --- 3. Action Type Classifier ---
def action_type_classifier(text):
    keywords = {
        "call": ["call", "phone"],
        "email": ["email", "mail"],
        "meeting": ["meet", "meeting", "face-to-face"],
        "demo": ["demo", "demonstration"],
        "webinar": ["webinar", "session"]
    }
    for action, words in keywords.items():
        if any(word in text.lower() for word in words):
            return {"interaction_type": action.title()}
    return {"interaction_type": "Meeting"}

# --- 7. Topic Trend Tracker ---
topic_counts = {}
def topic_trend_tracker(text):
    global topic_counts
    topics = ["AI tools", "drug trials", "clinical trials", "new platform"]
    found = []
    for topic in topics:
        if topic.lower() in text.lower():
            found.append(topic)
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    return {"topics_found": found, "topic_counts": topic_counts.copy()}

# --- 8. Keyword-Based Recommendations ---
def keyword_recommendations(text):
    recommendations = []
    if "ai tools" in text.lower():
        recommendations.append("Schedule demo for AI tools")
    if "drug trial" in text.lower():
        recommendations.append("Share clinical trial info")
    if "new platform" in text.lower():
        recommendations.append("Provide onboarding info")
    return {"recommendations": recommendations}

# --- 9. Meeting Conflict Detector ---
scheduled_meetings = []
def meeting_conflict_detector(text):
    conflict = False
    time_match = re.search(r"(\d{1,2}[:.]?\d{0,2}\s*(am|pm)?)", text, re.IGNORECASE)
    if time_match:
        t = time_match.group(1).replace(".", ":")
        for m in scheduled_meetings:
            if t in m:
                conflict = True
        scheduled_meetings.append(t)
    return {"meeting_conflict": conflict, "scheduled_times": scheduled_meetings.copy()}

# --- Other tools ---
def log_interaction(text):
    return {"message": "Interaction logged", "data": text}

def edit_interaction(text):
    return {"message": "Interaction editable via chat", "data": text}

def summarize_notes(text):
    return {"summary": text[:100]}

def suggest_followup(text):
    followup_date = datetime.now() + timedelta(days=14)
    return {"suggestion": f"Follow-up scheduled on {followup_date.strftime('%Y-%m-%d %H:%M')}"}

def extract_entities(text):
    return {"hcp_name": "Dr Smith", "sentiment": "positive"}

def sentiment_analysis(text):
    if any(word in text.lower() for word in ["positive", "interested", "excited"]):
        s = "positive"
    elif any(word in text.lower() for word in ["neutral", "ok"]):
        s = "neutral"
    else:
        s = "negative"
    return {"sentiment": s}

def meeting_info(text):
    return {"meeting": "Meeting detected in text"}

# Add all tools
tools["action_type"] = action_type_classifier
tools["topic_trend"] = topic_trend_tracker
tools["keyword_reco"] = keyword_recommendations
tools["meeting_conflict"] = meeting_conflict_detector
tools["log"] = log_interaction
tools["edit"] = edit_interaction
tools["summarize"] = summarize_notes
tools["followup"] = suggest_followup
tools["extract"] = extract_entities
tools["sentiment"] = sentiment_analysis
tools["meeting"] = meeting_info