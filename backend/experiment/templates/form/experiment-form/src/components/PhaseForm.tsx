import React from 'react';
import { Button } from './Button';
import { FiTrash } from 'react-icons/fi';

interface Phase {
  id?: number;
  index: number;
  dashboard: boolean;
  randomize: boolean;
}

interface PhaseFormProps {
  phase: Phase;
  onDelete: () => void;
  onChange: (phase: Phase) => void;
}

export const PhaseForm: React.FC<PhaseFormProps> = ({
  phase,
  onDelete,
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
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button
          variant="danger"
          size="sm"
          icon={<FiTrash />}
          onClick={onDelete}
        >
          Delete Phase
        </Button>
      </div>

      <div className="space-y-4">
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="dashboard"
            checked={phase.dashboard}
            onChange={handleChange}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span>Show Dashboard</span>
        </label>

        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="randomize"
            checked={phase.randomize}
            onChange={handleChange}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span>Randomize Blocks</span>
        </label>
      </div>
    </div>
  );
};
