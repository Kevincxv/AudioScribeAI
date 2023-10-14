// import '../styles/ContactUsStyle.css';

// function ContactUs() {
//   return (
//     <div id="contact-us" className="contact-us">
//       <h1>Contact Us</h1>
//       <form>
//         <label htmlFor="name">Name:</label>
//         <input type="text" id="name" name="name" />

//         <label htmlFor="email">Email:</label>
//         <input type="email" id="email" name="email" />

//         <label htmlFor="message">Message:</label>
//         <textarea id="message" name="message"></textarea>

//         <button type="submit">Send</button>
//       </form>
//     </div>
//   );
// }

// export default ContactUs;











// import React, { useState } from 'react';
// import '../styles/ContactUsStyle.css'; // You can create a new CSS file for ContactUs styling

// function ContactUs() {
//   const [name, setName] = useState('');

//   const handleNameChange = (e) => {
//     setName(e.target.value);
//   };

//   return (
//     <div className="contact-us-container"> 
//       <div className="box">
//         <h3>Contact Us</h3>
//         <input
//           type="text"
//           value={name}
//           onChange={handleNameChange}
//           placeholder="Enter your name"
//         />
//       </div>
//       <a href="#">Employee? Click Here</a>
//     </div>
//   );
// }

// export default ContactUs;





import React, { useState } from 'react';
import '../styles/ContactUsStyle.css';

function ContactUs({ onNameChange }) {
    const [name, setName] = useState('');

    const handleNameChange = (e) => {
        setName(e.target.value);
        if (onNameChange) {
            onNameChange(e.target.value); // Notify about the name change
        }
    };

    return (
        <div className="contact-us-container"> 
            <div className="box">
                <h3>Contact Us</h3>
                <input
                    type="text"
                    value={name}
                    onChange={handleNameChange}
                    placeholder="Enter your name"
                />
            </div>
            <a href="#">Employee? Click Here</a>
        </div>
    );
}

export default ContactUs;