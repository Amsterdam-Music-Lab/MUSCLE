import React from 'react';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';
import { BlockQuestionSeries } from '../types/types';
import { QuestionSeriesForm } from './QuestionSeriesForm';

interface QuestionSeriesFormsProps {
  series: BlockQuestionSeries[];
  onChange: (series: BlockQuestionSeries[]) => void;
}

const defaultQuestionSeries: BlockQuestionSeries = {
  id: undefined,
  name: '',
  index: 0,
  randomize: false,
  questions: [],
};

export const QuestionSeriesForms: React.FC<QuestionSeriesFormsProps> = ({ series, onChange }) => {
  const [activeTabIndex, setActiveTabIndex] = React.useState(0);

  const handleAdd = () => {
    const newSeries = {
      ...defaultQuestionSeries,
      index: series.length + 1,
    };
    const updatedSeries = [...series, newSeries].map((s, index) => ({ ...s, index: index + 1 }));
    onChange(updatedSeries);
    setActiveTabIndex(updatedSeries.length - 1);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this question series?')) {
      const updatedSeries = series
        .filter((_, i) => i !== index)
        .map((s, index) => ({ ...s, index: index + 1 }));
      onChange(updatedSeries);
      setActiveTabIndex(Math.min(index, series.length - 2));
    }
  };

  const handleChange = (index: number, newSeries: BlockQuestionSeries) => {
    const updatedSeries = series.map((s, i) => {
      if (i === index) {
        return { ...s, ...newSeries };
      }
      return s;
    });
    onChange(updatedSeries);
  };

  const handleTabChange = (tabIndex: string | number) => {
    if (tabIndex === 'new') {
      handleAdd();
    } else {
      setActiveTabIndex(tabIndex as number);
    }
  };

  return (
    <div className="mt-8">
      <h3 className="text-lg font-medium">Question Series*</h3>

      <div className="mt-4">
        <Tabs
          tabs={[
            ...series.map((s, index) => ({
              id: index,
              label: s.name || `Series ${index + 1}`,
            })),
            {
              id: 'new',
              label: (
                <div className="flex items-center gap-2">
                  <FiPlus className="w-4 h-4" />
                  <span>New Series</span>
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
              title: 'Remove series',
              onClick: (tabId) => handleRemove(tabId as number),
            },
          ]}
        />

      </div>

      {series.length > 0 && !!series[activeTabIndex] && (
        <QuestionSeriesForm
          series={series[activeTabIndex]}
          onChange={(updatedSeries) => handleChange(activeTabIndex, updatedSeries)}
        />
      )}
    </div>
  );
};
