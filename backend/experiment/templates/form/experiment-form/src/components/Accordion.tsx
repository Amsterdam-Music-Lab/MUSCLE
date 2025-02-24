import React, { useState } from 'react';
import { FiChevronDown, FiChevronRight } from 'react-icons/fi';

interface AccordionItemProps {
  title: string;
  children: React.ReactNode;
  isOpen?: boolean;
  onToggle?: () => void;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({
  title,
  children,
  isOpen = false,
  onToggle,
}) => {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault(); // Prevent form submission
    onToggle?.();
  };

  return (
    <div className="border rounded-md mb-2">
      <button
        type="button" // Explicitly set type to button
        className="w-full px-4 py-2 text-left font-medium flex items-center justify-between bg-gray-50 hover:bg-gray-100"
        onClick={handleClick}
      >
        <span>{title}</span>
        {isOpen ? <FiChevronDown /> : <FiChevronRight />}
      </button>
      {isOpen && <div className="p-4 border-t">{children}</div>}
    </div>
  );
};

interface AccordionProps {
  items: {
    id: number | string;
    title: string;
    content: React.ReactNode;
  }[];
  singleOpen?: boolean;
}

export const Accordion: React.FC<AccordionProps> = ({ items, singleOpen = false }) => {
  const [openItems, setOpenItems] = useState<Set<number | string>>(new Set());

  const toggleItem = (id: number | string) => {
    setOpenItems((prev) => {
      const newOpenItems = new Set(prev);
      if (singleOpen) {
        newOpenItems.clear();
      }
      if (newOpenItems.has(id)) {
        newOpenItems.delete(id);
      } else {
        newOpenItems.add(id);
      }
      return newOpenItems;
    });
  };

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <AccordionItem
          key={item.id}
          title={item.title}
          isOpen={openItems.has(item.id)}
          onToggle={() => toggleItem(item.id)}
        >
          {item.content}
        </AccordionItem>
      ))}
    </div>
  );
};
