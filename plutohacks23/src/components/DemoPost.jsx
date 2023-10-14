import '../styles/demoPost.css';
import React, { useState } from 'react';

function DemoPost(){
    const [transcript, setTranscript] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchTranscript = () => {
        window.open('/display_transcript', '_blank');
    };
    
    const displaySummary = () => {
        window.open('/display_summary', '_blank');
    };

    const playAudio = async () => {
        try {
            const response = await fetch('/play_audio');
            const data = await response.json();
            setMessage(data.audio);
        } catch (err) {
            setError(err.message);
        }
    };

    const displayReminders = async () => {
        try {
            const response = await fetch('/display_reminders');
            const data = await response.json();
            setMessage(data.reminders);
        } catch (err) {
            setError(err.message);
        }
    };

    return(
    
        <>
            <div className="header">
                <h1 className="header-title">Finished call with {name}</h1>
                <p className="header-description">Here are some options for what to do after the call.</p>
            </div>
            <div className="buttonList">
                <button className="button" onClick={playAudio}>PlayBack</button>
                <button className="button" onClick={fetchTranscript}>Transcript</button>
                <button className="button" onClick={displaySummary}>Summary</button>
                <button className="button" onClick={displayReminders}>Reminders</button>
                <button className="button" >Translate</button>
            </div>
            {loading && <p>Loading transcript...</p>}
            {transcript && <div className="transcript">{transcript}</div>}
            {error && <p>Error: {error}</p>}
        </>
    )
}
export default DemoPost
