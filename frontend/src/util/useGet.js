import { useState, useEffect } from "react";
import axios from "axios";

// useGet is a react hook for getting data from a given url
export const useGet = (url) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(url);
                setData(response.data);
                setLoading(false);
            } catch (err) {
                setData(null);
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return [data, loading];
};

export default useGet;
