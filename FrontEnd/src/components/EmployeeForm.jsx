//EmployeeForm.jsx
import React, { useState } from 'react';
import '../styles/FrontPageStyle.css';
// import logo from '../assets/images/logo.png'; // Import the logo image


function EmployeeForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePhoneChange = (e) => {
    setPhone(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Submit the form data to the server
    console.log(`Name: ${name}, Email: ${email}, Phone: ${phone}`);
  };

  return (
    <div className="employee-form-container">
      <div className="box">
        <h3>Employee Info</h3>
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input type="text" value={name} onChange={handleNameChange} />
          </label>
          <label>
            Email:
            <input type="email" value={email} onChange={handleEmailChange} />
          </label>
          <label>
            Phone:
            <input type="tel" value={phone} onChange={handlePhoneChange} />
          </label>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default EmployeeForm;