import React from 'react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  const pages = [];
  for (let i = 1; i <= totalPages; i++) {
    pages.push(
      <Button
        key={i}
        onClick={() => onPageChange(i)}
        className={`px-3 py-1 border ${i === currentPage ? 'bg-blue-500 text-white' : '!bg-white !text-blue-500'}`}
      >
        {i}
      </Button>
    );
  }

  return (
    <div className="flex justify-center items-center gap-2 mt-4">
      <Button
        onClick={() => onPageChange(currentPage - 1)}
        className="px-3 py-1 border"
        disabled={currentPage === 1}
      >
        &lt;
      </Button>
      {pages}
      <Button
        onClick={() => onPageChange(currentPage + 1)}
        className="px-3 py-1 border"
        disabled={currentPage === totalPages}
      >
        &gt;
      </Button>
    </div>
  );
};

export default Pagination;
