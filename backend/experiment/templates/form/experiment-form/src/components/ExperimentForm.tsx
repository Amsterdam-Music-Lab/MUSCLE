import React, { useEffect, useState } from 'react';

interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
}

interface ExperimentFormProps {
  experimentId?: number; // If provided, we edit an existing experiment, otherwise we create a new one
}

const ExperimentForm: React.FC<ExperimentFormProps> = ({ experimentId }) => {
  const [experiment, setExperiment] = useState<Experiment>({ slug: '', active: true });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (experimentId) {
      setLoading(true);
      fetch(`/api/experiments/${experimentId}/`)
        .then(res => res.json())
        .then(data => {
          setExperiment(data);
          setLoading(false);
        })
        .catch(err => {
          setError('Failed to load experiment');
          setLoading(false);
        });
    }
  }, [experimentId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, type, checked, value } = e.target;
    setExperiment(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    const method = experimentId ? 'PUT' : 'POST';
    const url = experimentId ? `/api/experiments/${experimentId}/` : '/api/experiments/';

    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(experiment),
    })
      .then(res => {
        if (!res.ok) {
          return res.json().then(errData => {
            throw new Error(JSON.stringify(errData));
          });
        }
        return res.json();
      })
      .then(data => {
        setSuccess(true);
        setLoading(false);
        setExperiment(data); // update state with returned data
      })
      .catch(err => {
        console.error(err);
        setError('Failed to save experiment.');
        setLoading(false);
      });
  };

  if (loading && !success && !error && experimentId) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-4 bg-white shadow-md rounded">
      <h2 className="text-xl font-bold mb-4">{experimentId ? 'Edit Experiment' : 'Create Experiment'}</h2>

      {error && <div className="text-red-600 mb-4">{error}</div>}
      {success && <div className="text-green-600 mb-4">Saved successfully!</div>}

      <label className="block mb-2">
        <span className="text-gray-700">Slug</span>
        <input
          type="text"
          name="slug"
          value={experiment.slug}
          onChange={handleChange}
          required
          className="mt-1 block w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
        />
      </label>

      <label className="flex items-center mb-4">
        <input
          type="checkbox"
          name="active"
          checked={experiment.active}
          onChange={handleChange}
          className="mr-2 form-checkbox h-5 w-5 text-blue-600"
        />
        <span className="text-gray-700">Active</span>
      </label>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
      </button>
    </form>
  );
};

export default ExperimentForm;
