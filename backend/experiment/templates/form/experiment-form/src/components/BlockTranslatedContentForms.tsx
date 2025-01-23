import React from 'react';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';
import { BlockTranslatedContent } from '../types/types';
import { Flag } from './Flag';
import { BlockTranslatedContentForm } from './BlockTranslatedContentForm';

interface BlockTranslatedContentFormsProps {
  contents: BlockTranslatedContent[];
  onChange: (contents: BlockTranslatedContent[]) => void;
}

const defaultContent: BlockTranslatedContent = {
  index: 0,
  language: '',
  name: '',
  description: '',
};

export const BlockTranslatedContentForms: React.FC<BlockTranslatedContentFormsProps> = ({ contents, onChange }) => {
  const [activeTabIndex, setActiveTabIndex] = React.useState(0);

  const handleAdd = () => {
    const newContent = {
      ...defaultContent,
      index: contents.length,
    };
    const updatedContents = [...contents, newContent].map((content, index) => ({ ...content, index }));
    onChange(updatedContents);
    setActiveTabIndex(updatedContents.length - 1);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this translation?')) {
      onChange(contents.filter((_, i) => i !== index));
      setActiveTabIndex(Math.min(index, contents.length - 2));
    }
  };

  const handleChange = (index: number, newContent: BlockTranslatedContent) => {
    const updatedContents = contents.map((content, i) => {
      if (i === index) {
        return { ...content, ...newContent };
      }
      return content;
    });
    onChange(updatedContents);
  };

  const getTabLabel = (content: BlockTranslatedContent, index: number) => {
    if (content.language) {
      return <Flag languageCode={content.language} showLabel={true} />;
    }
    return `Translation ${index + 1}`;
  };

  const handleTabChange = (tabIndex: string | number) => {
    if (tabIndex === 'new') {
      handleAdd();
    } else {
      setActiveTabIndex(tabIndex as number);
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
        <BlockTranslatedContentForm
          content={contents[activeTabIndex]}
          onChange={(content) => handleChange(activeTabIndex, content)}
        />
      )}
    </div>
  );
};
