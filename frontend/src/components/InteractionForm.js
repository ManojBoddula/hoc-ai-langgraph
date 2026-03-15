// src/components/InteractionForm.js
import React from "react";
import { useSelector } from "react-redux";

function InteractionForm() {
  const form = useSelector((state) => state.form);

  const sentimentEmoji = {
    positive: "😊",
    neutral: "😐",
    negative: "😞",
  };

  return (
    <div style={{ padding: "20px", background: "#f0f4f8", borderRadius: "12px" }}>
      <h2 style={{ color: "#2a2a72", marginBottom: "20px" }}>Log HCP Interaction</h2>

      {/* Card style fields */}
      <div className="field-card">
        <label>HCP Name</label>
        <input value={form.hcp_name || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Interaction Type</label>
        <input value={form.interaction_type || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Date</label>
        <input value={form.date || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Time</label>
        <input value={form.time || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Topics Discussed</label>
        <textarea value={form.topics || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Outcomes</label>
        <textarea value={form.outcomes || ""} readOnly />
      </div>

      <div className="field-card">
        <label>Follow Up</label>
        <textarea value={form.followup || ""} readOnly />
      </div>

      {/* Sentiment Badge */}
      {form.sentiment && (
        <div className={`sentiment ${form.sentiment}`}>
          {sentimentEmoji[form.sentiment]} {form.sentiment.toUpperCase()}
        </div>
      )}

      {/* Tools Outputs */}
      {form.tools && Object.keys(form.tools).length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h3 style={{ color: "#2a2a72" }}>Tools Outputs</h3>
          {Object.entries(form.tools).map(([toolName, value], idx) => (
            <div
              key={idx}
              className="tool-card"
              style={{
                border: "1px solid #ccc",
                padding: "10px",
                marginBottom: "8px",
                borderRadius: "8px",
                backgroundColor: "#dbeafe",
              }}
            >
              <strong>{toolName}</strong>
              <pre style={{ whiteSpace: "pre-wrap", marginTop: "5px" }}>
                {JSON.stringify(value, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default InteractionForm;