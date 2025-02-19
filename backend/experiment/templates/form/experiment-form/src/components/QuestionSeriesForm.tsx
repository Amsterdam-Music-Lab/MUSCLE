import React, { useEffect, useState } from 'react';
import { BlockQuestionSeries, Question, QuestionGroup } from '../types/types';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { API_BASE_URL } from '../config';
import { SelectedQuestionsTable } from './question-series/SelectedQuestionsTable';
import { AvailableQuestionsTable } from './question-series/AvailableQuestionsTable';
import { FiPlus } from 'react-icons/fi';

interface QuestionSeriesFormProps {
  series: BlockQuestionSeries;
  onChange: (series: BlockQuestionSeries) => void;
}

export function QuestionSeriesForm({ series, onChange }: QuestionSeriesFormProps) {
  const [availableQuestions, setAvailableQuestions] = useState<Question[]>([]);
  const [questionGroups, setQuestionGroups] = useState<QuestionGroup[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedQuestionKey, setHighlightedQuestionKey] = useState<string | null>(null);

  useEffect(() => {
    fetch(API_BASE_URL + '/experiment/api/questions/')
      .then(res => res.json())
      .then(data => {
        setAvailableQuestions(data.questions);
        setQuestionGroups(data.questionGroups);
      });
  }, []);

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

  const filteredQuestions = availableQuestions
    .filter(q => !series.questions.some(sq => sq.key === q.key))
    .filter(q =>
      q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.key.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.type.toLowerCase().includes(searchQuery.toLowerCase())
    );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    if (filteredQuestions.length > 0) {
      setHighlightedQuestionKey(filteredQuestions[0].key);
    } else {
      setHighlightedQuestionKey(null);
    }
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && highlightedQuestionKey) {
      e.preventDefault();
      handleAddQuestion(highlightedQuestionKey);
      setSearchQuery('');
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const currentIndex = filteredQuestions.findIndex(q => q.key === highlightedQuestionKey);
      let newIndex;

      if (e.key === 'ArrowDown') {
        newIndex = currentIndex < filteredQuestions.length - 1 ? currentIndex + 1 : 0;
      } else {
        newIndex = currentIndex > 0 ? currentIndex - 1 : filteredQuestions.length - 1;
      }

      setHighlightedQuestionKey(filteredQuestions[newIndex]?.key || null);
    }
  };

  const createNewQuestion = () => {
    throw new Error('Function not implemented.');
  };

  const submitNewQuestion = (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const questionText = formData.get('questionText') as string;
    const questionKey = questionText.toLowerCase().replace(/\s+/g, '_');
    const questionType = 'text'; // Default type, can be changed later
    const newQuestion = {
      key: questionKey,
      question: questionText,
      type: questionType,
    };

    // TODO: Post new question to the server
    throw new Error('Function not implemented.');
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
          <SelectedQuestionsTable
            questions={series.questions}
            availableQuestions={availableQuestions}
            onQuestionsChange={(questions) => onChange({ ...series, questions })}
            onRemoveQuestion={handleRemoveQuestion}
          />

          <AvailableQuestionsTable
            questions={filteredQuestions}
            searchQuery={searchQuery}
            highlightedQuestionKey={highlightedQuestionKey}
            onSearch={handleSearch}
            onSearchKeyDown={handleSearchKeyDown}
            onAddQuestion={handleAddQuestion}
            onCreateNewQuestion={createNewQuestion}
          />

          <form className="gap-2 flex items-end" onSubmit={submitNewQuestion}>
            <div className="space-y-2">
              <label className="text-gray-700 text-sm font-semibold">Create New Question</label>
              <input
                type="text"
                name="questionText"
                placeholder="What is your favorite artist?"
                className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-200 focus:border-blue-400"
              />
            </div>
            <button onClick={createNewQuestion} className="whitespace-nowrap px-4 py-2 border border-transparent rounded-md bg-blue-600 hover:bg-blue-800 text-white flex items-center gap-1">
              <FiPlus />
              Create New Question
            </button>
          </form>

        </div>
      </div>
    </div>
  );
}
