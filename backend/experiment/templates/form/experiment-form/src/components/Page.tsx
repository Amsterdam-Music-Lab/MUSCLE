import { ReactNode } from 'react';
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
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 inline-block mb-4"
          >
            &lt; {backText}
          </Link>
        )}
        <h1 className="text-2xl font-bold">{title}</h1>
      </div>
      {children}
    </div>
  );
};

export default Page;
