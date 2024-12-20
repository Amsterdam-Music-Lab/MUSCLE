import React from 'react';

interface FormFieldProps {
  label: string;
  error?: string;
  className?: string;
  children: React.ReactNode;
}

export const FormField: React.FC<FormFieldProps> = ({
  label,
  error,
  className = '',
  children
}) => {
  return (
    <div className={`mb-5 ${className}`}>
      <label className="block">
        <span className="block text-sm font-semibold text-gray-700 mb-2">{label}</span>
        {children}
      </label>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};
