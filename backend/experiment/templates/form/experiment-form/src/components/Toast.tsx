import { Toast as ToastType } from '../utils/store';

interface ToastProps {
  toast: ToastType;
}

export const Toast: React.FC<ToastProps> = ({ toast }) => {
  const bgColorClass = {
    info: 'bg-gray-800',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    error: 'bg-red-600'
  }[toast.level];

  return (
    <div className={`${bgColorClass} text-white px-6 py-3 rounded-lg shadow-lg transition-all duration-300 ease-in-out`}>
      <p>{toast.message}</p>
    </div>
  );
};
