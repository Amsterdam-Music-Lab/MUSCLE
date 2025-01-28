import { useState } from 'react';
import { QuestionInSeries } from '../types/types';

export function useQuestionDragAndDrop(questions: QuestionInSeries[], onQuestionsChange: (questions: QuestionInSeries[]) => void) {
  const [draggedQuestionKey, setDraggedQuestionKey] = useState<string | null>(null);

  const handleDragStart = (e: React.DragEvent<HTMLTableRowElement>, questionKey: string) => {
    setDraggedQuestionKey(questionKey);
    e.currentTarget.classList.add('opacity-50');
    if (e.dataTransfer) {
      e.dataTransfer.effectAllowed = 'move';
    }
  };

  const handleDragEnd = (e: React.DragEvent<HTMLTableRowElement>) => {
    e.currentTarget.classList.remove('opacity-50');
    setDraggedQuestionKey(null);
  };

  const handleDragOver = (e: React.DragEvent<HTMLTableRowElement>) => {
    e.preventDefault();
    e.currentTarget.classList.add('border-t-2', 'border-blue-500');
  };

  const handleDragLeave = (e: React.DragEvent<HTMLTableRowElement>) => {
    e.currentTarget.classList.remove('border-t-2', 'border-blue-500');
  };

  const handleDrop = (e: React.DragEvent<HTMLTableRowElement>, targetQuestionKey: string) => {
    e.preventDefault();
    e.currentTarget.classList.remove('border-t-2', 'border-blue-500');

    if (!draggedQuestionKey || draggedQuestionKey === targetQuestionKey) return;

    const updatedQuestions = [...questions];
    const draggedIndex = updatedQuestions.findIndex(q => q.key === draggedQuestionKey);
    const targetIndex = updatedQuestions.findIndex(q => q.key === targetQuestionKey);

    const [draggedQuestion] = updatedQuestions.splice(draggedIndex, 1);
    updatedQuestions.splice(targetIndex, 0, draggedQuestion);

    const reindexedQuestions = updatedQuestions.map((q, idx) => ({
      ...q,
      index: idx
    }));

    onQuestionsChange(reindexedQuestions);
  };

  return {
    draggedQuestionKey,
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDragLeave,
    handleDrop,
  };
}
