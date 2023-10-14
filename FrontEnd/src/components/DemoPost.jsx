import '../styles/demoPost.css';
import React, { useState } from 'react';
import axios from 'axios';

function DemoPost() {
    const [transcript, setTranscript] = useState(null);
    const [tempTranscript, setTempTranscript] = useState(null); // new state variable
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showTranscript, setShowTranscript] = useState(false);
    const [showSummary, setShowSummary] = useState(false);

    const fetchTranscript = async () => {
        setLoading(true);
        await axios
            .get('http://localhost:5000/transcribe')
            .then((res) => {
                console.log(res.data.transcript);
                setTranscript(res.data.transcript);
                setTempTranscript(res.data.transcript); 
                setShowTranscript(true);
                setShowSummary(false);
            })
            .catch((err) => {
                console.log(err);
            });
        setLoading(false);
        document.querySelector('.transcript').classList.add('show');
    };
    
    const fetchSummary = async () => {
        setLoading(true);
        await axios
            .get('http://localhost:5000/summarize')
            .then((res) => {
                setSummary(res.data.summary);
                setShowSummary(true);
                setShowTranscript(false);
            })
            .catch((err) => {
                console.log(err);
            });
        setLoading(false);
        document.querySelector('.transcript').classList.add('show');
    };

    const playAudio = async () => {
        try {
            const response = await axios.get('http://localhost:5000/play_audio');
            const audio = new Audio(response.data.audio_url);
            audio.play();
        } catch (err) {
            setError(err.message);
        }
    };

    const displayReminders = async () => {
        try {
            const response = await axios.get('http://localhost:5000/display_reminders');
            window.open(response.data.reminders_url, '_blank');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <>
            {showTranscript || showSummary? (
                <div className="transcript">
                    <textarea value={tempTranscript || 'No transcript available.'} readOnly /> {/* use tempTranscript */}
                </div>
            ) : (
                <div className="header">
                    <h1 className="header-title">Finished call</h1>
                    <p className="header-description">Here are some options for what to do after the call.</p>
                </div>
            )}
            {showSummary && (
                <div className="summary transcript">
                    <textarea value={summary || 'No summary available.'} readOnly />
                </div>
            )}
            <div className="buttonList">
                <button className="button" onClick={playAudio}>
                    Playback
                </button>
                <button className="button" onClick={fetchTranscript}>
                    Transcript
                </button>
                <button className="button" onClick={fetchSummary}>
                    Summary
                </button>
                <button className="button" onClick={displayReminders}>
                    Reminders
                </button>
                <button className="button">Translate</button>
            </div>
            {loading && <p>Loading transcript...</p>}
            {error && <p>Error: {error}</p>}
        </>
    );
}

export default DemoPost;