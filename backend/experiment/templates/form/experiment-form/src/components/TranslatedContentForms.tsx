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
import { TranslatedContentForm } from './TranslatedContentForm';

interface TranslatedContentFormsProps {
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

export const TranslatedContentForms: React.FC<TranslatedContentFormsProps> = ({ contents, onChange }) => {
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
    navigate(`/experiments/${experimentId}/translated-content/${updatedContents.length - 1}`);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this translation?')) {
      onChange(contents.filter((_, i) => i !== index));
      // Navigate to the closest tab
      const nextIndex = Math.min(index, contents.length - 2);
      navigate(`/experiments/${experimentId}/translated-content/${nextIndex}`);
    }
  };

  const handleChange = (index: number, newContent: TranslatedContent) => {
    const updatedContents = contents.map((content, i) => {
      if (i === index) {
        return { ...content, ...newContent };
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
        wrap={true}
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

      {contents.length > 0 && !!contents[activeTabIndex] && (
        <TranslatedContentForm content={contents[activeTabIndex]} onChange={(content) => handleChange(activeTabIndex, content)} />
      )}
    </div>
  );
};
