import React, { useEffect, useState } from 'react';
import { createEntityUrl } from '../config';
import { useParams } from 'react-router-dom';
import Page from './Page';
import { TranslatedContentForm } from './TranslatedContentForm';
import { FiSave, FiArrowLeft, FiPlus } from 'react-icons/fi';
import { Button } from './Button';
import { Accordion } from './Accordion';
import { PhaseForm } from './PhaseForm';

interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
  translated_content: TranslatedContent[];
  phases: Phase[];
}

interface ExperimentFormProps {
}


const ExperimentForm: React.FC<ExperimentFormProps> = () => {
  const [experiment, setExperiment] = useState<Experiment>({
    slug: '',
    active: true,
    translated_content: [],
    phases: []
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

  const handleAddPhase = () => {
    setExperiment(prev => ({
      ...prev,
      phases: [
        ...prev.phases,
        {
          index: prev.phases.length,
          dashboard: false,
          randomize: false,
        }
      ]
    }));
  };

  const handlePhaseChange = (index: number, updatedPhase: Phase) => {
    setExperiment(prev => ({
      ...prev,
      phases: prev.phases.map((phase, i) => {
        if (i === index) {
          // Preserve the existing ID if it exists
          return { ...updatedPhase, id: phase.id };
        }
        return phase;
      })
    }));
  };

  const handlePhaseDelete = (index: number) => {
    setExperiment(prev => ({
      ...prev,
      phases: prev.phases.filter((_, i) => i !== index)
    }));
  };

  if (loading && !success && !error && experimentId) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  return (
    <Page 
      title={experimentId ? 'Edit Experiment' : 'Create Experiment'}
    >
      <Button
        to="/experiments"
        variant="secondary"
        icon={<FiArrowLeft />}
        className="mb-4"
      >
        Back to Experiments
      </Button>

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

        <div className="mt-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Phases</h3>
            <Button
              variant="primary"
              size="sm"
              icon={<FiPlus />}
              onClick={handleAddPhase}
            >
              Add Phase
            </Button>
          </div>

          <Accordion
            items={experiment.phases.map((phase, index) => ({
              id: phase.id || index,
              title: `Phase ${index + 1}`,
              content: (
                <PhaseForm
                  phase={phase}
                  onChange={(updatedPhase) => handlePhaseChange(index, updatedPhase)}
                  onDelete={() => handlePhaseDelete(index)}
                />
              ),
            }))}
          />
        </div>

        <Button
          type="submit"
          disabled={loading}
          variant="success"
          icon={<FiSave />}
          className="mt-6"
        >
          {loading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
        </Button>
      </form>
    </Page>
  );
};

export default ExperimentForm;
