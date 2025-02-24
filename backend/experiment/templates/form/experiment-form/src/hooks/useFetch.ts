import { useState, useEffect, useCallback } from "react";

// useFetch is a react hook for getting data from a given url
export const useFetch = <T,>(url: string, method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'GET', body: any = null): [T | null, string | null, boolean, () => void] => {

  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setData(null);
    setError(null);
    setLoading(true);
    try {

      let options: RequestInit = {
        method,
      }

      if (body) {
        options = {
          ...options,
          body: JSON.stringify(body),
          headers: { 'Content-Type': 'application/json' }
        }
      }

      const jwt = localStorage.getItem('jwt');

      if (jwt) {
        options = {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${jwt}`
          }
        }
      }

      const response = await fetch(url, options);
      const jsonData = await response.json();
      setData(jsonData);
    } catch (err) {
      setData(null);
      setError(err.toString());

    } finally {
      setLoading(false);
    }
  }, [url, method, body]);

  useEffect(() => {
    const abortController = new AbortController();
    fetchData();
    return () => {
      abortController.abort();
    };
  }, [url, fetchData]);

  return [data, error, loading, fetchData];
};

export default useFetch;
