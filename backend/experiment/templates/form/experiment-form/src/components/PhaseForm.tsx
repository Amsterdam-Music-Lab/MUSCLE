import React from 'react';
import { FormField } from './form/FormField';
import { Phase } from '../types/types';

interface PhaseFormProps {
  phase: Phase;
  onDelete: () => void;
  onChange: (phase: Phase) => void;
}

export const PhaseForm: React.FC<PhaseFormProps> = ({
  phase,
  onChange,
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, type, checked, value } = e.target;
    onChange({
      ...phase,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  return (
    <div className="grid sm:grid-cols-2 gap-5">
      <FormField label="Show Dashboard">
        <input
          type="checkbox"
          name="dashboard"
          checked={phase.dashboard}
          onChange={handleChange}
          className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
        />
      </FormField>

      <FormField label="Randomize Blocks">
        <input
          type="checkbox"
          name="randomize"
          checked={phase.randomize}
          onChange={handleChange}
          className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
        />
      </FormField>
    </div>
  );
};
