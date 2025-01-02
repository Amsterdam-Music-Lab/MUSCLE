import React from 'react';

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({ className = '', label, ...props }) => {
  return (
    <label className="inline-flex items-center">
      <input
        type="checkbox"
        {...props}
        className={`
          w-4 h-4 text-blue-600 rounded
          border-gray-300 shadow-sm
          focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:ring-opacity-50
          disabled:bg-gray-100 disabled:cursor-not-allowed
          ${className}
        `}
      />
      {label && <span className="ml-2 text-gray-700">{label}</span>}
    </label>
  );
};
