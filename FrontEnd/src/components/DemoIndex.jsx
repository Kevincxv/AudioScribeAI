import React, { useState } from 'react';
import '../styles/demoIndex.css';
import images from '../assets/images/profile-pic-icon.png';
import answerIcon from '../assets/images/accept.svg'; 
import declineIcon from '../assets/images/decline.svg';
import DemoPost from './DemoPost';

function DemoIndex() {
    const [isAnswered, setIsAnswered] = useState(false);
    const [isDeclined, setIsDeclined] = useState(false);
    const [callerName, setCallerName] = useState('');

    const startRecording = async () => {
        try {
            const response = await fetch('/start_recording', { method: 'POST' });
            const data = await response.json();
            console.log(data.status);
        } catch (err) {
            console.error(err.message);
        }
    };

    const stopRecording = async () => {
        try {
            const response = await fetch('/stop_recording', { method: 'POST' });
            const data = await response.json();
            console.log(data.status);
        } catch (err) {
            console.error(err.message);
        }
    };

    const handleAnswerClick = () => {
        setIsAnswered(true);
        startRecording();
    };

    const handleDeclineClick = () => {
        setIsDeclined(true);
        stopRecording();
    };

    return (
        <>
            {isDeclined ? (
                <DemoPost name={callerName} />
            ) : (
                <div className="profile-container">
                    <h2>Waiting for a call...</h2>
                    <img src={images} alt="Profile" className="profile-pic" />
                    <div className="button-container">
                        {!isAnswered && !isDeclined && (
                            <button className="answer" onClick={handleAnswerClick}>
                                <img src={answerIcon} alt="Answer" />
                            </button>
                        )}
                        {!isDeclined && (
                            <button className="decline" onClick={handleDeclineClick}>
                                <img src={declineIcon} alt="Decline" />
                            </button>
                        )}
                    </div>
                </div>
            )}
        </>
    );
}

export default DemoIndex;