import { useBoundStore } from '../utils/store';
import { Toast } from './Toast';

export const Toasts: React.FC = () => {
  const toasts = useBoundStore((state) => state.toasts);

  return (
    <div className="fixed bottom-4 right-4 flex flex-col gap-2">
      {toasts.map((toast, index) => (
        <Toast key={index} toast={toast} />
      ))}
    </div>
  );
};
