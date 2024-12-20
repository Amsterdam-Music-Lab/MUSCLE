import React, { useState } from 'react';
import { FormField } from './form/FormField';
import { Phase, Block } from '../types/types';
import { BlockForm } from './BlockForm';
import { Tabs } from './Tabs';
import { FiPlus, FiTrash } from 'react-icons/fi';

interface PhaseFormProps {
  phase: Phase;
  onDelete: () => void;
  onChange: (phase: Phase) => void;
}

const defaultBlock: Block = {
  index: 0,
  slug: '',
  rounds: 10,
  bonus_points: 0,
  rules: '',
};

export const PhaseForm: React.FC<PhaseFormProps> = ({ phase, onChange }) => {
  const [activeBlockIndex, setActiveBlockIndex] = useState(0);

  const handleChange = (field: keyof Phase, value: any) => {
    onChange({ ...phase, [field]: value });
  };

  const handleAddBlock = () => {
    const newBlock = {
      ...defaultBlock,
      index: phase.blocks?.length || 0,
    };
    const blocks = [...(phase.blocks || []), newBlock];
    handleChange('blocks', blocks);
    setActiveBlockIndex(blocks.length - 1);
  };

  const handleBlockChange = (index: number, updatedBlock: Block) => {
    const blocks = (phase.blocks || []).map((block, i) => 
      i === index ? updatedBlock : block
    );
    handleChange('blocks', blocks);
  };

  const handleBlockDelete = (index: number) => {
    if (confirm('Are you sure you want to remove this block?')) {
      const blocks = (phase.blocks || []).filter((_, i) => i !== index);
      handleChange('blocks', blocks);
      setActiveBlockIndex(Math.max(0, activeBlockIndex - 1));
    }
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

      <div className="mt-8">
        <h4 className="text-lg font-medium mb-4">Blocks</h4>
        
        <Tabs
          tabs={[
            ...(phase.blocks || []).map((_, index) => ({
              id: index,
              label: `Block ${index + 1}`,
            })),
            {
              id: 'new',
              label: (
                <div className="flex items-center gap-2">
                  <FiPlus className="w-4 h-4" />
                  <span>New Block</span>
                </div>
              ),
            }
          ]}
          activeTab={activeBlockIndex}
          onTabChange={(tabId) => {
            if (tabId === 'new') {
              handleAddBlock();
            } else {
              setActiveBlockIndex(tabId as number);
            }
          }}
          actions={[
            {
              icon: <FiTrash className="w-4 h-4" />,
              title: 'Remove block',
              onClick: (tabId) => handleBlockDelete(tabId as number),
            },
          ]}
        />

        {phase.blocks && phase.blocks.length > 0 && (
          <div className="mt-4">
            <BlockForm
              block={phase.blocks[activeBlockIndex]}
              onChange={(updatedBlock) => handleBlockChange(activeBlockIndex, updatedBlock)}
            />
          </div>
        )}
      </div>
    </div>
  );
};
