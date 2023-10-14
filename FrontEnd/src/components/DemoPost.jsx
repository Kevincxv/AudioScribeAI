import '../styles/demoPost.css';
import React, { useState } from 'react';
import axios from 'axios';

function DemoPost() {
    const [transcript, setTranscript] = useState(null);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showTranscript, setShowTranscript] = useState(false);
    const [showSummary, setShowSummary] = useState(false);

    const fetchTranscript = async () => {
        setLoading(true);
        try {
            // Simulate a delay to show loading state
            await new Promise(resolve => setTimeout(resolve, 2000));
            setTranscript('This is a temporary transcript.');
            setShowTranscript(true);
            setShowSummary(false);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchSummary = async () => {
        setLoading(true);
        try {
            // Simulate a delay to show loading state
            await new Promise(resolve => setTimeout(resolve, 2000));
            setSummary('This is a temporary summary.');
            setShowSummary(true);
            setShowTranscript(false);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const playAudio = async () => {
        try {
            const response = await axios.get('/play_audio');
            const audio = new Audio(response.data.audio_url);
            audio.play();
        } catch (err) {
            setError(err.message);
        }
    };

    const displayReminders = async () => {
        try {
            const response = await axios.get('/display_reminders');
            window.open(response.data.reminders_url, '_blank');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <>
            {showTranscript || showSummary? (
                <div className="transcript">
                    <textarea value={transcript || 'No transcript available.'} readOnly />
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
                    PlayBack
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