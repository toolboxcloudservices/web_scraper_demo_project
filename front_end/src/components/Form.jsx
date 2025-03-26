import React, {useState} from "react";
import {Input, Button, Form as AntForm, message} from "antd";
import axios from "axios";

const Form = ({setData, setError, setScreenshots, setLoading, setStep, buttonLoading, setButtonLoading}) => {
    const [url, setUrl] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setData(null);
        setScreenshots(null); // Clear previous screenshots
        setLoading(true);
        setButtonLoading(true); // Enable button loading indicator when scraping starts

        // Set step to "Starting"
        setStep(0);

        try {
            // Simulate scraping process with steps
            setStep(1); // Change to "In Progress"

            const response = await axios.post("http://localhost:5000/api", {url});

            setData(response.data.data);
            setScreenshots(response.data.screenshots); // Save the screenshots data

            // Set step to "Finished"
            setStep(2); // Change to "Finished"
        } catch (err) {
            setError("Error fetching data. Please try again.");
            message.error("Error fetching data.");
        } finally {
            setLoading(false);
            setButtonLoading(false); // Disable button loading indicator when process ends
        }
    };

    return (
        <AntForm onSubmitCapture={handleSubmit} layout="vertical">
            <AntForm.Item label="Enter Town URL">
                <Input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://www.example.com"
                    required
                />
            </AntForm.Item>
            <Button
                type="primary"
                htmlType="submit"
                block
                loading={buttonLoading} // Now using buttonLoading state here
            >
                Start Scraping
            </Button>
        </AntForm>
    );
};

export default Form;
