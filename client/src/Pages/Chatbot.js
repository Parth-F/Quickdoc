import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import axios from 'axios';
import chatboticon from '../assets/chatbot.png';
import page1 from '../assets/Page1.png';
import page2 from '../assets/Page2.png';
import page3 from '../assets/Page3.png';
import { Link } from 'react-router-dom';

// API base URL - can be configured based on environment
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const Chatbot = () => {
  const [messages, setMessages] = useState([{
    id: 1, 
    text: "Thanks for getting in touch with Astor today! 😊 We are here to help you build your wellness so that you are healthy today and tomorrow.", 
    type: "bot"
  }]);
  const [input, setInput] = useState("");
  const [showInstModal, setShowInstModal] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    document.title = 'Astor AI: Chatbot';
    
    // Clear any potentially stored chat data on component mount
    // This ensures a fresh session every time the page loads
    const currentMode = localStorage.getItem('mode');
    localStorage.clear();
    if (currentMode) {
      localStorage.setItem('mode', currentMode);
    }
  }, []);

  const handleCloseModal = () => {
    setShowInstModal(false);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prevMessages) => [...prevMessages, { id: prevMessages.length + 1, text: input, type: "user" }]);
    setInput("");

    // Get model preference from localStorage or default to flagship model
    const useFineTuneModel = localStorage.getItem('mode') === '0' || !localStorage.getItem('mode');
    
    try {
      const endpoint = useFineTuneModel ? 'queryFineTune' : 'queryRAG';
      const result = await axios.post(`${API_BASE_URL}/${endpoint}`, {
        query_text: input,
      });

      setMessages((prevMessages) => [...prevMessages, { id: prevMessages.length + 2, text: result.data.response, type: "bot" }]);
    } catch (error) {
      setMessages((prevMessages) => [...prevMessages, { id: prevMessages.length + 2, text: error.response?.data?.error || 'There was an error processing your request.', type: "bot" }]);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Determine which model is being used
  const modelType = localStorage.getItem('mode') === '0' || !localStorage.getItem('mode') ? "Flagship" : "Augmented";

  return (
    <div className="chatbot">
      {showInstModal && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: '#fff',
          padding: '30px',
          borderRadius: '12px',
          boxShadow: '0 8px 16px rgba(0,0,0,0.2)',
          zIndex: '1000',
          maxWidth: '90%',
          width: '800px',
          maxHeight: '80vh',
          overflowY: 'auto',
          textAlign: 'center',
          marginTop: '2%',
          paddingTop: '2%'
        }}>
          <div style={{ marginBottom: '20px' }}>
            <h2 style={{ fontSize: '1.5em', marginBottom: '10px', color: '#242424' }}>Welcome to Astor!</h2>
          </div>
          <div style={{ marginBottom: '20px', textAlign: 'left' }}>
            <h4 style={{ fontSize: '1.2em', marginBottom: '8px', color: '#333' }}>Step 1: Ask Your Question</h4>
            <p style={{ fontSize: '1em', lineHeight: '1.6', color: '#555' }}>
              Begin your interaction with Astor's chatbot by typing your medical question.
            </p>
            <img src={page1} alt="Step 1" style={{ width: '100%', maxWidth: '300px', height: 'auto', borderRadius: '10px', boxShadow: '0 0 10px rgba(0,0,0,0.2)' }} />
          </div>
          <div style={{ marginBottom: '20px', textAlign: 'left' }}>
            <h4 style={{ fontSize: '1.2em', marginBottom: '8px', color: '#333' }}>Step 2: Get Expert Answers</h4>
            <p style={{ fontSize: '1em', lineHeight: '1.6', color: '#555' }}>
              Receive accurate medical information from our AI assistant.
            </p>
            <img src={page2} alt="Step 2" style={{ width: '100%', maxWidth: '300px', height: 'auto', borderRadius: '10px', boxShadow: '0 0 10px rgba(0,0,0,0.2)' }} />
          </div>
          <div style={{ marginBottom: '20px', textAlign: 'left' }}>
            <h4 style={{ fontSize: '1.2em', marginBottom: '8px', color: '#333' }}>Step 3: Continue Your Conversation</h4>
            <p style={{ fontSize: '1em', lineHeight: '1.6', color: '#555' }}>
              Ask follow-up questions or start a new topic at any time.
            </p>
            <img src={page3} alt="Step 3" style={{ width: '100%', maxWidth: '300px', height: 'auto', borderRadius: '10px', boxShadow: '0 0 10px rgba(0,0,0,0.2)' }} />
          </div>
          <div style={{ marginTop: '20px' }}>
            <button onClick={handleCloseModal} style={{ backgroundColor: '#242424', color: '#fff', border: 'none', borderRadius: '8px', padding: '12px 25px', fontSize: '1em', cursor: 'pointer' }}>
              Got It!
            </button>
          </div>
        </div>
      )}
      
      <header className="navbar">
        <Link to='/about'>
          <img src={chatboticon} alt="chatbot-icon" className="logo" />
        </Link>
        <div className='title'>Astor - {modelType} Model</div>
      </header>
      
      <div className="chatbot-messages">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.type}`}>
            <p>{message.text}</p>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chatbot-footer">
        <div className="message-input-container">
          <input 
            className="message-input"
            type='text'
            value={input} 
            onChange={(e) => setInput(e.target.value)} 
            placeholder="Type your message..." 
          />
          <button className="send-button" onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
