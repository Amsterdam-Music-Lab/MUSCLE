import React, { useState, useEffect } from 'react';
import Page from './Page';
import useFetch from '../hooks/useFetch';
import { createQuestionAPIUrl } from '../config';
import { Question } from '../types/types';
import { Link } from 'react-router-dom';
import Pagination from './Pagination';
import { Input } from './form/Input';
import { FormField } from './form/FormField';
import { FiPlusCircle } from 'react-icons/fi';

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
    }, 50);
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

  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  const loadingClass = loading ? 'opacity-50 pointer-events-none' : '';

  return (
    <Page title="Questions Overview">
      <div className={loadingClass}>
        <div className='flex justify-between items-end flex-wrap gap-4 mb-4'>
          <div>
            <Input
              type="text"
              placeholder="Search questions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="p-2 border rounded"
            />
          </div>
          <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={changePage} />
          <Link to="/questions/new" className="bg-emerald-500 text-white px-4 py-2 rounded">
            <FiPlusCircle className="inline mr-1" />
            New Question
          </Link>
        </div>
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
                    <Link to={`/questions/${question.key}/edit`} className="text-blue-500 hover:underline">
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
        <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={changePage} className="mt-4" />
      </div>
    </Page>
  );
};

export default QuestionsOverview;
