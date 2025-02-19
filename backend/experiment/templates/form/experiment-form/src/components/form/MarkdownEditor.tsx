import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownEditorProps {
  value: string;
  onChange: (value: string) => void;
  rows?: number;
  field?: string;
  className?: string;
}

export function MarkdownEditor({ field, value, onChange, rows = 10, className = '' }: MarkdownEditorProps) {
  const [isPreview, setIsPreview] = useState(false);

  const placeholder = `# ${field ? field : 'Markdown input'}\n\n**Write your _markdown_ content here...**`;

  return (
    <div className={`relative group ${className}`}>
      <div className="absolute right-2 top-2 flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10">
        <button
          type="button"
          onClick={() => setIsPreview(false)}
          className={`px-3 py-1 text-sm rounded shadow hover:shadow-md transition-shadow ${!isPreview ? 'bg-blue-500 text-white' : 'bg-white hover:bg-gray-50'
            }`}
        >
          Edit
        </button>
        <button
          type="button"
          onClick={() => setIsPreview(true)}
          className={`px-3 py-1 text-sm rounded shadow hover:shadow-md transition-shadow ${isPreview ? 'bg-blue-500 text-white' : 'bg-white hover:bg-gray-50'
            }`}
        >
          Preview
        </button>
      </div>

      {isPreview ? (
        <div className="prose max-w-none p-4 border rounded-md bg-white min-h-[200px]">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{value}</ReactMarkdown>
        </div>
      ) : (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          rows={rows}
          className="w-full p-2 border rounded-md"
          placeholder={placeholder}
        />
      )}
    </div>
  );
}
