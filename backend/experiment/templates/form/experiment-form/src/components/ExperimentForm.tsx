import React, { useEffect, useState } from 'react';
import { createEntityUrl } from '../config';
import { useParams } from 'react-router-dom';
import Page from './Page';
import { TranslatedContentForm } from './TranslatedContentForm';

interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
  translated_content: TranslatedContent[];
}

interface ExperimentFormProps {
}


const ExperimentForm: React.FC<ExperimentFormProps> = () => {
  const [experiment, setExperiment] = useState<Experiment>({
    slug: '',
    active: true,
    translated_content: []
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const { id: experimentId } = useParams<{ id: string }>();
  const url = createEntityUrl('experiments', experimentId);

  useEffect(() => {
    if (experimentId) {
      setLoading(true);
      fetch(url)
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
    <Page 
      title={experimentId ? 'Edit Experiment' : 'Create Experiment'}
      backTo="/experiments"
      backText="Back to Experiments"
    >
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-4">
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

        <TranslatedContentForm
          contents={experiment.translated_content}
          onChange={(newContents) => setExperiment(prev => ({ ...prev, translated_content: newContents }))}
        />

        <button
          type="submit"
          disabled={loading}
          className="mt-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
        </button>
      </form>
    </Page>
  );
};

export default ExperimentForm;
