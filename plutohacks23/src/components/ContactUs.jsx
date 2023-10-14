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
            <div className="name-input-container">
            </div>
            <button onClick={handleButtonClick}>Contact Us</button>
            <button onClick={onEmployeeClick}>Employee? Click Here</button>
        </div>
    </div>
  );
}

export default ContactUs;