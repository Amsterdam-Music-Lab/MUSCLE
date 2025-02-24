import React, { useState, useEffect } from 'react';
import { Phase, Selection } from '../types/types';
import { PhaseForm } from './PhaseForm';
import { Timeline } from './Timeline';
import { BlockForm } from './BlockForm';
import useBoundStore from '../utils/store';
import { useNavigate, useParams, useLocation, Routes, Route } from 'react-router-dom';
import { Button } from './Button';
import { FiPlus } from 'react-icons/fi';

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
  const experiment = useBoundStore(state => state.experiment);
  const [timelineSelection, setTimelineSelection] = useState<Selection | null>(null);
  const navigate = useNavigate();
  const params = useParams();
  const { id: experimentId } = params;
  const location = useLocation();


  useEffect(() => {
    // Parse URL to set initial selection
    const match = location.pathname.match(/\/phases\/(\d+)(?:\/blocks\/(\d+))?/);

    if (match) {
      const [_, phaseIndex, blockIndex] = match;
      if (blockIndex !== undefined) {
        // Set block selection
        setTimelineSelection({
          type: 'block',
          phaseIndex: parseInt(phaseIndex),
          blockIndex: parseInt(blockIndex)
        });
      } else {
        // Set phase selection
        setTimelineSelection({
          type: 'phase',
          phaseIndex: parseInt(phaseIndex)
        });
      }
    } else if (phases.length > 0) {


      // Default to first phase if no selection in URL
      navigate(`/experiments/${experimentId}/phases/0`);
    }
  }, [location.pathname, phases]);

  const handleTimelineSelect = (selection: Selection) => {

    setTimelineSelection(selection);
    const basePath = `/experiments/${experimentId}/phases`;
    if (selection.type === 'block') {
      navigate(`${basePath}/${selection.phaseIndex}/blocks/${selection.blockIndex}`);
    } else {
      navigate(`${basePath}/${selection.phaseIndex}`);
    }
  };

  const addPhaseOrBlock = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    if (type === 'phase') {
      const newPhase: Phase = {
        ...defaultPhase,
        index: phaseIndex,
        blocks: [],
      };

      let updatedPhases = [...phases];

      updatedPhases
        .splice(phaseIndex, 0, newPhase)

      updatedPhases = updatedPhases
        .map((phase, i) => ({ ...phase, index: i }));

      onChange(updatedPhases);
      setTimelineSelection({ type: 'phase', phaseIndex: phaseIndex });
    } else {

      const position = blockIndex !== undefined ? blockIndex : phases[phaseIndex].blocks.length;

      const phase = phases[phaseIndex];
      if (!phase) return;
      if (!experiment) return;

      const experimentSlug = experiment.slug;
      const blockSlugArray: [string, number, number] = [experimentSlug, phaseIndex, position];
      let blockSlug = blockSlugArray.join('-');

      // Check if block slug already exists in the experiment
      while (phase.blocks.some(b => b.slug === blockSlug)) {
        blockSlugArray[1] += 1;
        blockSlug = blockSlugArray.join('-');
      }

      const newBlock = {
        index: position,
        slug: blockSlug,
        rounds: 10,
        bonus_points: 0,
        rules: '',
        translated_contents: [],
        playlists: [],
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

  const handleAdd = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    addPhaseOrBlock(type, phaseIndex, blockIndex);

    // then navigate to the new block (if the index(es) are different than the current selection)
    if (type === 'phase') {
      navigate(`/experiments/${experimentId}/phases/${phaseIndex}`);
    } else {
      navigate(`/experiments/${experimentId}/phases/${phaseIndex}/blocks/${blockIndex}`);
    }
  };

  const deletePhaseOrBlock = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    if (type === 'phase') {
      if (!confirm('Are you sure you want to delete this phase?')) return;

      const updatedPhases = phases.filter((_, i) => i !== phaseIndex)
        .map((phase, i) => ({ ...phase, index: i }));

      setTimelineSelection(null);
      onChange(updatedPhases);

      return updatedPhases;

    } else if (blockIndex !== undefined) {
      if (!confirm('Are you sure you want to delete this block?')) return;

      const phase = phases[phaseIndex];
      const updatedBlocks = phase.blocks
        .filter((_, i) => i !== blockIndex)
        .map((block, i) => ({ ...block, index: i }));

      const updatedPhase = { ...phase, blocks: updatedBlocks };
      const updatedPhases = phases.map((p, i) => i === phaseIndex ? updatedPhase : p);

      setTimelineSelection(null);
      onChange(updatedPhases);

      return updatedPhases;
    }
  };

  const handleDelete = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    const updatedPhases = deletePhaseOrBlock(type, phaseIndex, blockIndex);

    if (!updatedPhases?.length) {
      navigate(`/experiments/${experimentId}/phases`);
      return;
    }

    // navigate to the most appropriate location after deletion
    if (type === 'phase') {
      if (phaseIndex === 0) {
        navigate(`/experiments/${experimentId}/phases/0`);
      } else {
        navigate(`/experiments/${experimentId}/phases/${phaseIndex - 1}`);
      }
    } else {

      if (blockIndex === undefined) {
        navigate(`/experiments/${experimentId}/phases/${phaseIndex}`);
        return;
      }

      if (blockIndex === 0) {
        navigate(`/experiments/${experimentId}/phases/${phaseIndex}`);
      } else {
        navigate(`/experiments/${experimentId}/phases/${phaseIndex}/blocks/${blockIndex - 1}`);
      }
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
        onSelect={handleTimelineSelect}
        onAdd={handleAdd}
      />

      {/* Add new phase button if there are no phases */}
      {!phases.length && (
        <Button
          icon={<FiPlus className="w-4 h-4" />}
          onClick={() => handleAdd('phase', phases.length)}
        >
          Add Phase
        </Button>
      )}

      <Routes>
        <Route path="/:blocks/:blockIndex" element={
          selected?.type === 'block' && (
            <div className="p-5 bg-gray-50 rounded-md">
              <div className="p-5 border rounded-md bg-white">
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
                  onDelete={() => handleDelete('block', timelineSelection.phaseIndex, timelineSelection.blockIndex)}
                />
              </div>
            </div>
          )
        } />
        <Route path="*" element={
          selected?.type === 'phase' && (
            <div className="p-5 bg-gray-50 rounded-md">
              <div className="p-5 border rounded-md bg-white">
                <PhaseForm
                  onChange={(updatedPhase) => {
                    onChange(phases.map((p, i) =>
                      i === timelineSelection.phaseIndex ? updatedPhase : p
                    ));
                  }}
                  onDelete={() => handleDelete('phase', timelineSelection.phaseIndex)}
                />
              </div>
            </div>
          )
        } />
      </Routes>
    </div>
  );
};
