# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_node  # use the node function directly

app = FastAPI(title="AI CRM HCP Backend")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI CRM backend running"}

@app.post("/chat")
async def chat(data: ChatRequest):
    try:
        # --- Call node directly ---
        result = agent_node({"input": data.message})

        if result is None:
            return {"entities": {}, "summary": ""}

        return {
            "entities": result.get("entities", {}),
            "summary": result.get("summary", "")
        }

    except Exception as e:
        return {"error": str(e)}