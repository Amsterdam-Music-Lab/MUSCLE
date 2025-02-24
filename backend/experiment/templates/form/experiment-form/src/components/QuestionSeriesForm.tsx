import React, { useEffect, useState } from 'react';
import { BlockQuestionSeries, Question, QuestionData, QuestionGroup, QuestionInSeries, QuestionTypeEnum } from '../types/types';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { API_BASE_URL, createQuestionQuestionAPIUrl } from '../config';
import { SelectedQuestionsTable } from './question-series/SelectedQuestionsTable';
import { AvailableQuestionsTable } from './question-series/AvailableQuestionsTable';
import { FiPlus } from 'react-icons/fi';
import useBoundStore from '../utils/store';
import { Button } from './Button';

interface QuestionSeriesFormProps {
  series: BlockQuestionSeries;
  onChange: (series: BlockQuestionSeries) => void;
}

export function QuestionSeriesForm({ series, onChange }: QuestionSeriesFormProps) {
  const addToast = useBoundStore(state => state.addToast);
  const [availableQuestions, setAvailableQuestions] = useState<Question[]>([]);
  const [questionGroups, setQuestionGroups] = useState<QuestionGroup[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedQuestionKey, setHighlightedQuestionKey] = useState<string | null>(null);
  const [newQuestionText, setNewQuestionText] = useState('');

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
    alert('Not implemented yet');
  };

  const submitNewQuestion = async (
    e: React.KeyboardEvent<HTMLInputElement> | React.MouseEvent<HTMLButtonElement>,
    questionText: string
  ) => {

    e.preventDefault();

    if (!questionText) return;

    // the question key needs to be unique and a valid slug, so we can use the question text as a base and replace spaces with dashes, lowercase it and remove special characters
    const questionKey = questionText
      .toLowerCase()
      .replace(/[^a-z0-9 ]/g, '')
      .replace(/ /g, '_');
    const questionType = QuestionTypeEnum.TextQuestion;
    const newQuestion: QuestionData = {
      key: questionKey,
      question: questionText,
      type: questionType,
    };
    const response = await fetch(createQuestionQuestionAPIUrl('questions'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newQuestion),
    });
    const data = await response.json();

    if (response.ok) {
      setAvailableQuestions([...availableQuestions, data]);
      handleAddQuestion(data.key);
      setNewQuestionText('');
    }

    if (!response.ok) {
      let message = 'Error creating question';

      if (data?.key) {
        message = `Error creating question: ${data.key}`;
      }

      addToast({
        message,
        duration: 5000,
        level: 'error',
      });
      return;
    }
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

        <FormField label="Randomize" className="flex items-start">
          <Input
            type="checkbox"
            checked={series.randomize}
            onChange={(e) => onChange({ ...series, randomize: e.target.checked })}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 h-5 w-5"
          />
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

          <div className="gap-2 flex justify-between items-end" >
            <FormField className="space-y-2 mb-0 w-full" label='Create New Question'>
              <Input
                type="text"
                name="questionText"
                placeholder="What is your favorite artist?"
                className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-200 focus:border-blue-400"
                value={newQuestionText}
                onChange={(e) => setNewQuestionText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && submitNewQuestion(e, newQuestionText)}
              />
            </FormField>
            <Button
              type="button"
              onClick={(e) => submitNewQuestion(e, newQuestionText)}
              className="whitespace-nowrap px-4 py-2 border border-transparent rounded-md bg-blue-600 hover:bg-blue-800 text-white flex items-center gap-1">
              <FiPlus />
              Create New Question
            </Button>
          </div>

        </div>
      </div>
    </div>
  );
}
