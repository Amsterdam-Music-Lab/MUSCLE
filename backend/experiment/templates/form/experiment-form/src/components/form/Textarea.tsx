import React from 'react';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  fullWidth?: boolean;
}

export const Textarea: React.FC<TextareaProps> = ({ className = '', fullWidth = true, ...props }) => {
  return (
    <textarea
      {...props}
      className={`
        px-4 py-3 rounded-md border border-gray-300 shadow-sm
        focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:ring-opacity-50
        disabled:bg-gray-100 disabled:cursor-not-allowed
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `}
    />
  );
};
