import React from 'react';
import { Question } from '../../types/types';
import { FormField } from '../form/FormField';

interface AvailableQuestionsTableProps {
  questions: Question[];
  searchQuery: string;
  highlightedQuestionKey: string | null;
  onSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSearchKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onAddQuestion: (key: string) => void;
}

export function AvailableQuestionsTable({
  questions,
  searchQuery,
  highlightedQuestionKey,
  onSearch,
  onSearchKeyDown,
  onAddQuestion,
}: AvailableQuestionsTableProps) {
  return (
    <FormField label="Available Questions">
      <div className="space-y-2">
        <input
          type="text"
          value={searchQuery}
          onChange={onSearch}
          onKeyDown={onSearchKeyDown}
          placeholder="Search questions..."
          className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-blue-200 focus:border-blue-400"
        />
        <div className="border rounded max-h-[400px] overflow-y-auto">
          <table className="w-full">
            <thead className="sticky top-0 bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left">Question</th>
                <th className="px-4 py-2 text-left">Type</th>
                <th className="px-4 py-2 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {questions.map((question) => (
                <tr
                  key={question.key}
                  className={`border-t ${question.key === highlightedQuestionKey
                      ? 'bg-blue-50'
                      : 'hover:bg-gray-50'
                    }`}
                >
                  <td className="px-4 py-2">{question.question}</td>
                  <td className="px-4 py-2">{question.type}</td>
                  <td className="px-4 py-2 text-center">
                    <button
                      type="button"
                      onClick={() => onAddQuestion(question.key)}
                      className="text-green-600 hover:text-green-800 p-1 whitespace-nowrap"
                      title="Add question"
                    >
                      Add +
                    </button>
                  </td>
                </tr>
              ))}
              {questions.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-4 py-2 text-center text-gray-500">
                    No questions found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </FormField>
  );
}
