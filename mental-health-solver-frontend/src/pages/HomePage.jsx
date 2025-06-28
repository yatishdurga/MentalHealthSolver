// src/pages/HomePage.jsx
import React, { useState } from "react";
import axios from "axios";

function HomePage() {
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = { sender: "user", text: inputText };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        text: inputText,
      });
      const botMessage = {
        sender: "bot",
        text: `Your mental health category might be: ${response.data.prediction}`,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        sender: "bot",
        text: "⚠️ Something went wrong. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const styles = {
    container: {
      maxWidth: "600px",
      margin: "40px auto",
      padding: "20px",
      borderRadius: "15px",
      boxShadow: "0 8px 30px rgba(0, 0, 0, 0.1)",
      backgroundColor: "#f9f9f9",
      fontFamily: "'Segoe UI', sans-serif",
    },
    header: {
      fontSize: "22px",
      fontWeight: "bold",
      marginBottom: "20px",
      textAlign: "center",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      color: "#333",
    },
    chatBox: {
      height: "600px",
      overflowY: "auto",
      border: "5px solid #ddd",
      borderRadius: "15px",
      padding: "20px",
      backgroundColor: "#fff",
      marginBottom: "15px",
    },
    messageBubble: (sender) => ({
      padding: "10px 14px",
      marginBottom: "10px",
      borderRadius: "20px",
      backgroundColor: sender === "user" ? "#d0eaff" : "#e0e0e0",
      alignSelf: sender === "user" ? "flex-end" : "flex-start",
      maxWidth: "80%",
      display: "flex",
      alignItems: "center",
      color: "#333",
    }),
    form: {
      display: "flex",
      gap: "10px",
    },
    input: {
      flex: 1,
      padding: "10px",
      borderRadius: "20px",
      border: "1px solid #ccc",
      fontSize: "16px",
    },
    button: {
      padding: "10px 16px",
      borderRadius: "50%",
      backgroundColor: "#007bff",
      color: "white",
      border: "none",
      cursor: "pointer",
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <i className="fas fa-brain" style={{ marginRight: "10px" }}></i>
        Mental Health AI Assistant
      </div>

      <div style={{ ...styles.chatBox, display: "flex", flexDirection: "column" }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={styles.messageBubble(msg.sender)}>
            {msg.sender === "user" ? (
              <i className="fas fa-user-circle" style={{ marginRight: "8px" }}></i>
            ) : (
              <i className="fas fa-robot" style={{ marginRight: "8px", color: "#555" }}></i>
            )}
            {msg.text}
          </div>
        ))}
      </div>

      <form style={styles.form} onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your thoughts..."
          style={styles.input}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button type="submit" style={styles.button}>
          <i className="fas fa-paper-plane"></i>
        </button>
      </form>
    </div>
  );
}

export default HomePage;
