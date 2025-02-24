import React from 'react';
import { FormField } from './form/FormField';
import { Input } from './form/Input';
import { Select } from './form/Select';
import { Block, BlockTranslatedContent } from '../types/types';
import { useBlockRules } from '../hooks/useBlockRules';
import { FiTrash2 } from 'react-icons/fi';
import { Button } from './Button';
import { BlockTranslatedContentForms } from './BlockTranslatedContentForms';
import { useBlockPlaylists } from '../hooks/useBlockPlaylists';
import { QuestionSeriesForms } from './QuestionSeriesForms';

interface BlockFormProps {
  block: Block;
  onChange: (block: Block) => void;
  onDelete: () => void;
}

export const BlockForm: React.FC<BlockFormProps> = ({ block, onChange, onDelete }) => {
  const { rules, loading, error } = useBlockRules();
  const { playlists, loading: playlistsLoading, error: playlistsError } = useBlockPlaylists();

  const handleChange = (field: keyof Block, value: string | number | BlockTranslatedContent[]) => {
    onChange({ ...block, [field]: value });
  };

  return (
    <div className="space-y-5">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-medium">Block Settings</h3>
        <Button
          variant="danger"
          size="sm"
          icon={<FiTrash2 />}
          onClick={onDelete}
        >
          Delete Block
        </Button>
      </div>
      <div className="grid sm:grid-cols-2 gap-5">
        <FormField label="Slug">
          <Input
            type="text"
            value={block.slug}
            onChange={(e) => handleChange('slug', e.target.value)}
            required
          />
        </FormField>

        <FormField label="Index">
          <Input
            type="number"
            value={block.index}
            onChange={(e) => handleChange('index', parseInt(e.target.value))}
            required
          />
        </FormField>
      </div>

      <div className="grid sm:grid-cols-2 gap-5">
        <FormField label="Rounds">
          <Input
            type="number"
            value={block.rounds}
            onChange={(e) => handleChange('rounds', parseInt(e.target.value))}
            required
          />
        </FormField>

        <FormField label="Bonus Points">
          <Input
            type="number"
            value={block.bonus_points}
            onChange={(e) => handleChange('bonus_points', parseInt(e.target.value))}
          />
        </FormField>
      </div>

      <div className="grid sm:grid-cols-2 gap-5">
        <FormField label="Rules">
          <Select
            value={block.rules}
            onChange={(e) => handleChange('rules', e.target.value)}
            required
            disabled={loading}
          >
            <option value="">Select rules</option>
            {rules.map((rule) => (
              <option key={rule.id} value={rule.id}>
                {rule.name}
              </option>
            ))}
          </Select>
          {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
          {loading && <p className="text-gray-500 text-sm mt-1">Loading rules...</p>}
        </FormField>

        <FormField label="Playlists">
          <Select
            value={block.playlists.map((playlist) => playlist.id)}
            onChange={(e) => {
              const selectedPlaylists = Array.from(e.target.selectedOptions, (option) => ({
                id: parseInt(option.value),
                name: option.text,
              }));
              handleChange('playlists', selectedPlaylists);
            }}
            multiple
            required
            disabled={playlistsLoading}
          >
            {playlists.map((playlist) => (
              <option key={playlist.id} value={parseInt(playlist.id)}>
                {playlist.name}
              </option>
            ))}
          </Select>
          {playlistsError && <p className="text-red-500 text-sm mt-1">{playlistsError}</p>}
          {playlistsLoading && <p className="text-gray-500 text-sm mt-1">Loading playlists...</p>}
        </FormField>
      </div>

      <BlockTranslatedContentForms
        contents={block.translated_contents || []}
        onChange={(contents) => handleChange('translated_contents', contents)}
      />

      <QuestionSeriesForms
        series={block.questionseries_set || []}
        onChange={(series) => handleChange('questionseries_set', series)}
      />
    </div>
  );
};
