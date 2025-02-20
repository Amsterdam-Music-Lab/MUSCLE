import React, { useState, useEffect } from 'react';
import Page from './Page';
import useFetch from '../hooks/useFetch';
import { createQuestionAPIUrl } from '../config';
import { Question } from '../types/types';
import { Link } from 'react-router-dom';

const url = createQuestionAPIUrl('questions');
const itemsPerPage = 25;

const QuestionsOverview: React.FC = () => {
  const [questions, error, loading, fetchData] = useFetch<Question[]>(url);
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState(searchTerm);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
      setCurrentPage(1);
    }, 300);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  const filteredQuestions = questions?.filter(q =>
    q.key.toLowerCase().includes(debouncedSearchTerm.toLowerCase()) ||
    q.question.toLowerCase().includes(debouncedSearchTerm.toLowerCase()) ||
    q.type.toLowerCase().includes(debouncedSearchTerm.toLowerCase())
  ) || [];

  const totalPages = Math.ceil(filteredQuestions.length / itemsPerPage);
  const displayQuestions = filteredQuestions.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const changePage = (page: number) => {
    if (page < 1 || page > totalPages) return;
    setCurrentPage(page);
  };

  const renderPagination = () => {
    if (totalPages <= 1) return null;
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => changePage(i)}
          className={`px-3 py-1 border ${i === currentPage ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
        >
          {i}
        </button>
      );
    }
    return (
      <div className="flex justify-center items-center gap-2 mt-4">
        <button onClick={() => changePage(currentPage - 1)} className="px-3 py-1 border" disabled={currentPage === 1}>
          &lt;
        </button>
        {pages}
        <button onClick={() => changePage(currentPage + 1)} className="px-3 py-1 border" disabled={currentPage === totalPages}>
          &gt;
        </button>
      </div>
    );
  };

  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  const loadingClass = loading ? 'opacity-50 pointer-events-none' : '';

  return (
    <Page title="Questions Overview">
      <div className={loadingClass}>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search questions..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        {renderPagination()}
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white shadow-md rounded">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Key</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Question</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Type</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {displayQuestions.map((question) => (
                <tr key={question.key} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link to={`/questions/${question.key}`} className="text-blue-500 hover:underline">
                      {question.key}
                    </Link>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{question.question}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{question.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {renderPagination()}
      </div>
    </Page>
  );
};

export default QuestionsOverview;
