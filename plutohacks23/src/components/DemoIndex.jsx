import React, { useState, useEffect } from 'react';
import '../styles/demoIndex.css';
import images from '../assets/images/profile-pic-icon.png';
import answerIcon from '../assets/images/accept.svg'; 
import declineIcon from '../assets/images/decline.svg';

function DemoIndex() {
    const [callerName, setCallerName] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [isAnswered, setIsAnswered] = useState(false);
    const [isDeclined, setIsDeclined] = useState(false);

    const startRecording = async () => {
        // Implement the function to start recording (from the previous example)
    };

    const stopRecording = async () => {
        // Implement the function to stop recording (from the previous example)
    };

    const handleAnswerClick = () => {
        setIsAnswered(true);
    };

    const handleDeclineClick = () => {
        setIsDeclined(true);
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5173/');
                const data = await response.json();
                setCallerName(data.name);
                setIsLoading(false);
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (isDeclined) {
            setIsAnswered(false);
            setIsDeclined(false);
        }
    }, [isDeclined]);

    return (
        <div className="profile-container">
            {isLoading ? (
                <h2>Loading...</h2>
            ) : (
                <h2>{callerName ? `${callerName} is calling...` : 'Waiting for a call...'}</h2>
            )}
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
    );
}

export default DemoIndex;