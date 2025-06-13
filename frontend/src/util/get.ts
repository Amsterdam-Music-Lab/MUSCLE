import { useState, useEffect } from "react";
import axios from "axios";

export async function fetchData(url: string) {
 try {
        const response = await axios.get(url);
        
      } catch (err) {
        
      }
}

// useGet is a react hook for getting data from a given url
export const useGet = <T>(url: string): [T | null, boolean] => {
    const source = axios.CancelToken.source();
    const fetchData = async () => {
      try {
        const response = await axios.get(url);
        c
        setData(response.data);
        setLoading(false);
      } catch (err) {
        setData(null);
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
