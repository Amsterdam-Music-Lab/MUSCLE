import { useState, useEffect } from 'react';
import { createExperimentAPIUrl } from '../config';

export interface BlockRule {
  id: string;
  name: string;
}

export const useBlockRules = () => {
  const [rules, setRules] = useState<BlockRule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRules = async () => {
      setLoading(true);
      try {
        const response = await fetch(createExperimentAPIUrl('block-rules'));
        if (!response.ok) throw new Error('Failed to fetch block rules');
        const data = await response.json();
        setRules(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchRules();
  }, []);

  return { rules, loading, error };
};
