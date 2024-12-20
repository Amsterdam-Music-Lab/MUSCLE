import React from 'react';

interface TabAction {
  icon: React.ReactNode;
  title: string;
  onClick: (tabId: string | number) => void;
}

interface Tab {
  id: string | number;
  label: string;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string | number;
  onTabChange: (tabId: string | number) => void;
  actions?: TabAction[];
}

export const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, onTabChange, actions = [] }) => {
  return (
    <div className="border-b border-gray-200">
      <nav className="-mb-px flex space-x-8" aria-label="Tabs">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className="flex items-center group"
          >
            <button
              type="button"
              onClick={() => onTabChange(tab.id)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
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
