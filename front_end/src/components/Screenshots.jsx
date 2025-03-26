import React from "react";
import { Image } from "antd";

const Screenshots = ({ screenshots }) => {
    if (!screenshots || Object.keys(screenshots).length === 0) {
        return <p>No screenshots available.</p>;
    }

    return (
        <div style={{ marginTop: "24px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px" }}>
                {Object.entries(screenshots).map(([step, url]) => (
                    <div key={step} style={{ border: "1px solid #ddd", padding: "8px", borderRadius: "6px" }}>
                        <Image width="100%" src={`http://localhost:5000/screenshot/${url}`} alt={`Screenshot - ${step}`} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Screenshots;
