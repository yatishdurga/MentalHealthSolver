import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FaRobot, FaPaperPlane } from 'react-icons/fa';

function HomePage() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messageEndRef = useRef(null);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = { type: 'user', text: inputText };
    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/analyze', {
        text: userMessage.text,
      });

      const { prediction, tips = [], books = [], videos = [], quotes = [], similar_statements = [] } = res.data;

      // Build bot response dynamically
      let botText = `🧠 It looks like you're experiencing: **${prediction}**.\n\n`;

      if (tips.length) botText += `💡 *Tips*:\n${tips.map((t) => `• ${t}`).join('\n')}\n\n`;
      if (books.length) botText += `📘 *Books*:\n${books.map((b) => `• ${b}`).join('\n')}\n\n`;
      if (videos.length) botText += `🎥 *Videos*:\n${videos.map((v) => `• ${v}`).join('\n')}\n\n`;
      if (quotes.length) botText += `💬 *Quote*:\n"${quotes[0]}"\n\n`;

      if (similar_statements.length) {
        botText += `🧑‍🤝‍🧑 *Similar Experiences*:\n${similar_statements
          .map((s, idx) => `${idx + 1}. "${s.statement}" (${s.category}, Score: ${s.score.toFixed(2)})`)
          .join('\n')}`;
      }

      setMessages((prev) => [...prev, { type: 'bot', text: botText.trim() }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { type: 'bot', text: '❗ Oops! Something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        backgroundColor: '#84dcfc',
        minHeight: '100vh',
        padding: '2rem',
        fontFamily: 'Arial, sans-serif',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          backgroundColor: '#a7bdc8',
          width: '100%',
          maxWidth: '600px',
          borderRadius: '20px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
          display: 'flex',
          flexDirection: 'column',
          height: '80vh',
        }}
      >
        {/* Header */}
        <div
          style={{
            backgroundColor: '#0c5c8c',
            color: '#fff',
            padding: '1rem',
            borderTopLeftRadius: '20px',
            borderTopRightRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontWeight: 'bold',
            fontSize: '1.1rem',
          }}
        >
          <FaRobot size={20} /> AI Mental Health Assistant
        </div>

        {/* Chat Window */}
        <div
          style={{
            flex: 1,
            padding: '1rem',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}
        >
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: msg.type === 'user' ? '#1493cb' : '#ffffff',
                color: msg.type === 'user' ? '#fff' : '#314256',
                padding: '0.75rem 1rem',
                borderRadius: '16px',
                maxWidth: '70%',
                whiteSpace: 'pre-line',
              }}
            >
              {msg.text}
            </div>
          ))}
          {loading && (
            <div style={{ alignSelf: 'flex-start', fontStyle: 'italic', color: '#314256' }}>
              Typing...
            </div>
          )}
          <div ref={messageEndRef} />
        </div>

        {/* Input Form */}
        <form
          onSubmit={handleSubmit}
          style={{
            display: 'flex',
            padding: '1rem',
            backgroundColor: '#fff',
            borderBottomLeftRadius: '20px',
            borderBottomRightRadius: '20px',
            borderTop: '1px solid #ccc',
          }}
        >
          <input
            type="text"
            placeholder="How are you feeling today?"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              padding: '0.75rem 1rem',
              fontSize: '1rem',
              borderRadius: '10px',
              backgroundColor: '#e9f6fa',
              color: '#314256',
              marginRight: '0.5rem',
            }}
          />
          <button
            type="submit"
            style={{
              backgroundColor: '#1493cb',
              color: '#fff',
              border: 'none',
              borderRadius: '10px',
              padding: '0.75rem 1rem',
              cursor: 'pointer',
              transition: 'background 0.3s',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <FaPaperPlane /> Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default HomePage;
