import React, { useEffect, useState } from 'react';
import { createEntityUrl } from '../config';
import { useNavigate, useParams } from 'react-router-dom';
import Page from './Page';
import { TranslatedContentForm } from './TranslatedContentForm';
import { FiSave, FiArrowLeft, FiPlus, FiTrash, FiGlobe, FiLayers } from 'react-icons/fi';
import { Button } from './Button';
import { Tabs } from './Tabs';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { PhaseForm } from './PhaseForm';
import { Experiment, Phase, TranslatedContent } from '../types/types';

interface ExperimentFormProps {
}

interface UnsavedChanges {
  main: boolean;
  translatedContent: boolean;
  phases: boolean;
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
  const [activeTab, setActiveTab] = useState<'translatedContent' | 'phases'>('translatedContent');
  const [unsavedChanges, setUnsavedChanges] = useState<UnsavedChanges>({
    main: false,
    translatedContent: false,
    phases: false,
  });
  const [activePhaseIndex, setActivePhaseIndex] = useState(0);
  
  const navigate = useNavigate();
  const { id: experimentId } = useParams<{ id: string }>();
  const url = createEntityUrl('experiments', experimentId);

  const hasUnsavedChanges = unsavedChanges.main || unsavedChanges.translatedContent || unsavedChanges.phases;

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
    setUnsavedChanges(prev => ({ ...prev, main: true }));
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
    const newPhase = {
      index: experiment.phases.length,
      dashboard: false,
      randomize: false,
    };
    setExperiment(prev => ({
      ...prev,
      phases: [...prev.phases, newPhase]
    }));
    setActivePhaseIndex(experiment.phases.length);
    setUnsavedChanges(prev => ({ ...prev, phases: true }));
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
    setUnsavedChanges(prev => ({ ...prev, phases: true }));
  };

  const handlePhaseDelete = (index: number) => {
    if (confirm('Are you sure you want to remove this phase?')) {
      setExperiment(prev => ({
        ...prev,
        phases: prev.phases.filter((_, i) => i !== index)
      }));
      
      // Adjust activePhaseIndex after deletion
      setActivePhaseIndex(prevIndex => {
        if (prevIndex >= index && prevIndex > 0) {
          return prevIndex - 1;
        }
        return 0;
      });
      
      setUnsavedChanges(prev => ({ ...prev, phases: true }));
    }
  };

  const handleTranslatedContentChange = (newContents: TranslatedContent[]) => {
    setExperiment(prev => ({ ...prev, translated_content: newContents }));
    setUnsavedChanges(prev => ({ ...prev, translatedContent: true }));
  };

  const getTabLabel = (label: string, hasChanges: boolean) => {
    return hasChanges ? `${label} *` : label;
  };

  const getPhaseTabLabel = (index: number) => `Phase ${index + 1}`;

  useEffect(() => {
    if (success) {
      setUnsavedChanges({ main: false, translatedContent: false, phases: false });
    }
  }, [success]);

  if (loading && !success && !error && experimentId) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  return (
    <Page 
      title={experimentId ? 'Edit Experiment' : 'Create Experiment'}
    >
      <Button
        variant="secondary"
        icon={<FiArrowLeft />}
        className="mb-4"
        onClick={(e: React.MouseEvent) => {
          if (hasUnsavedChanges) {
            const confirmLeave = confirm('You have unsaved changes. Are you sure you want to leave?');
            if (!confirmLeave) {
              e.preventDefault();
              return;
            }
          }
          navigate('/experiments');
        }}
      >
        {`Back to Experiments${hasUnsavedChanges ? ' *' : ''}`}
      </Button>

      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-5 space-y-5 max-w-5xl">
        {error && <div className="text-red-600 mb-4">{error}</div>}
        {success && <div className="text-green-600 mb-4">Saved successfully!</div>}

        <div className="space-y-5">
          <FormField label="Slug">
            <Input
              type="text"
              name="slug"
              value={experiment.slug}
              onChange={handleChange}
              required
            />
          </FormField>

          <FormField label="Status">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                name="active"
                checked={experiment.active}
                onChange={handleChange}
                className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 h-5 w-5"
              />
              <span className="text-gray-700">Active</span>
            </label>
          </FormField>
        </div>

        <Tabs
          tabs={[
            {
              id: 'translatedContent',
              label: getTabLabel('Translated Content', unsavedChanges.translatedContent),
              icon: <FiGlobe />
            },
            {
              id: 'phases',
              label: getTabLabel('Phases', unsavedChanges.phases),
              icon: <FiLayers />
            },
          ]}
          activeTab={activeTab}
          onTabChange={(tabId) => setActiveTab(tabId as 'translatedContent' | 'phases')}
        />

        <div className="mt-4 px-2">
          {activeTab === 'translatedContent' && (
            <TranslatedContentForm
              contents={experiment.translated_content}
              onChange={handleTranslatedContentChange}
            />
          )}

          {activeTab === 'phases' && (
            <div className="">
              <h3 className="text-lg font-medium mb-5">Phases</h3>

              <Tabs
                tabs={[
                  ...experiment.phases.map((_, index) => ({
                    id: index,
                    label: getPhaseTabLabel(index),
                  })),
                  {
                    id: 'new',
                    label: (
                      <div className="flex items-center gap-2">
                        <FiPlus className="w-4 h-4" />
                        <span>New Phase</span>
                      </div>
                    ),
                  }
                ]}
                activeTab={activePhaseIndex}
                onTabChange={(tabId) => {
                  if (tabId === 'new') {
                    handleAddPhase();
                  } else {
                    setActivePhaseIndex(tabId as number);
                  }
                }}
                actions={[
                  {
                    icon: <FiTrash className="w-4 h-4" />,
                    title: 'Remove phase',
                    onClick: (tabId) => handlePhaseDelete(tabId as number),
                  },
                ]}
              />

              {experiment.phases.length > 0 && (
                <div className='p-5 bg-gray-50'>
                <div className="p-5 border rounded-md bg-white">
                  <PhaseForm
                    phase={experiment.phases[activePhaseIndex]}
                    onChange={(updatedPhase) => handlePhaseChange(activePhaseIndex, updatedPhase)}
                    onDelete={() => handlePhaseDelete(activePhaseIndex)}
                  />
                </div>
                </div>
              )}
            </div>
          )}
        </div>

        <Button
          type="submit"
          disabled={loading}
          variant="success"
          icon={<FiSave />}
          className="mt-5"
        >
          {loading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
        </Button>
      </form>
    </Page>
  );
};

export default ExperimentForm;
