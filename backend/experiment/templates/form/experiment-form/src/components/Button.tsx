import React, { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface ButtonProps {
  children: ReactNode;
  onClick?: (e?: React.MouseEvent) => void;
  type?: 'button' | 'submit' | 'reset';
  variant?:
  | 'primary' | 'secondary' | 'danger' | 'success' | 'warning'
  | 'primaryInverted' | 'secondaryInverted' | 'dangerInverted' | 'successInverted' | 'warningInverted'
  | 'primaryText' | 'secondaryText' | 'dangerText' | 'successText' | 'warningText';
  size?: 'sm' | 'md' | 'lg';
  icon?: ReactNode;
  to?: string;
  disabled?: boolean;
  className?: string;
}

const variantStyles = {
  primary: 'bg-indigo-600 hover:bg-indigo-700 text-white',
  secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-800',
  danger: 'bg-red-500 hover:bg-red-600 text-white',
  success: 'bg-emerald-500 hover:bg-emerald-600 text-white',
  warning: 'bg-amber-500 hover:bg-amber-600 text-white',
  // inverted variants
  primaryInverted: 'bg-white border border-indigo-600 text-indigo-600 hover:bg-indigo-600 hover:text-white',
  secondaryInverted: 'bg-white border border-gray-300 text-gray-800 hover:bg-gray-300 hover:text-gray-900',
  dangerInverted: 'bg-white border border-red-500 text-red-500 hover:bg-red-500 hover:text-white',
  successInverted: 'bg-white border border-emerald-500 text-emerald-500 hover:bg-emerald-500 hover:text-white',
  warningInverted: 'bg-white border border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-white',
  // text-only variants
  primaryText: 'text-indigo-600 hover:underline',
  secondaryText: 'text-gray-800 hover:underline',
  dangerText: 'text-red-500 hover:underline',
  successText: 'text-emerald-500 hover:underline',
  warningText: 'text-amber-500 hover:underline',
};

const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2',
  lg: 'px-6 py-3 text-lg',
};

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  size = 'md',
  icon,
  to,
  disabled = false,
  className = '',
}) => {
  const baseStyle = 'inline-flex items-center justify-center rounded-md font-medium transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed';
  const styles = `${baseStyle} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`;

  if (onClick) {
    return (
      <button
        type={type}
        onClick={onClick}
        disabled={disabled}
        className={styles}
      >
        {icon && <span className="mr-2">{icon}</span>}
        {children}
      </button>
    );
  } else if (to) {
    return (
      <Link to={to} className={styles}>
        {icon && <span className="mr-2">{icon}</span>}
        {children}
      </Link>
    );
  }

  return (
    <button
      type={type}
      disabled={disabled}
      className={styles}
    >
      {icon && <span className="mr-2">{icon}</span>}
      {children}
    </button>
  );
};
