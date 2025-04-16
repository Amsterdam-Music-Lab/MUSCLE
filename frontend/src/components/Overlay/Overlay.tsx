import React, { useEffect } from 'react';
import './Overlay.scss';
import { Button } from "@/components/ui";

interface OverlayProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  content: React.ReactNode;
}

const Overlay: React.FC<OverlayProps> = ({
  isOpen,
  onClose,
  title = 'Tutorial',
  content
}) => {

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    } else {
      document.removeEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  return (
    <div
      className={`overlay ${isOpen ? 'visible' : ''}`}
      aria-hidden={!isOpen}
      role="presentation"
      onClick={handleOverlayClick}
    >
      <div
        className="content"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          className="closeIcon"
          onClick={onClose}
          aria-label="Close tutorial"
        >
          ×
        </button>

        <div className="header">
          <h2>{title}</h2>
        </div>

        <div className="body">
          {content}
        </div>

        <div className="footer">
          <Button onClick={() => onClose()} className='primary' title="Continue" clickOnce={false} />
        </div>
      </div>
    </div>
  );
};

export default Overlay;
