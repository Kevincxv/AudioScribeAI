import '../styles/demoPost.css';
import React, { useState, useEffect } from 'react';


function DemoPost(){
    const [transcript, setTranscript] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);
    const [name, setName] = useState("Customer");

    const fetchTranscript = async () => {
        setError(null);
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/display_transcript');
            const data = await response.json();
            setTranscript(data.transcript);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    
    const displaySummary = async () => {
        setError(null);
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/display_summary');
            const data = await response.json();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const playAudio = async () => {
        setError(null);
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/play_audio');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const displayReminders = async () => {
        setError(null);
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/display_reminders');
            const data = await response.json();
            // Do something with reminders data if needed
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTranscript();
    }, []);

    return (
        <div className="App">
            {loading && <div>Loading...</div>}
            {error && <div>Error: {error}</div>}
            {transcript && <div>{transcript}</div>}
            <button onClick={displaySummary}>Display Summary</button>
            <button onClick={playAudio}>Play Audio</button>
            <button onClick={displayReminders}>Display Reminders</button>
        </div>
    );
}
export default DemoPost;
