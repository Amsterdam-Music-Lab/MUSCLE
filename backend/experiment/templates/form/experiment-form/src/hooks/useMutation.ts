import { useState, useCallback } from "react";

export const useMutation = <T, R = T>(
  url: string,
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'POST'
): [(data: T) => Promise<R>, { loading: boolean; error: string | null; data: R | null }] => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<R | null>(null);

  const mutate = useCallback(async (body: T) => {
    setLoading(true);
    setError(null);

    try {
      const jwt = localStorage.getItem('jwt');
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...(jwt && { Authorization: `Bearer ${jwt}` })
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData));
      }

      const jsonData = await response.json();
      setData(jsonData);
      return jsonData;
    } catch (err) {
      setError(err.toString());
      throw err;
    } finally {
      setLoading(false);
    }
  }, [url, method]);

  return [mutate, { loading, error, data }];
};

export default useMutation;
