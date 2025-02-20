import React, { useState } from 'react';
import { QuestionTypeEnum, QuestionData, QuestionChoice } from '../types/types';
import { Button } from './Button';
import { FiMinus, FiPlus, FiSave } from 'react-icons/fi';
import { Input } from './form/Input';

interface QuestionFormProps {
  initialData?: QuestionData & {
    choices?: QuestionChoice[];
    explainer?: string;
    scale_steps?: number;
    profile_scoring_rule?: string;
    min_value?: number;
    max_value?: number;
    max_length?: number;
    min_values?: number;
    view?: string;
    is_skippable?: boolean;
  };
  onSubmit: (data: QuestionData & {
    choices?: QuestionChoice[];
    explainer?: string;
    scale_steps?: number;
    profile_scoring_rule?: string;
    min_value?: number;
    max_value?: number;
    max_length?: number;
    min_values?: number;
    view?: string;
    is_skippable?: boolean;
  }) => void;
  className?: string;
  error?: { [key: string]: string };
  loading?: boolean;
}

export function QuestionForm({ className = "bg-white p-4", initialData, onSubmit, error }: QuestionFormProps) {
  const [questionKey, setQuestionKey] = useState(initialData?.key || '');
  const [questionText, setQuestionText] = useState(initialData?.question || '');
  const [questionType, setQuestionType] = useState(initialData?.type || '');
  const [choices, setChoices] = useState<QuestionChoice[]>(initialData?.choices || []);
  // Optional fields
  const [explainer, setExplainer] = useState(initialData?.explainer || '');
  const [scaleSteps, setScaleSteps] = useState(initialData?.scale_steps || 7);
  const [profileScoringRule, setProfileScoringRule] = useState(initialData?.profile_scoring_rule || '');
  const [minValue, setMinValue] = useState(initialData?.min_value || 0);
  const [maxValue, setMaxValue] = useState(initialData?.max_value || 120);
  const [maxLength, setMaxLength] = useState(initialData?.max_length || 64);
  const [minValues, setMinValues] = useState(initialData?.min_values || 1);
  const [view, setView] = useState(initialData?.view || '');
  const [isSkippable, setIsSkippable] = useState(initialData?.is_skippable || false);

  // Helper functions to control advanced input visibility based on questionType:
  const shouldShowScaleSteps = questionType === QuestionTypeEnum.LikertQuestion || questionType === QuestionTypeEnum.LikertQuestionIcon;
  const shouldShowProfileScoringRule = shouldShowScaleSteps;
  const shouldShowMinMaxValues = questionType === QuestionTypeEnum.NumberQuestion;
  const shouldShowMaxLength = questionType === QuestionTypeEnum.TextQuestion;
  const shouldShowChoiceAdvanced = questionType === QuestionTypeEnum.ChoiceQuestion;

  const handleAddChoice = () => {
    setChoices([...choices, { key: '', text: '', index: choices.length }]);
  };

  const handleChoiceChange = (idx: number, field: 'key' | 'text', value: string) => {
    const newChoices = choices.map((choice, i) =>
      i === idx ? { ...choice, [field]: value } : choice
    );
    setChoices(newChoices);
  };

  const handleRemoveChoice = (idx: number) => {
    const newChoices = choices.filter((_, i) => i !== idx)
      .map((choice, i) => ({ ...choice, index: i }));
    setChoices(newChoices);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const submissionData: QuestionData = {
      key: questionKey,
      question: questionText,
      type: questionType as QuestionTypeEnum,
      choices,
      explainer,
      is_skippable: isSkippable
    }

    if (shouldShowMinMaxValues) {
      submissionData.min_value = minValue;
      submissionData.max_value = maxValue;
    }

    if (shouldShowChoiceAdvanced) {
      submissionData.view = view;
    }

    if (shouldShowProfileScoringRule) {
      submissionData.profile_scoring_rule = profileScoringRule;
    }

    if (shouldShowScaleSteps) {
      submissionData.scale_steps = scaleSteps;
    }

    if (shouldShowMaxLength) {
      submissionData.max_length = maxLength;
    }

    onSubmit(submissionData);
  };

  return (
    <form onSubmit={handleSubmit} className={className}>
      {/* Question Key */}
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Question Key</label>
        <Input
          type="text"
          placeholder="UNIQUE_QUESTION_KEY"
          value={questionKey}
          onChange={(e) => setQuestionKey(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          required
        />
        {error?.key && <p className="text-red-500 text-sm mt-1">{error.key}</p>}
      </div>

      {/* Question Text */}
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Question Text</label>
        <input
          type="text"
          placeholder="What is your favorite color?"
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          required
        />
        {error?.question && <p className="text-red-500">{error.question}</p>}
      </div>

      {/* Question Type */}
      <div className="mb-4">
        <label className="block text-gray-700 mb-1">Question Type</label>
        <select
          value={questionType}
          onChange={(e) => setQuestionType(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          required
        >
          <option value="">Select type</option>
          {Object.keys(QuestionTypeEnum).map((type) => (
            <option key={type} value={QuestionTypeEnum[type as keyof typeof QuestionTypeEnum]}>
              {QuestionTypeEnum[type as keyof typeof QuestionTypeEnum]}
            </option>
          ))}
        </select>
      </div>

      {/* Advanced Options */}
      <fieldset className="mb-4 border p-4 rounded">
        <legend className="px-2 text-gray-700">Advanced Options</legend>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1">Explainer</label>
          <input
            type="text"
            value={explainer}
            placeholder="Optional explainer text"
            onChange={(e) => setExplainer(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          />
        </div>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className={shouldShowScaleSteps ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Scale Steps</label>
            <input
              type="number"
              value={scaleSteps}
              onChange={(e) => setScaleSteps(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className={shouldShowProfileScoringRule ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Profile Scoring Rule</label>
            <select
              value={profileScoringRule}
              onChange={(e) => setProfileScoringRule(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Select rule</option>
              <option value="LIKERT">LIKERT</option>
              <option value="REVERSE_LIKERT">REVERSE_LIKERT</option>
              <option value="CATEGORIES_TO_LIKERT">CATEGORIES_TO_LIKERT</option>
            </select>
          </div>
          <div className={shouldShowMinMaxValues ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Min Value</label>
            <input
              type="number"
              value={minValue}
              onChange={(e) => setMinValue(parseFloat(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className={shouldShowMinMaxValues ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Max Value</label>
            <input
              type="number"
              value={maxValue}
              onChange={(e) => setMaxValue(parseFloat(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className={shouldShowMaxLength ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Max Length</label>
            <input
              type="number"
              value={maxLength}
              onChange={(e) => setMaxLength(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className={shouldShowChoiceAdvanced ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">Min Values (for choices)</label>
            <input
              type="number"
              value={minValues}
              onChange={(e) => setMinValues(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className={shouldShowChoiceAdvanced ? '' : 'hidden'}>
            <label className="block text-gray-700 mb-1">View</label>
            <select
              value={view}
              onChange={(e) => setView(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Select view</option>
              <option value="BUTTON_ARRAY">BUTTON_ARRAY</option>
              <option value="CHECKBOXES">CHECKBOXES</option>
              <option value="RADIOS">RADIOS</option>
              <option value="DROPDOWN">DROPDOWN</option>
            </select>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={isSkippable}
              onChange={(e) => setIsSkippable(e.target.checked)}
              className="mr-2"
            />
            <label className="text-gray-700">Is Skippable</label>
          </div>
        </div>
      </fieldset>

      {/* Choices (only for ChoiceQuestion type) */}
      {questionType === QuestionTypeEnum.ChoiceQuestion && (
        <div className="mb-4">
          <label className="block text-gray-700 mb-1">Choices</label>
          {choices.map((choice, idx) => (
            <div key={idx} className="flex mb-2">
              <input
                type="text"
                placeholder="Choice Key"
                value={choice.key}
                onChange={(e) => handleChoiceChange(idx, 'key', e.target.value)}
                className="w-1/3 px-3 py-2 border rounded mr-2"
                required
              />
              <input
                type="text"
                placeholder="Choice Text"
                value={choice.text}
                onChange={(e) => handleChoiceChange(idx, 'text', e.target.value)}
                className="w-1/2 px-3 py-2 border rounded mr-2"
                required
              />
              <Button
                type="button"
                onClick={() => handleRemoveChoice(idx)}
                variant='danger'
                icon={<FiMinus />}
              >
                Remove
              </Button>
            </div>
          ))}
          <Button
            type="button"
            onClick={handleAddChoice}
            icon={<FiPlus />}
          >
            Add Choice
          </Button>
        </div>
      )}

      <div className="h-px bg-gray-300 my-4" />

      <div className="text-right">
        <Button type="submit" icon={<FiSave />}>
          Submit
        </Button>
      </div>
    </form>
  );
}

export default QuestionForm;
