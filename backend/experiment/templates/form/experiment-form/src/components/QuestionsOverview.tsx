import React from 'react';
import Page from './Page';
import useFetch from '../hooks/useFetch';
import { createQuestionAPIUrl } from '../config';
import { Question } from '../types/types';
import { Link } from 'react-router-dom';

const url = createQuestionAPIUrl('questions');

const QuestionsOverview: React.FC = () => {
  const [questions, error, loading, fetchData] = useFetch<Question[]>(url);

  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  const loadingClass = loading ? 'opacity-50 pointer-events-none' : '';

  return (
    <Page title="Questions Overview">
      <div className={loadingClass}>
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
              {questions?.map((question) => (
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
      </div>
    </Page>
  );
};

export default QuestionsOverview;
