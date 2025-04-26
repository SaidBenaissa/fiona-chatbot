import React, { useState, useEffect, useRef } from 'react';
import apiClient from './api'; // Ensure apiClient is imported
import './Chat.css'; // Import the CSS file

const Chat = ({ error: initialError, response: initialResponse, references: initialReferences }) => {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [language, setLanguage] = useState("English");
  const [currentError, setError] = useState(initialError);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (initialResponse) {
      const botMessage = { sender: 'bot', text: initialResponse, references: initialReferences };
      setMessages((prev) => [...prev, botMessage]);
    }
  }, [initialResponse, initialReferences]);

  const sendMessage = async () => { // Ensure function is async
    if (!input.trim()) return;
    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);
    setError(null);

    try {
      // *** This is the crucial part: Use apiClient.post ***
      const response = await apiClient.post('/query', { query: currentInput, language: language });

      if (response.data && response.data.answer) {
        const botMessage = { sender: 'bot', text: response.data.answer, references: response.data.references };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        setError("Received an unexpected response format from the server.");
      }
    } catch (err) {
      // ... existing error handling ...
       let errorMessage = "Failed to connect to the server.";
      if (err.response && err.response.data && err.response.data.detail) {
         if (typeof err.response.data.detail === 'string') {
            errorMessage = err.response.data.detail;
         } else {
             try {
                errorMessage = err.response.data.detail.map(e => `${e.loc[1]}: ${e.msg}`).join(', ');
             } catch {
                errorMessage = "An unknown error occurred in the backend.";
             }
         }
      } else if (err.response && err.response.data && err.response.data.answer) {
          errorMessage = err.response.data.answer;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  return (
    <div className="chat-container">
      <div className="language-selector">
        <label htmlFor="language">Language: </label>
        <select id="language" value={language} onChange={handleLanguageChange}>
          <option value="English">English</option>
          <option value="French">French</option>
          <option value="German">German</option>
        </select>
      </div>

      <div className="chat-history">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className="message-text">{msg.text}</div>
            {/* Display references if they exist for bot messages */}
            {msg.sender === 'bot' && msg.references && msg.references.length > 0 && (
              <div className="message-references">
                <strong>Sources:</strong>
                <ul>
                  {msg.references.map((ref, refIndex) => (
                    <li key={refIndex}>
                      {ref.metadata?.source || 'Unknown source'} (Chunk {ref.metadata?.chunk_index ?? 'N/A'})
                      {/* Optionally display ref.content snippet here too */}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="message bot-message loading-indicator">
            <span></span><span></span><span></span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {currentError && <div className="error-message">⚠️ {currentError}</div>}

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;