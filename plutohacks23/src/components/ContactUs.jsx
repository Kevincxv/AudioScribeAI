import React, { useState } from 'react';

function ContactUs({ onNameChange }) {
    const [name, setName] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:5173/');
            const data = await response.json();
            onNameChange(data.name);
        } catch (error) {
            console.error(error);
        }
    };

    const handleChange = (event) => {
        setName(event.target.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Name:
                <input type="text" value={name} onChange={handleChange} />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
}

export default ContactUs;