import React from 'react';
import { FiPlus, FiCircle, FiBox } from 'react-icons/fi';
import { Phase, Selection } from '../types/types';
import { useNavigate, useParams } from 'react-router-dom';

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
  const { id: experimentId } = useParams();
  const navigate = useNavigate();

  const handleSelect = (selection: Selection) => {
    const basePath = `/experiments/${experimentId}/phases`;
    if (selection.type === 'block') {
      navigate(`${basePath}/${selection.phaseIndex}/blocks/${selection.blockIndex}`);
    } else {
      navigate(`${basePath}/${selection.phaseIndex}`);
    }
    onSelect(selection);
  };

  const isSelected = (type: 'phase' | 'block', phaseIndex: number, blockIndex?: number) => {
    return selectedItem?.type === type &&
      selectedItem.phaseIndex === phaseIndex &&
      selectedItem.blockIndex === blockIndex;
  };

  return (
    <div className="w-full overflow-x-auto pt-4">
      <div className="flex flex-col items-start p-4 gap-3 min-w-max relative">
        {phases.map((phase, phaseIndex) => (
          <React.Fragment key={phaseIndex}>
            {/* Add button before phase */}
            {phaseIndex === 0 && (
              <div className={`absolute -top-2 -ml-0 z-10 hover:opacity-100 transition-opacity ${isSelected('phase', phaseIndex) ? 'opacity-100' : 'opacity-25'}`}>
                <AddButton
                  onClick={() => onAdd('phase', 0)}
                  type="phase"
                />
              </div>
            )}

            <div className={`relative flex items-center gap-1 p-2 pr-5 rounded-full ${phaseIndex === selectedItem?.phaseIndex ? 'bg-blue-100' : 'bg-gray-100'}`}>

              {/* Phase node */}
              <button
                onClick={() => handleSelect({ type: 'phase', phaseIndex })}
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
                  <div className={`-mt-2.5 flex ${isSelected('block', phaseIndex, blockIndex) || isSelected('block', phaseIndex, blockIndex - 1) ? 'opacity-100' : 'opacity-25'} transition-opacity hover:opacity-100`}>
                    {/* Add button before block */}
                    <AddButton
                      onClick={() => onAdd('block', phaseIndex, blockIndex)}
                      type="block"
                    />
                  </div>
                  <button
                    onClick={() => handleSelect({
                      type: 'block',
                      phaseIndex,
                      blockIndex
                    })}
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

              {/* Add button for new block if no or the last block is selected */}
              <div className={`-mt-2.5 
              
              ${!isSelected('block', phaseIndex) && !isSelected('block', phaseIndex, phase.blocks.length - 1)

                  ? 'opacity-25' : 'opacity-100'} transition-opacity hover:opacity-100`}>
                {/* Add button after block */}
                <AddButton
                  onClick={() => onAdd('block', phaseIndex, phase.blocks.length)}
                  type="block"
                />
              </div>

              {/* vertical line between the phases equal to the gap size of gap-2  */}
              {phaseIndex < phases.length - 1 && (
                <div className={`absolute -bottom-4 left-6 w-0.5 h-4 ${isSelected('phase', phaseIndex) || isSelected('phase', phaseIndex + 1) ? 'bg-blue-400' : 'bg-gray-200'}`} />
              )}

              {/* Add button after phase */}
              <div className={`absolute -bottom-3 left-0 z-10 hover:opacity-100 transition-opacity 
              ${isSelected('phase', phaseIndex) || isSelected('phase', phaseIndex + 1) ? 'opacity-100' : 'opacity-25'} `}>
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
