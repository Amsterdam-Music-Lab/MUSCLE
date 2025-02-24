import React from 'react';
import { Question } from '../../types/types';
import { FormField } from '../form/FormField';
import { FiExternalLink, FiPlus } from 'react-icons/fi';
import { Button } from '../Button';
import { Link } from 'react-router-dom';

interface AvailableQuestionsTableProps {
  questions: Question[];
  searchQuery: string;
  highlightedQuestionKey: string | null;
  onSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSearchKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onAddQuestion: (key: string) => void;
  onCreateNewQuestion: () => void;
}

export function AvailableQuestionsTable({
  questions,
  searchQuery,
  highlightedQuestionKey,
  onSearch,
  onSearchKeyDown,
  onAddQuestion,
  onCreateNewQuestion,
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
                    <Button
                      type="button"
                      onClick={() => onAddQuestion(question.key)}
                      variant='successText'
                      className='whitespace-nowrap'
                      title="Add question"
                    >
                      Add +
                    </Button>
                    <Link
                      to={`/questions/${question.key}/edit`}
                      target='_blank'
                      className="flex items-center gap-1 text-indigo-600 hover:text-indigo-500 whitespace-nowrap px-3 py-1.5"
                      title="Edit question"
                    >
                      Edit
                      <FiExternalLink />
                    </Link>
                  </td>
                </tr>
              ))}
              {questions.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-4 py-2 text-center text-gray-500">
                    No questions found. Try a different search term
                    {onCreateNewQuestion ? (
                      <>
                        or
                        <button
                          type="button"
                          className="text-blue-600 hover:text-blue-800 ml-2 inline-flex items-center gap-1"
                          onClick={onCreateNewQuestion}
                        >
                          Create a New Question
                          <FiPlus />
                        </button>
                      </>
                    ) : ''}
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
