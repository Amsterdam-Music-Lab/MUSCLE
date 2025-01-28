import React, { useEffect, useState } from 'react';
import { createExperimentEntityUrl } from '../config';
import { useNavigate, useParams, Routes, Route, useLocation } from 'react-router-dom';
import Page from './Page';
import { TranslatedContentForms } from './TranslatedContentForms';
import { FiSave, FiArrowLeft, FiGlobe, FiLayers, FiLoader } from 'react-icons/fi';
import { Button } from './Button';
import { Tabs } from './Tabs';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Experiment, TranslatedContent } from '../types/types';
import { PhasesForm } from './PhasesForm';
import useFetch from '../hooks/useFetch';
import { useMutation } from '../hooks/useMutation';
import useBoundStore from '../utils/store';

interface ExperimentFormProps {
}

interface UnsavedChanges {
  main: boolean;
  translatedContent: boolean;
  phases: boolean;
}

const ExperimentForm: React.FC<ExperimentFormProps> = () => {
  const { id: experimentId } = useParams<{ id: string }>();
  const url = createExperimentEntityUrl('experiments', experimentId);
  const [experimentResource, error, loading] = useFetch(url, 'GET', null);
  const [saveExperiment, { loading: saveLoading }] = useMutation<Experiment>(
    url,
    experimentId ? 'PUT' : 'POST'
  );

  const experiment = useBoundStore(state => state.experiment);
  const setExperiment = useBoundStore(state => state.setExperiment);
  const patchExperiment = useBoundStore(state => state.patchExperiment);
  const addToast = useBoundStore(state => state.addToast);

  const [success, setSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState<'translatedContent' | 'phases'>('translatedContent');
  const [unsavedChanges, setUnsavedChanges] = useState<UnsavedChanges>({
    main: false,
    translatedContent: false,
    phases: false,
  });

  const navigate = useNavigate();
  const location = useLocation();

  const hasUnsavedChanges = unsavedChanges.main || unsavedChanges.translatedContent || unsavedChanges.phases;

  useEffect(() => {
    if (experimentResource) {
      setExperiment(experimentResource);
      navigate(`/experiments/${experimentId}/phases`);
    } else {
      setExperiment({
        slug: '',
        active: true,
        translated_content: [],
        phases: [],
      });
    }
  }, [experimentResource]);

  useEffect(() => {
    // Set active tab based on URL
    if (location.pathname.includes('/translated-content')) {
      setActiveTab('translatedContent');
    } else if (location.pathname.includes('/phases')) {
      setActiveTab('phases');
    }
  }, [location]);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        handleSubmit(event as unknown as React.FormEvent);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [experiment]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, type, checked, value } = e.target;
    patchExperiment({
      [name]: type === 'checkbox' ? checked : value
    });
    setUnsavedChanges(prev => ({ ...prev, main: true }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);

    try {
      const savedExperiment = await saveExperiment(experiment!);
      setSuccess(true);
      setExperiment(savedExperiment);
      addToast({
        message: "Experiment saved successfully!",
        duration: 3000,
        level: "success"
      });
    } catch (err) {
      addToast({
        message: "Failed to save experiment. Please try again.",
        duration: 5000,
        level: "error"
      });
      console.error("Error submitting form:", err);
    }
  };

  const handleTranslatedContentChange = (newContents: TranslatedContent[]) => {
    patchExperiment({ translated_content: newContents });
    setUnsavedChanges(prev => ({ ...prev, translatedContent: true }));
  };

  const getTabLabel = (label: string, hasChanges: boolean) => {
    return hasChanges ? `${label} *` : label;
  };

  const handleTabChange = (tabId: string) => {
    const tab = tabId as 'translatedContent' | 'phases';
    setActiveTab(tab);
    if (tab === 'translatedContent') {
      navigate(`/experiments/${experimentId}/translated-content`);
    } else {
      navigate(`/experiments/${experimentId}/phases`);
    }
  };

  useEffect(() => {
    if (success) {
      setUnsavedChanges({ main: false, translatedContent: false, phases: false });
    }
  }, [success]);

  if (loading && !success && !error && experimentId) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (!experiment) {
    return <div className="text-center mt-5">Experiment not found</div>;
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
              id: 'phases',
              label: getTabLabel('Phases & Blocks', unsavedChanges.phases),
              icon: <FiLayers />
            },
            {
              id: 'translatedContent',
              label: getTabLabel('Translated Content', unsavedChanges.translatedContent),
              icon: <FiGlobe />
            },
          ]}
          activeTab={activeTab}
          onTabChange={handleTabChange}
        />

        <div className="mt-4 px-2">
          <Routes>
            <Route
              path="translated-content/:language?"
              element={
                <TranslatedContentForms
                  contents={experiment.translated_content}
                  onChange={handleTranslatedContentChange}
                />
              }
            />
            <Route
              path="phases/:phaseIndex?/*"
              element={
                <PhasesForm
                  phases={experiment.phases}
                  onChange={(newPhases) => {
                    patchExperiment({ phases: newPhases });
                    setUnsavedChanges(prev => ({ ...prev, phases: true }));
                  }}
                />
              }
            />
          </Routes>
        </div>

        <hr className="my-4 border-t border-gray-300" />

        <Button
          type="submit"
          disabled={saveLoading}
          variant="success"
          icon={!saveLoading ? <FiSave /> : <div className="animate-spin"><FiLoader /></div>}
          className="mt-5"
        >
          {saveLoading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
        </Button>
      </form>
    </Page>
  );
};

export default ExperimentForm;
