import { ReactNode } from 'react';
import { FiArrowLeft } from 'react-icons/fi';
import { Link } from 'react-router-dom';

interface PageProps {
  title: string;
  children: ReactNode;
  backTo?: string;
  backText?: string;
}

const Page = ({ title, children, backTo, backText = 'Back' }: PageProps) => {
  return (
    <div className="p-3">
      <div className="mb-5">
        {backTo && (
          <Link
            to={backTo}
            className="inline-flex items-center justify-center rounded-md font-medium transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 mb-4"
          >
            <FiArrowLeft className="inline mr-1" />
            {backText}
          </Link>
        )}
        <h1 className="text-2xl font-bold font-rajdhani">{title}</h1>
      </div>
      {children}
    </div>
  );
};

export default Page;
