import React from 'react';
import './App.css';
import Chatbot from './Pages/Chatbot';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from './Pages/HomePage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Chatbot as default landing page */}
        <Route path="/" element={<Chatbot />} />
        {/* About page */}
        <Route path="/about" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
