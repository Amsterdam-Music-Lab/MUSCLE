import React, { useState } from 'react';
import { QuestionTypeEnum, QuestionData, QuestionChoice } from '../types/types';
import { Button } from './Button';
import { FiMinus, FiPlus, FiSave } from 'react-icons/fi';
import { Input } from './form/Input';
import { FormField } from './form/FormField';
import { Select } from './form/Select';
import { Checkbox } from './form/Checkbox';

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
      <FormField label="Question Key" error={error?.key} >
        <Input
          type="text"
          placeholder="UNIQUE_QUESTION_KEY"
          value={questionKey}
          onChange={(e) => setQuestionKey(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          required
        />
      </FormField>

      {/* Question Text */}
      <FormField label="Question Text" error={error?.question} >
        <input
          type="text"
          placeholder="What is your favorite color?"
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          required
        />
      </FormField>

      {/* Question Type */}
      <FormField label="Question Type" error={error?.type} >
        <Select
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
        </Select>
      </FormField>

      {/* Advanced Options */}
      <fieldset className="mb-4 border p-4 rounded">
        <legend className="px-2 text-gray-700">Advanced Options</legend>
        <FormField label="Explainer" error={error?.explainer} >
          <Input
            type="text"
            value={explainer}
            placeholder="Optional explainer text"
            onChange={(e) => setExplainer(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          />
        </FormField>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <FormField className={shouldShowScaleSteps ? '' : 'hidden'} label="Scale Steps" error={error?.scale_steps} >
            <input
              type="number"
              value={scaleSteps}
              onChange={(e) => setScaleSteps(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </FormField>
          <FormField className={shouldShowProfileScoringRule ? '' : 'hidden'} label="Profile Scoring Rule" error={error?.profile_scoring_rule} >
            <Select
              value={profileScoringRule}
              onChange={(e) => setProfileScoringRule(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Select rule</option>
              <option value="LIKERT">LIKERT</option>
              <option value="REVERSE_LIKERT">REVERSE_LIKERT</option>
              <option value="CATEGORIES_TO_LIKERT">CATEGORIES_TO_LIKERT</option>
            </Select>
          </FormField>
          <FormField className={shouldShowMinMaxValues ? '' : 'hidden'} label="Min Value" error={error?.min_value} >
            <Input
              type="number"
              value={minValue}
              onChange={(e) => setMinValue(parseFloat(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </FormField>
          <FormField className={shouldShowMinMaxValues ? '' : 'hidden'} label="Max Value" error={error?.max_value} >
            <Input
              type="number"
              value={maxValue}
              onChange={(e) => setMaxValue(parseFloat(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </FormField>
          <FormField className={shouldShowMaxLength ? '' : 'hidden'} label="Max Length" error={error?.max_length} >
            <Input
              type="number"
              value={maxLength}
              onChange={(e) => setMaxLength(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </FormField>
          <FormField className={shouldShowChoiceAdvanced ? '' : 'hidden'} label="Min Values" error={error?.min_values} >
            <Input
              type="number"
              value={minValues}
              onChange={(e) => setMinValues(parseInt(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </FormField>
          <FormField className={shouldShowChoiceAdvanced ? '' : 'hidden'} label="View" error={error?.view} >
            <Select
              value={view}
              onChange={(e) => setView(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Select view</option>
              <option value="BUTTON_ARRAY">BUTTON_ARRAY</option>
              <option value="CHECKBOXES">CHECKBOXES</option>
              <option value="RADIOS">RADIOS</option>
              <option value="DROPDOWN">DROPDOWN</option>
            </Select>
          </FormField>
          <FormField className="flex items-center" label="Is Skippable" error={error?.is_skippable} >
            <Checkbox
              checked={isSkippable}
              onChange={(e) => setIsSkippable(e.target.checked)}
              className="mr-2"
            />
          </FormField>
        </div>
        {/* Choices (only for ChoiceQuestion type) */}
        {questionType === QuestionTypeEnum.ChoiceQuestion && (
          <FormField className="mb-4" label="Choices" error={error?.choices} >
            {choices.map((choice, idx) => (
              <div key={idx} className="flex mb-2">
                <Input
                  type="text"
                  placeholder="Choice Key"
                  value={choice.key}
                  onChange={(e) => handleChoiceChange(idx, 'key', e.target.value)}
                  className="w-1/3 px-3 py-2 border rounded mr-2"
                  required
                />
                <Input
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
                  variant="dangerText"
                  icon={<FiMinus />}
                >
                  Remove
                </Button>
              </div>
            ))}
            {choices.length === 0 && <p className="text-gray-500">No choices added yet.</p>}
            <Button
              type="button"
              onClick={handleAddChoice}
              icon={<FiPlus />}
              className="mt-2"
            >
              Add Choice
            </Button>
          </FormField>
        )}
      </fieldset>


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
