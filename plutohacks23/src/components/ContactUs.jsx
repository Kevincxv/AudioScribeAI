//ContactUs.jsx
import React, { useState } from 'react';
import '../styles/FrontPageStyle.css';

function ContactUs({ onNameChange, onEmployeeClick }) {
  const [name, setName] = useState('');

  const handleNameChange = (e) => {
    setName(e.target.value);
    if (onNameChange) {
      onNameChange(e.target.value); // Notify about the name change
    }
  };

  const handleButtonClick = () => {
    // Handle button click event
    // used to handle the button click event
  };

  return (
    <div className="contact-us-container">
      <div className="box-container">
        <h3>Contact Us</h3>
            <div className="name-input-container">
            <input
                type="text"
                value={name}
                onChange={handleNameChange}
                placeholder="Enter your name"
            />
            </div>
            <button onClick={handleButtonClick}>Enter</button>
            <button onClick={onEmployeeClick}>Employee? Click Here</button>
        </div>
    </div>
  );
}

export default ContactUs;