import React, { useEffect } from 'react';
import { FiPlus, FiCircle, FiBox } from 'react-icons/fi';
import { Phase, Selection } from '../types/types';

interface TimelineProps {
  phases: Array<Phase>;
  selectedItem: Selection | null;
  onSelect: (selection: Selection) => void;
  onAdd: (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => void;
}

export const Timeline: React.FC<TimelineProps> = ({
  phases,
  selectedItem,
  onSelect,
  onAdd,
}) => {

  useEffect(() => {
    if (!selectedItem && phases.length > 0) {
      onSelect({ type: 'phase', phaseIndex: 0 });
    }
  }, [selectedItem, phases, onSelect]);

  const isSelected = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    return selectedItem?.type === type &&
      selectedItem.phaseIndex === phaseIndex &&
      selectedItem.blockIndex === blockIndex;
  };

  return (
    <div className="w-full overflow-x-auto pt-4">
      <div className="flex items-center p-4 gap-2 min-w-max relative">
        {phases.map((phase, phaseIndex) => (
          <React.Fragment key={phaseIndex}>
            {/* Add button before phase */}
            <div className="-mt-2.5 ml-2.5 z-10">
              {phaseIndex === 0 && (
                <AddButton
                  onClick={() => onAdd('phase', 0)}
                  type="phase"
                />
              )}
            </div>

            <div className={`relative flex items-center gap-1 p-2 pr-5 rounded-full ${phaseIndex === selectedItem?.phaseIndex ? 'bg-blue-100' : 'bg-gray-100'}`}>

              {/* Phase node */}
              <button
                onClick={() => onSelect({ type: 'phase', phaseIndex })}
                type="button"
                className={`
                  relative p-2 rounded-full hover:bg-blue-400 group
                  ${isSelected('phase', phaseIndex) ? 'bg-blue-600' : ''}
                `}
                title={`Phase ${phaseIndex + 1}`}
              >
                <FiCircle className={`w-6 h-6 group-hover:text-white ${isSelected('phase', phaseIndex) ? 'text-white' : 'text-gray-600'}`} />
              </button>



              {/* Blocks for this phase */}
              {phase.blocks.map((_block, blockIndex) => (
                <React.Fragment key={blockIndex}>
                  <div className={`-mt-2.5 flex ${isSelected('block', phaseIndex, blockIndex) ? '' : ''}`}>
                    {/* Add button after block */}
                    <AddButton
                      onClick={() => onAdd('block', phaseIndex, blockIndex)}
                      type="block"
                    />
                  </div>
                  <button
                    onClick={() => onSelect({ type: 'block', phaseIndex, blockIndex })}
                    type="button"
                    className={`
                      relative p-2 rounded-md hover:bg-blue-400 group
                      ${isSelected('block', phaseIndex, blockIndex) ? 'bg-blue-400' : ''}
                    `}
                    title={`Block ${blockIndex + 1}`}
                  >
                    <FiBox className={`w-5 h-5 group-hover:text-white ${isSelected('block', phaseIndex, blockIndex) ? 'text-white' : 'text-gray-600'}`} />
                  </button>

                </React.Fragment>
              ))}

              {/* Add button for new block if no block is selected */}
              <div className={`-mt-2.5`}>
                {/* Add button after block */}
                <AddButton
                  onClick={() => onAdd('block', phaseIndex, phase.blocks.length)}
                  type="block"
                />
              </div>

              {/* Add button after phase */}
              <div className="absolute -mt-2.5 -right-5 z-10">
                <AddButton
                  onClick={() => onAdd('phase', phaseIndex + 1)}
                  type="phase"
                />
              </div>
            </div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

const AddButton: React.FC<{
  onClick: () => void;
  type: 'phase' | 'block';
}> = ({ onClick, type }) => (
  <div className="group relative">
    <button
      onClick={onClick}
      type="button"
      className={`p-1.5 w-1 bg-blue-600 transition-transform transform hover:scale-150 ${type === 'phase' ? 'rounded-full' : 'rounded'}`}
    >
      <FiPlus className="w-3 h-3 absolute left-0 top-0 text-white" />
    </button>
    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block">
      <div className="bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
        Add {type}
      </div>
    </div>
  </div>
);
