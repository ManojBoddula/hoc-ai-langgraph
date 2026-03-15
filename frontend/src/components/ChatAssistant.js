import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";

function ChatAssistant() {
  const [msg, setMsg] = useState("");
  const dispatch = useDispatch();
  const messages = useSelector((state) => state.messages);
  const form = useSelector((state) => state.form);

  const sentimentEmoji = { positive: "😊", neutral: "😐", negative: "😞" };

  const send = async () => {
    if (!msg.trim()) return;

    dispatch({ type: "ADD_MESSAGE", payload: { type: "user", text: msg } });

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", { message: msg });
      const data = res.data;

      if (data.entities) {
        dispatch({ type: "UPDATE_FORM", payload: data.entities });
      }

      let botText = data.summary || "No response";
      if (data.entities && data.entities.sentiment) {
        botText = `${sentimentEmoji[data.entities.sentiment]} ${botText}`;
      }

      dispatch({ type: "ADD_MESSAGE", payload: { type: "bot", text: botText } });
      setMsg("");
    } catch (err) {
      console.error(err);
      dispatch({ type: "ADD_MESSAGE", payload: { type: "bot", text: "Backend connection error" } });
    }
  };

  return (
    <div>
      <h3>AI Assistant</h3>
      <div className="chat-history">
        {messages.map((m, idx) => (
          <div key={idx} className={`chat-message ${m.type}`}>
            <p>{m.text}</p>
          </div>
        ))}
      </div>
      <textarea
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
        placeholder="Describe your interaction..."
      />
      <button onClick={send} disabled={!msg.trim()}>Send</button>
    </div>
  );
}

export default ChatAssistant;