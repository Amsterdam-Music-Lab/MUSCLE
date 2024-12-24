import React, { useEffect, useState } from 'react';
import { createEntityUrl } from '../config';
import { useNavigate, useParams, Routes, Route, useLocation, Navigate } from 'react-router-dom';
import Page from './Page';
import { TranslatedContentForm } from './TranslatedContentForm';
import { FiSave, FiArrowLeft, FiGlobe, FiLayers } from 'react-icons/fi';
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
  const url = createEntityUrl('experiments', experimentId);
  const [experimentResource, error, loading, fetchData] = useFetch(url, 'GET', null);
  const [saveExperiment, { loading: saveLoading, error: saveError }] = useMutation<Experiment>(
    url,
    experimentId ? 'PUT' : 'POST'
  );

  const experiment = useBoundStore(state => state.experiment);
  const setExperiment = useBoundStore(state => state.setExperiment);
  const patchExperiment = useBoundStore(state => state.patchExperiment);

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
      const savedExperiment = await saveExperiment(experiment);
      setSuccess(true);
      setExperiment(savedExperiment);
    } catch (err) {
      console.error(err);
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
        {saveError && <div className="text-red-600 mb-4">{saveError}</div>}

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
          onTabChange={handleTabChange}
        />

        <div className="mt-4 px-2">
          <Routes>
            <Route
              path="translated-content/:language?"
              element={
                <TranslatedContentForm
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

        <Button
          type="submit"
          disabled={saveLoading}
          variant="success"
          icon={<FiSave />}
          className="mt-5"
        >
          {saveLoading ? 'Saving...' : (experimentId ? 'Update Experiment' : 'Create Experiment')}
        </Button>
      </form>
    </Page>
  );
};

export default ExperimentForm;
