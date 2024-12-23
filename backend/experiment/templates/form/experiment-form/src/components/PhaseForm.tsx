import React from 'react';
import { FormField } from './form/FormField';
import { Phase } from '../types/types';

interface PhaseFormProps {
  phase: Phase;
  onChange: (phase: Phase) => void;
}

export const PhaseForm: React.FC<PhaseFormProps> = ({ phase, onChange }) => {
  const handleChange = (field: keyof Phase, value: any) => {
    onChange({ ...phase, [field]: value });
  };

  return (
    <div className="space-y-5">
      <div className="grid sm:grid-cols-2 gap-5">
        <FormField label="Dashboard">
          <input
            type="checkbox"
            checked={phase.dashboard}
            onChange={(e) => handleChange('dashboard', e.target.checked)}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 h-5 w-5"
          />
        </FormField>

        <FormField label="Randomize">
          <input
            type="checkbox"
            checked={phase.randomize}
            onChange={(e) => handleChange('randomize', e.target.checked)}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 h-5 w-5"
          />
        </FormField>
      </div>
    </div>
  );
};
