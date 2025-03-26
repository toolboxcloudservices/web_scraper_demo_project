import { useEffect, useState } from "react";

const Logs = () => {
    const [logs, setLogs] = useState([]); // Store logs in an array

    useEffect(() => {
        // Get the backend URL from environment variables or fallback to localhost during development
        const apiUrl = "http://localhost:5000/api";

        // Connect to the event source
        const eventSource = new EventSource(`${apiUrl}/logs`);

        eventSource.onmessage = function (event) {
            setLogs((prevLogs) => [...prevLogs, event.data]); // Append new logs
        };

        return () => {
            eventSource.close();
        };
    }, []);

    return (
        <div style={{ background: "#f5f5f5", padding: "15px", borderRadius: "8px", marginTop: "10px" }}>
            <pre style={{
                background: "#fff",
                padding: "15px",
                borderRadius: "5px",
                height: "auto", // Allows it to expand
                border: "1px solid #ddd",
                whiteSpace: "pre-line", // Keeps proper formatting while allowing line breaks
                wordBreak: "break-word", // Prevents overflow
            }}>
                {logs.length > 0 ? logs.join("\n") : "No logs yet..."}
            </pre>
        </div>
    );
};

export default Logs;
