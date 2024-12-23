import React, { useState } from 'react';
import { Phase, Selection } from '../types/types';
import { PhaseForm } from './PhaseForm';
import { Timeline } from './Timeline';
import { BlockForm } from './BlockForm';

const defaultPhase: Phase = {
  index: 0,
  blocks: [],
  dashboard: false,
  randomize: false,
};

interface PhasesFormProps {
  phases: Phase[];
  onChange: (phases: Phase[]) => void;
}

export const PhasesForm: React.FC<PhasesFormProps> = ({ phases, onChange }) => {
  const [timelineSelection, setTimelineSelection] = useState<Selection | null>(null);

  const handleAdd = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    if (type === 'phase') {
      const newPhase: Phase = {
        ...defaultPhase,
        index: phaseIndex,
        blocks: [],
      };

      const updatedPhases = [...phases];

      updatedPhases
        .splice(phaseIndex, 0, newPhase)
        .map((phase, i) => ({ ...phase, index: i }));

      onChange(updatedPhases);
      setTimelineSelection({ type: 'phase', phaseIndex: phaseIndex });
    } else {

      const position = blockIndex !== undefined ? blockIndex : phases[phaseIndex].blocks.length;

      const phase = phases[phaseIndex];
      if (!phase) return;

      const newBlock = {
        index: position,
        slug: `block-${phase.blocks.length + 1}`,
        rounds: 10,
        bonus_points: 0,
        rules: '',
      };

      // use splice to insert new block at position
      let newBlocks = [...phase.blocks];

      newBlocks
        .splice(position, 0, newBlock)

      newBlocks = newBlocks
        .map((block, i) => ({ ...block, index: i }))

      const updatedPhase = {
        ...phase,
        blocks: [...newBlocks],
      };

      onChange(phases.map((p, i) => i === phaseIndex ? updatedPhase : p));
      setTimelineSelection({ type: 'block', phaseIndex, blockIndex: position });
    }
  };

  // Get selected item details
  const getSelected = () => {

    if (!timelineSelection) return null;

    if (timelineSelection.type === 'phase') {

      if (timelineSelection.phaseIndex >= phases.length) {
        console.warn('Phase index out of range (type: phase)');
        return null;
      }

      const phase = phases[timelineSelection.phaseIndex];
      return { type: 'phase', item: phase };
    }

    if (timelineSelection.type === 'block') {

      if (timelineSelection.phaseIndex >= phases.length) {
        console.warn('Phase index out of range (type: block)');
        return null;
      }

      const phase = phases[timelineSelection.phaseIndex];

      // Check if block index is defined as a number and greater than or equal to 0
      if (typeof timelineSelection.blockIndex !== 'number' || timelineSelection.blockIndex < 0) {
        console.warn('Block index not found');
        return null;
      }

      if (timelineSelection.blockIndex >= phase.blocks.length) {
        console.warn('Block index out of range');
        return null;
      }

      const block = phase.blocks[timelineSelection.blockIndex];

      return { type: 'block', item: block, phase };
    }

    return null;
  };

  const selected = getSelected();

  return (
    <div className="space-y-6">
      <Timeline
        phases={phases}
        selectedItem={timelineSelection}
        onSelect={setTimelineSelection}
        onAdd={handleAdd}
      />

      {selected && (
        <div className="p-5 bg-gray-50 rounded-md">
          <div className="p-5 border rounded-md bg-white">
            {selected.type === 'phase' ? (
              <PhaseForm
                phase={selected.item}
                onChange={(updatedPhase) => {
                  onChange(phases.map((p, i) =>
                    i === timelineSelection.phaseIndex ? updatedPhase : p
                  ));
                }}
              />
            ) : (
              <BlockForm
                block={selected.item}
                onChange={(updatedBlock) => {
                  const updatedPhase = {
                    ...selected.phase,
                    blocks: selected.phase.blocks.map((b, i) =>
                      i === timelineSelection.blockIndex ? updatedBlock : b
                    ),
                  };
                  onChange(phases.map((p, i) =>
                    i === timelineSelection.phaseIndex ? updatedPhase : p
                  ));
                }}
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
};
