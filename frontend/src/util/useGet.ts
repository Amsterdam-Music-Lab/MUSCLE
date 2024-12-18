import { useState, useEffect, useCallback } from "react";
import axios from "axios";

export type Params = Record<string, string | number | boolean>;

// useGet is a react hook for getting data from a given url
export const useGet = <T,>(url: string): [T | null, boolean, (params?: Params) => Promise<void>] => {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async (params?: Params) => {
        setLoading(true);
        try {
            const response = await axios.get(url, { params });
            console.log({ response })
            setData(response.data);
        } catch (err) {
            setData(null);
        } finally {
            setLoading(false);
        }
    }, [url]);

    useEffect(() => {
        const source = axios.CancelToken.source();
        fetchData();

        return () => {
            source.cancel();
        };
    }, [url, fetchData]);

    return [data, loading, fetchData];
};

export default useGet;
