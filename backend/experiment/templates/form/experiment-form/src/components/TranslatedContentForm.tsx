import React, { useEffect } from 'react';
import { ISO_LANGUAGES } from '../constants';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { Textarea } from './form/Textarea';
import { TranslatedContent } from '../types/types';
import { Flag } from './Flag';
import { useNavigate, useParams } from 'react-router-dom';

interface TranslatedContentFormProps {
  contents: TranslatedContent[];
  onChange: (contents: TranslatedContent[]) => void;
}

const defaultContent: TranslatedContent = {
  index: 0,
  language: '',
  name: '',
  description: '',
  about_content: '',
  social_media_message: 'I scored {points} points in {experiment_name}!',
};

export const TranslatedContentForm: React.FC<TranslatedContentFormProps> = ({ contents, onChange }) => {
  const navigate = useNavigate();
  const { id: experimentId, language } = useParams();


  // Find index of current language in contents
  const languageInContents = contents.find(content => content.language === language);
  const potentialContentIndex = parseInt(language ?? '0', 10);
  const activeTabIndex = languageInContents ? contents.indexOf(languageInContents) : potentialContentIndex;

  useEffect(() => {
    // If we have contents but no language in URL, redirect to first language
    if (contents.length > 0 && !language) {
      const firstContent = contents[0];
      navigate(`/experiments/${experimentId}/translated-content/${firstContent.language || '0'}`);
    }
  }, [contents, language, experimentId]);

  const handleAdd = () => {
    const newContent = {
      ...defaultContent,
      index: contents.length,
    };
    const updatedContents = [...contents, newContent].map((content, index) => ({ ...content, index }));

    onChange(updatedContents);
    // Navigate to the new content's tab
    navigate(`/experiments/${experimentId}/translated-content/${updatedContents.length}`);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this translation?')) {
      onChange(contents.filter((_, i) => i !== index));
      setActiveTabIndex(Math.max(0, activeTabIndex - 1));
    }
  };

  const handleChange = (index: number, field: keyof TranslatedContent, value: string) => {
    const updatedContents = contents.map((content, i) => {
      if (i === index) {
        return { ...content, [field]: value };
      }
      return content;
    });
    onChange(updatedContents);
  };

  const getTabLabel = (content: TranslatedContent, index: number) => {
    if (content.language) {
      return <Flag languageCode={content.language} showLabel={true} />;
    }
    return `Translation ${index + 1}`;
  };

  const handleTabChange = (tabIndex: string | number) => {
    if (tabIndex === 'new') {
      handleAdd();
    } else {
      const content = contents[tabIndex as number];
      console.log('content', content);
      navigate(`/experiments/${experimentId}/translated-content/${content.language || tabIndex}`);
    }
  };

  return (
    <div className="">
      <h3 className="text-lg font-medium mb-5">
        Translated Content
      </h3>

      <Tabs
        tabs={[
          ...contents.map((content, index) => ({
            id: index,
            label: getTabLabel(content, index),
          })),
          {
            id: 'new',
            label: (
              <div className="flex items-center gap-2">
                <FiPlus className="w-4 h-4" />
                <span>New Translation</span>
              </div>
            ),
          }
        ]}
        activeTab={activeTabIndex}
        onTabChange={handleTabChange}
        actions={[
          {
            icon: <FiTrash className="w-4 h-4" />,
            title: 'Remove translation',
            onClick: (tabId) => handleRemove(tabId as number),
          },
        ]}
      />

      {contents.length > 0 && (
        <div className='p-5 bg-gray-50'>
          <div className="p-5 bg-white border rounded-md space-y-5">

            <div className="grid sm:grid-cols-2 gap-5">
              <FormField label="Language">
                <Select
                  value={contents[activeTabIndex].language}
                  onChange={(e) => handleChange(activeTabIndex, 'language', e.target.value)}
                >
                  <option value="">Select language</option>
                  {Object.entries(ISO_LANGUAGES).map(([code, name]) => (
                    <option key={code} value={code}>
                      {name}
                    </option>
                  ))}
                </Select>
              </FormField>

              <FormField label="Name">
                <Input
                  type="text"
                  value={contents[activeTabIndex].name}
                  onChange={(e) => handleChange(activeTabIndex, 'name', e.target.value)}
                />
              </FormField>
            </div>

            <FormField label="Description">
              <Textarea
                value={contents[activeTabIndex].description}
                onChange={(e) => handleChange(activeTabIndex, 'description', e.target.value)}
                rows={3}
              />
            </FormField>

            <FormField label="About Content">
              <Textarea
                value={contents[activeTabIndex].about_content}
                onChange={(e) => handleChange(activeTabIndex, 'about_content', e.target.value)}
                rows={3}
              />
            </FormField>

            <FormField label="Social Media Message">
              <Input
                type="text"
                value={contents[activeTabIndex].social_media_message}
                onChange={(e) => handleChange(activeTabIndex, 'social_media_message', e.target.value)}
              />
            </FormField>
          </div>
        </div>
      )}
    </div>
  );
};
