import React from "react";
import InteractionForm from "./components/InteractionForm";
import ChatAssistant from "./components/ChatAssistant";
import "./styles.css";

function App() {
  return (
    <div className="container">
      <div className="left">
        <InteractionForm />
      </div>
      <div className="right">
        <ChatAssistant />
      </div>
    </div>
  );
}

export default App;