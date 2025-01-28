import React from 'react';
import { Question, QuestionInSeries } from '../../types/types';
import { FormField } from '../form/FormField';
import { useQuestionDragAndDrop } from '../../hooks/useQuestionDragAndDrop';

interface SelectedQuestionsTableProps {
  questions: QuestionInSeries[];
  availableQuestions: Question[];
  onQuestionsChange: (questions: QuestionInSeries[]) => void;
  onRemoveQuestion: (key: string) => void;
}

export function SelectedQuestionsTable({
  questions,
  availableQuestions,
  onQuestionsChange,
  onRemoveQuestion,
}: SelectedQuestionsTableProps) {
  const {
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDragLeave,
    handleDrop,
  } = useQuestionDragAndDrop(questions, onQuestionsChange);

  if (questions.length === 0) return null;

  return (
    <FormField label="Selected Questions">
      <div className="mt-2 border rounded">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-4 py-2 text-left"></th>
              <th className="px-4 py-2 text-left">Question</th>
              <th className="px-4 py-2 text-left">Index</th>
              <th className="px-4 py-2 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {questions.map((q) => {
              const question = availableQuestions.find(aq => aq.key === q.key);
              return (
                <tr
                  key={q.key}
                  draggable
                  title="Drag to reorder"
                  onDragStart={(e) => handleDragStart(e, q.key)}
                  onDragEnd={handleDragEnd}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={(e) => handleDrop(e, q.key)}
                  className="border-t group"
                >
                  <td className="px-4 py-2 text-center cursor-move select-none transition-colors text-gray-500 group-hover:text-black">
                    <div className="w-full h-full">⠿</div>
                  </td>
                  <td className="px-4 py-2">{question?.question}</td>
                  <td className="px-4 py-2">
                    <input
                      type="number"
                      min="0"
                      value={q.index}
                      onChange={(e) => {
                        const newIndex = parseInt(e.target.value);
                        const updatedQuestions = questions.map(question =>
                          question.key === q.key
                            ? { ...question, index: newIndex }
                            : question
                        );
                        onQuestionsChange(updatedQuestions);
                      }}
                      className="w-20 px-2 py-1 border rounded"
                    />
                  </td>
                  <td className="px-4 py-2 text-center">
                    <button
                      type="button"
                      onClick={() => onRemoveQuestion(q.key)}
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
  );
}
