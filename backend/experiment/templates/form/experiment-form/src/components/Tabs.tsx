import React, { useState } from 'react';

interface TabAction {
  icon: React.ReactNode;
  title: string;
  onClick: (tabId: string | number) => void;
}

interface Tab {
  id: string | number;
  label: string;
  icon?: React.ReactNode;  // Add icon support
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string | number;
  onTabChange: (tabId: string | number) => void;
  actions?: TabAction[];
  onReorder?: (startIndex: number, endIndex: number) => void;
  draggable?: boolean;
  wrap?: boolean;
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  activeTab,
  onTabChange,
  actions = [],
  onReorder,
  draggable = false,
  wrap = false,
}) => {
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null);

  const handleDragStart = (e: React.DragEvent, index: number) => {
    if (tabs[index].id === 'new') return;
    setDraggedIndex(index);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    if (tabs[index].id === 'new') return;
    setDragOverIndex(index);
  };

  const handleDragEnd = () => {
    if (draggedIndex !== null && dragOverIndex !== null && onReorder) {
      onReorder(draggedIndex, dragOverIndex);
    }
    setDraggedIndex(null);
    setDragOverIndex(null);
  };

  return (
    <div className="border-b border-gray-200">
      <nav className={`-mb-px flex ${wrap ? 'flex-wrap' : 'overflow-x-auto'}
      `} aria-label="Tabs">
        {tabs.map((tab, index) => (
          <div
            key={tab.id}
            draggable={draggable && tab.id !== 'new'}
            onDragStart={(e) => handleDragStart(e, index)}
            onDragOver={(e) => handleDragOver(e, index)}
            onDragEnd={handleDragEnd}
            className={`
              flex items-center group flex-shrink-0
              ${draggedIndex === index ? 'opacity-50' : ''}
              ${dragOverIndex === index ? 'border-2 border-blue-500 bg-blue-50' : ''}
            `}
          >
            <button
              type="button"
              onClick={() => onTabChange(tab.id)}
              className={`
                whitespace-nowrap py-4 px-3 border-b-2 font-medium text-sm flex items-center gap-2
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
                ${draggable && tab.id !== 'new' ? 'cursor-move' : ''}
              `}
            >
              {tab.icon && <span className="w-4 h-4">{tab.icon}</span>}
              {tab.label}
            </button>
            {actions.length > 0 && activeTab === tab.id && (
              <div className="flex gap-2 ml-2">
                {actions.map((action, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => action.onClick(tab.id)}
                    title={action.title}
                    className="p-1 text-gray-400 hover:text-gray-600 focus:outline-none"
                  >
                    {action.icon}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>
    </div>
  );
};
