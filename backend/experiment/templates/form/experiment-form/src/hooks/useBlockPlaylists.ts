import { useState, useEffect } from 'react';
import { createEntityUrl } from '../config';

export interface BlockPlaylists {
  id: string;
  name: string;
}

export const useBlockPlaylists = () => {
  const [playlists, setPlaylists] = useState<BlockPlaylists[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaylists = async () => {
      setLoading(true);
      try {
        const response = await fetch(createEntityUrl('section', 'playlists'));
        if (!response.ok) throw new Error('Failed to fetch playlists');
        const data = await response.json();
        setPlaylists(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, []);

  return { playlists, loading, error };
};
