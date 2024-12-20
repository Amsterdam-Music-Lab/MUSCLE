import React, { useState } from 'react';
import { Phase } from '../types/types';
import { PhaseForm } from './PhaseForm';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';

interface PhasesFormProps {
  phases: Phase[];
  onChange: (phases: Phase[]) => void;
}

const defaultPhase: Phase = {
  index: 0,
  dashboard: false,
  randomize: false,
  blocks: [],
};

export const PhasesForm: React.FC<PhasesFormProps> = ({ phases, onChange }) => {
  const [activePhaseIndex, setActivePhaseIndex] = useState(0);

  const handleAdd = () => {
    const newPhase = {
      ...defaultPhase,
      index: phases.length,
    };
    onChange([...phases, newPhase]);
    setActivePhaseIndex(phases.length);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this phase?')) {
      onChange(phases.filter((_, i) => i !== index));
      setActivePhaseIndex(Math.max(0, activePhaseIndex - 1));
    }
  };

  const handleChange = (index: number, updatedPhase: Phase) => {
    const updatedPhases = phases.map((phase, i) => {
      if (i === index) {
        return { ...updatedPhase, id: phase.id };
      }
      return phase;
    });
    onChange(updatedPhases);
  };

  return (
    <div>
      <h3 className="text-lg font-medium mb-5">Phases</h3>

      <Tabs
        tabs={[
          ...phases.map((_, index) => ({
            id: index,
            label: `Phase ${index + 1}`,
          })),
          {
            id: 'new',
            label: (
              <div className="flex items-center gap-2">
                <FiPlus className="w-4 h-4" />
                <span>New Phase</span>
              </div>
            ),
          }
        ]}
        activeTab={activePhaseIndex}
        onTabChange={(tabId) => {
          if (tabId === 'new') {
            handleAdd();
          } else {
            setActivePhaseIndex(tabId as number);
          }
        }}
        actions={[
          {
            icon: <FiTrash className="w-4 h-4" />,
            title: 'Remove phase',
            onClick: (tabId) => handleRemove(tabId as number),
          },
        ]}
      />

      {phases.length > 0 && (
        <div className='p-5 bg-gray-50'>
          <div className="p-5 border rounded-md bg-white">
            <PhaseForm
              phase={phases[activePhaseIndex]}
              onChange={(updatedPhase) => handleChange(activePhaseIndex, updatedPhase)}
              onDelete={() => handleRemove(activePhaseIndex)}
            />
          </div>
        </div>
      )}
    </div>
  );
};
