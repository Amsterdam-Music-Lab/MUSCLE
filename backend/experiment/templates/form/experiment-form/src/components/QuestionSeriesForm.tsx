import React, { useEffect, useState } from 'react';
import { BlockQuestionSeries, Question, QuestionGroup } from '../types/types';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { API_BASE_URL } from '../config';


interface QuestionSeriesFormProps {
  series: BlockQuestionSeries;
  onChange: (series: BlockQuestionSeries) => void;
}

export function QuestionSeriesForm({ series, onChange }: QuestionSeriesFormProps) {
  const [availableQuestions, setAvailableQuestions] = useState<Question[]>([]);
  const [questionGroups, setQuestionGroups] = useState<QuestionGroup[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<string>('');

  useEffect(() => {
    // Fetch available questions and groups
    fetch(API_BASE_URL + '/experiment/api/questions/')
      .then(res => res.json())
      .then(data => {
        setAvailableQuestions(data.questions);
        setQuestionGroups(data.questionGroups);
      });
  }, []);

  const handleQuestionSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedQuestionKeys = Array.from(e.target.selectedOptions, option => option.value);
    const existingQuestions = series.questions.reduce((acc, q) => ({ ...acc, [q.key]: q }), {} as Record<string, QuestionInSeries>);

    const updatedQuestions = selectedQuestionKeys.map((key, idx) => ({
      key,
      index: existingQuestions[key]?.index ?? idx
    }));

    onChange({ ...series, questions: updatedQuestions });
  };

  const handleGroupSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const groupKey = e.target.value;
    setSelectedGroup(groupKey);

    if (groupKey) {
      const group = questionGroups.find(g => g.key === groupKey);
      if (group) {
        const existingQuestions = series.questions.reduce((acc, q) => ({ ...acc, [q.key]: q }), {} as Record<string, QuestionInSeries>);
        const newQuestions = [...new Set([...series.questions.map(q => q.key), ...group.questions])].map((key, idx) => ({
          key,
          index: existingQuestions[key]?.index ?? idx
        }));
        onChange({ ...series, questions: newQuestions });
      }
    }
  };

  const handleAddQuestion = (questionKey: string) => {
    const existingQuestions = series.questions;
    const maxIndex = Math.max(...existingQuestions.map(q => q.index), -1);

    const newQuestions = [...existingQuestions, {
      key: questionKey,
      index: maxIndex + 1
    }];

    onChange({ ...series, questions: newQuestions });
  };

  const handleRemoveQuestion = (questionKey: string) => {
    const updatedQuestions = series.questions
      .filter(q => q.key !== questionKey)
      .map((q, idx) => ({ ...q, index: idx })); // Reindex remaining questions

    onChange({ ...series, questions: updatedQuestions });
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

        <FormField label="Add Questions from Group">
          <Select
            value={selectedGroup}
            onChange={handleGroupSelect}
            className="w-full"
          >
            <option value="">Select a question group</option>
            {questionGroups.map((group) => (
              <option key={group.key} value={group.key}>
                {group.key}
              </option>
            ))}
          </Select>
        </FormField>

        <div className="space-y-6">
          {/* Selected Questions Table */}
          {series.questions.length > 0 && (
            <FormField label="Selected Questions">
              <div className="mt-2 border rounded">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-2 text-left">Question</th>
                      <th className="px-4 py-2 text-left">Index</th>
                      <th className="px-4 py-2 text-center">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {series.questions.map((q) => {
                      const question = availableQuestions.find(aq => aq.key === q.key);
                      return (
                        <tr key={q.key} className="border-t">
                          <td className="px-4 py-2">{question?.question}</td>
                          <td className="px-4 py-2">
                            <input
                              type="number"
                              min="0"
                              value={q.index}
                              onChange={(e) => {
                                const newIndex = parseInt(e.target.value);
                                const updatedQuestions = series.questions.map(question =>
                                  question.key === q.key
                                    ? { ...question, index: newIndex }
                                    : question
                                );
                                onChange({ ...series, questions: updatedQuestions });
                              }}
                              className="w-20 px-2 py-1 border rounded"
                            />
                          </td>
                          <td className="px-4 py-2 text-center">
                            <button
                              type="button"
                              onClick={() => handleRemoveQuestion(q.key)}
                              className="text-red-600 hover:text-red-800 p-1 whitespace-nowrap"
                              title="Remove question"
                            >
                              Remove -
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </FormField>
          )}

          {/* Available Questions Table */}
          <FormField label="Available Questions">
            <div className="mt-2 border rounded max-h-[400px] overflow-y-auto">
              <table className="w-full">
                <thead className="sticky top-0 bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left">Question</th>
                    <th className="px-4 py-2 text-left">Type</th>
                    <th className="px-4 py-2 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {availableQuestions
                    .filter(q => !series.questions.some(sq => sq.key === q.key))
                    .map((question) => (
                      <tr key={question.key} className="border-t">
                        <td className="px-4 py-2">{question.question}</td>
                        <td className="px-4 py-2">{question.type}</td>
                        <td className="px-4 py-2 text-center">
                          <button
                            type="button"
                            onClick={() => handleAddQuestion(question.key)}
                            className="text-green-600 hover:text-green-800 p-1 whitespace-nowrap"
                            title="Add question"
                          >
                            Add +
                          </button>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </FormField>
        </div>
      </div>
    </div>
  );
}
