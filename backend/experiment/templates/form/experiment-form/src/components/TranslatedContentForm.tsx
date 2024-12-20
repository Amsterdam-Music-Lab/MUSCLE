import React, { useState } from 'react';
import { ISO_LANGUAGES } from '../constants';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { Textarea } from './form/Textarea';

interface TranslatedContent {
  id?: number;
  index: number;
  language: string;
  name: string;
  description: string;
  about_content: string;
  social_media_message: string;
}

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
  const [activeTabIndex, setActiveTabIndex] = useState(0);

  const handleAdd = () => {
    const newContent = {
      ...defaultContent,
      index: contents.length,
    };
    onChange([...contents, newContent]);
    setActiveTabIndex(contents.length);
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
    if (content.language && ISO_LANGUAGES[content.language]) {
      return ISO_LANGUAGES[content.language];
    }
    return `Translation ${index + 1}`;
  };

  return (
    <div className="space-y-5">
      <h3 className="text-lg font-medium">Translated Content</h3>

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
        onTabChange={(tabId) => {
          if (tabId === 'new') {
            handleAdd();
          } else {
            setActiveTabIndex(tabId as number);
          }
        }}
        actions={[
          {
            icon: <FiTrash className="w-4 h-4" />,
            title: 'Remove translation',
            onClick: (tabId) => handleRemove(tabId as number),
          },
        ]}
      />

      {contents.length > 0 && (
        <div className="p-5 border rounded-md space-y-5">
          <div className="flex justify-end">
            {/* ...existing remove button... */}
          </div>

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
      )}
    </div>
  );
};
