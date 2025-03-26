import Form from "../components/Form";
import Logs from "../components/Logs";
import Screenshots from "../components/Screenshots";
import Results from "../components/Results";
import { useState } from "react";

const Home = () => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [screenshots, setScreenshots] = useState({});

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-2xl font-bold text-center my-6">IT Department Data Scraper</h1>
            <Form setData={setData} setError={setError} setScreenshots={setScreenshots} />
            <Logs />
            <Screenshots screenshots={screenshots} />
            <Results data={data} error={error} />
        </div>
    );
};

export default Home;
