import React from 'react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange, className = '' }) => {
  if (totalPages <= 1) return null;

  const pages = [];
  for (let i = 1; i <= totalPages; i++) {
    pages.push(
      <Button
        key={i}
        onClick={() => onPageChange(i)}
        className="px-3 py-1 border"
        variant={i === currentPage ? 'primary' : 'primaryInverted'}
      >
        {i}
      </Button>
    );
  }

  return (
    <div className={`flex justify-center items-center gap-2 ${className}`}>
      <Button
        onClick={() => onPageChange(currentPage - 1)}
        className="px-3 py-1 border"
        disabled={currentPage === 1}
        variant="primaryInverted"
      >
        &lt;
      </Button>
      {pages}
      <Button
        onClick={() => onPageChange(currentPage + 1)}
        className="px-3 py-1 border"
        disabled={currentPage === totalPages}
        variant="primaryInverted"
      >
        &gt;
      </Button>
    </div>
  );
};

export default Pagination;
