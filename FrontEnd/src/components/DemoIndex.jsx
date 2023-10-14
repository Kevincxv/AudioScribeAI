import React, { useState, useEffect } from 'react';
import '../styles/demoIndex.css';
import images from '../assets/images/profile-pic-icon.png';
import answerIcon from '../assets/images/accept.svg'; 
import declineIcon from '../assets/images/decline.svg';
import DemoPost from './DemoPost';

function DemoIndex() {
    const [isAnswered, setIsAnswered] = useState(false);
    const [endCall, setEndCall] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    
    const ringAudio = new Audio('../assests/latest_recording.wav');

    const startRecording = async () => {
        try {
            const response = await fetch('/start_recording', { method: 'POST' });
            const data = await response.json();
            console.log(data.status);
            ringAudio.play(); // Play ringing sound
        } catch (err) {
            console.error(err.message);
        }
    };

    const stopRecording = async () => {
        try {
            const response = await fetch('/stop_recording', { method: 'POST' });
            const data = await response.json();
            console.log(data.status);
            setEndCall(true); // Set endCall to true
        } catch (err) {
            console.error(err.message);
        }
    };

    const handleAnswerClick = () => {
        setIsAnswered(true);
        startRecording();
    };

    const handleDeclineClick = () => {
        if (isAnswered) {
            stopRecording();
        }
        setEndCall(true); // Set endCall to true
    };

    useEffect(() => {
        if (endCall && !isAnswered) {
            setIsPaused(true); // Pause animation
            setTimeout(() => {
                setIsPaused(false); // Resume animation after 3 seconds
            }, 3000);
        }
    }, [endCall, isAnswered]);

    return (
        <>
            {isAnswered && endCall ? (
                <DemoPost />
            ) : (
                <div className="profile-container">
                    <h2>Someone is calling...</h2>
                    <img src={images} alt="Profile" className={`profile-pic ${isPaused ? 'paused' : ''}`} />
                    <div className="button-container">
                        {!isAnswered && !endCall && (
                            <button className="answer" onClick={handleAnswerClick}>
                                <img src={answerIcon} alt="Answer" />
                            </button>
                        )}
                        {!endCall && (
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