import React from 'react';
import { TranslatedContent } from '../types/types';
import { ISO_LANGUAGES } from "../constants";
import { Select } from './form/Select';
import { Input } from './form/Input';
import { MarkdownEditor } from './form/MarkdownEditor';
import { Button } from './Button';
import { FiTrash2, FiPlus } from 'react-icons/fi';

interface TranslatedContentFormsProps {
  contents: TranslatedContent[];
  onChange: (contents: TranslatedContent[]) => void;
}

const defaultContent: TranslatedContent = {
  index: 0,
  language: '',
  name: '',
  description: '',
  about_content: '',
  social_media_message: 'I scored {points} points in {experiment_name}!',
};

export const TranslatedContentForms: React.FC<TranslatedContentFormsProps> = ({ contents, onChange }) => {

  const handleAdd = () => {
    const newContent = {
      ...defaultContent,
      index: contents.length,
    };
    const updatedContents = [...contents, newContent].map((content, index) => ({ ...content, index }));

    onChange(updatedContents);
  };

  const handleRemove = (index: number) => {
    if (confirm('Are you sure you want to remove this translation?')) {
      onChange(contents.filter((_, i) => i !== index));
    }
  };

  const handleChange = (index: number, key: keyof TranslatedContent, value: string) => {
    const updated = [...contents];
    updated[index] = { ...updated[index], [key]: value };
    onChange(updated);
  };

  return (
    <div className="">
      <h3 className="text-lg font-medium mb-5">Translated Content</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">Language</th>
              <th className="text-left p-2">Name</th>
              <th className="text-left p-2">Description</th>
              <th className="text-left p-2">About Content</th>
              <th className="text-left p-2">Social Media Message</th>
              <th className="text-left p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {contents.map((content, index) => (
              <tr key={index} className="border-b">
                <td className="p-2">
                  <Select
                    value={content.language}
                    onChange={(e) => handleChange(index, 'language', e.target.value)}
                    className='min-w-32 block'
                  >
                    <option value="">Select language</option>
                    {Object.entries(ISO_LANGUAGES).map(([code, name]) => (
                      <option key={code} value={code}>
                        {name}
                      </option>
                    ))}
                  </Select>
                </td>
                <td className="p-2">
                  <Input
                    type="text"
                    value={content.name}
                    onChange={(e) => handleChange(index, 'name', e.target.value)}
                    required
                    className='min-w-32'
                  />
                </td>
                <td className="p-2">
                  <MarkdownEditor
                    value={content.description}
                    onChange={(value) => handleChange(index, 'description', value)}
                    rows={3}
                    field="Description"
                    className='min-w-64'
                  />
                </td>
                <td className="p-2">
                  <MarkdownEditor
                    value={content.about_content}
                    onChange={(value) => handleChange(index, 'about_content', value)}
                    rows={3}
                    field="About Content"
                    className='min-w-64'
                  />
                </td>
                <td className="p-2">
                  <Input
                    type="text"
                    value={content.social_media_message}
                    onChange={(e) => handleChange(index, 'social_media_message', e.target.value)}
                    className='min-w-64'
                  />
                </td>
                <td className="p-2">
                  <Button
                    variant="danger"
                    icon={<FiTrash2 />}
                    onClick={() => handleRemove(index)}
                  >
                    Remove
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Button
        variant="primary"
        onClick={handleAdd}
        className="mt-5 ml-2"
        icon={<FiPlus />}
      >
        Add new translation
      </Button>
    </div>
  );
};
