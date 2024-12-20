import React, { useState } from 'react';
import { ISO_LANGUAGES } from '../constants';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';
import { Button } from './Button';

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
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium">Translated Content</h3>
        <Button
          onClick={handleAdd}
          variant="primary"
          icon={<FiPlus />}
        >
          Add Translation
        </Button>
      </div>

      {contents.length > 0 && (
        <>
          <Tabs
            tabs={contents.map((content, index) => ({
              id: index,
              label: getTabLabel(content, index),
            }))}
            activeTab={activeTabIndex}
            onTabChange={(tabId) => setActiveTabIndex(tabId as number)}
            actions={[
              {
                icon: <FiTrash className="w-4 h-4" />,
                title: 'Remove translation',
                onClick: (tabId) => handleRemove(tabId as number),
              },
            ]}
          />

          <div className="p-4 border rounded-md space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Language
                  <select
                    value={contents[activeTabIndex].language}
                    onChange={(e) => handleChange(activeTabIndex, 'language', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  >
                    <option value="">Select language</option>
                    {Object.entries(ISO_LANGUAGES).map(([code, name]) => (
                      <option key={code} value={code}>
                        {name}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Name
                  <input
                    type="text"
                    value={contents[activeTabIndex].name}
                    onChange={(e) => handleChange(activeTabIndex, 'name', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Description
                <textarea
                  value={contents[activeTabIndex].description}
                  onChange={(e) => handleChange(activeTabIndex, 'description', e.target.value)}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                About Content
                <textarea
                  value={contents[activeTabIndex].about_content}
                  onChange={(e) => handleChange(activeTabIndex, 'about_content', e.target.value)}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Social Media Message
                <input
                  type="text"
                  value={contents[activeTabIndex].social_media_message}
                  onChange={(e) => handleChange(activeTabIndex, 'social_media_message', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </label>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
