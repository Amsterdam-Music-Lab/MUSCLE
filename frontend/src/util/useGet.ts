import { useState, useEffect } from "react";
import axios from "axios";

// useGet is a react hook for getting data from a given url
export const useGet = <T,>(url: string): [T | null, boolean] => {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setData(null);
        setLoading(true);

        const source = axios.CancelToken.source();
        const fetchData = async () => {
            try {
                const response = await axios.get(url);
                setData(response.data);
                setLoading(false);
            } catch (err) {
                setData(null);
                console.error(err);
                setLoading(false);
            }
        };
        fetchData();

        return () => {
            setData(null);
            setLoading(false);
            source.cancel();
        };
    }, [url]);

    return [data, loading];
};

export default useGet;
