import { ISO_LANGUAGES } from "../constants";
import { BlockTranslatedContent } from "../types/types";
import { FormField } from "./form/FormField";
import { Input } from "./form/Input";
import { Select } from "./form/Select";
import { MarkdownEditor } from "./form/MarkdownEditor";

interface BlockTranslatedContentFormProps {
  content: BlockTranslatedContent;
  onChange: (content: BlockTranslatedContent) => void;
}

export function BlockTranslatedContentForm({ content, onChange }: BlockTranslatedContentFormProps) {
  return (
    <div className='p-5 bg-gray-50'>
      <div className="p-5 bg-white border rounded-md space-y-5">
        <div className="grid sm:grid-cols-2 gap-5">
          <FormField label="Language">
            <Select
              value={content.language}
              onChange={(e) => onChange({ ...content, language: e.target.value })}
            >
              <option value="">Select language</option>
              {Object.entries(ISO_LANGUAGES).map(([code, name]) => (
                <option key={code} value={code}>
                  {name}
                </option>
              ))}
            </Select>
          </FormField>

          <FormField label="Name">
            <Input
              type="text"
              value={content.name}
              onChange={(e) => onChange({ ...content, name: e.target.value })}
              required
            />
          </FormField>
        </div>

        <FormField label="Description">
          <MarkdownEditor
            value={content.description}
            onChange={(value) => onChange({ ...content, description: value })}
            rows={3}
            field="Description"
          />
        </FormField>
      </div >
    </div >
  );
}
