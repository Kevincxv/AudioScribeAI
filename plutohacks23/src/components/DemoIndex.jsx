import React from 'react';
import '../styles/demoIndex.css';
import images from '../assets/images/profile-pic-icon.png';
import answerIcon from '../assets/images/accept.svg'; 
import declineIcon from '../assets/images/decline.svg';


function DemoIndex() {
    // const [callerName, setCallerName] = useState('');
    const startRecording = async () => {
        // Implement the function to start recording (from the previous example)
    };

    const stopRecording = async () => {
        // Implement the function to stop recording (from the previous example)
    };

    return (
        <div className="profile-container">
            {/* <h2>{callerName ? `${callerName} is calling...` : 'Waiting for a call...'}</h2> */}
            <img src={images} alt="Profile" className="profile-pic" />
            <div className="button-container">
                <button className="answer" onClick={startRecording}>
                    <img src={answerIcon} alt="Answer" />
                </button>
                <button className="decline" onClick={stopRecording}>
                    <img src={declineIcon} alt="Decline" />
                </button>
                {/* <ContactUs onNameChange={setCallerName} /> */}
            </div>
        </div>
    );
}

export default DemoIndex;
