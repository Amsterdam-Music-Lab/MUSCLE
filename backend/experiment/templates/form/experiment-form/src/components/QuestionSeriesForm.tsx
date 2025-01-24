import React from 'react';
import { BlockQuestionSeries } from '../types/types';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';

interface QuestionSeriesFormProps {
  series: BlockQuestionSeries;
  onChange: (series: BlockQuestionSeries) => void;
}

export function QuestionSeriesForm({ series, onChange }: QuestionSeriesFormProps) {
  const handleQuestionSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedQuestions = Array.from(e.target.selectedOptions, option => option.value);
    onChange({ ...series, questions: selectedQuestions });
  };

  return (
    <div className='p-5 bg-gray-50 mt-4'>
      <div className="p-5 bg-white border rounded-md space-y-5">
        <div className="grid sm:grid-cols-2 gap-5">
          <FormField label="Name">
            <Input
              type="text"
              value={series.name}
              onChange={(e) => onChange({ ...series, name: e.target.value })}
              required
            />
          </FormField>

          <FormField label="Index">
            <Input
              type="number"
              value={series.index}
              onChange={(e) => onChange({ ...series, index: parseInt(e.target.value) })}
              required
            />
          </FormField>
        </div>

        <FormField label="Randomize">
          <label className="flex items-center space-x-3">
            <input
              type="checkbox"
              checked={series.randomize}
              onChange={(e) => onChange({ ...series, randomize: e.target.checked })}
              className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 h-5 w-5"
            />
            <span className="text-gray-700">Randomize questions</span>
          </label>
        </FormField>

        <FormField label="Questions">
          <Select
            multiple
            value={series.questions}
            onChange={handleQuestionSelect}
            required
            className="min-h-[200px]"
          >
            {/* You'll need to fetch the available questions from your API */}
            {series.questions.map((question) => (
              <option key={question} value={question}>
                {question}
              </option>
            ))}
          </Select>
        </FormField>
      </div>
    </div>
  );
}
