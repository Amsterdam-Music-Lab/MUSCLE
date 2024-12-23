import React from 'react';
import { FiTrash2 } from 'react-icons/fi';
import { Phase } from '../types/types';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Button } from './Button';

interface PhaseFormProps {
  phase: Phase;
  onChange: (phase: Phase) => void;
  onDelete: () => void;
}

export const PhaseForm: React.FC<PhaseFormProps> = ({ phase, onChange, onDelete }) => {
  const handleChange = (field: keyof Phase, value: any) => {
    onChange({ ...phase, [field]: value });
  };

  return (
    <div className="space-y-5">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-medium">Phase Settings</h3>
        <Button
          variant="danger"
          size="sm"
          icon={<FiTrash2 />}
          onClick={onDelete}
        >
          Delete Phase
        </Button>
      </div>

      <div className="grid sm:grid-cols-2 gap-5">
        <FormField label="Index">
          <Input
            type="number"
            value={phase.index}
            onChange={(e) => handleChange('index', parseInt(e.target.value))}
            required
          />
        </FormField>
      </div>

      <div className="space-y-3">
        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={phase.dashboard}
            onChange={(e) => handleChange('dashboard', e.target.checked)}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span>Show Dashboard</span>
        </label>

        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={phase.randomize}
            onChange={(e) => handleChange('randomize', e.target.checked)}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span>Randomize Blocks</span>
        </label>
      </div>
    </div>
  );
};
