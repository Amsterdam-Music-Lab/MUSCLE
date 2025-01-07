import { ISO_LANGUAGES } from "../constants";
import { TranslatedContent } from "../types/types";
import { FormField } from "./form/FormField";
import { Input } from "./form/Input";
import { Select } from "./form/Select";
import { Textarea } from "./form/Textarea";
import { MarkdownEditor } from "./form/MarkdownEditor";

interface TranslatedContentProps {
  content: TranslatedContent;
  onChange: (content: TranslatedContent) => void;
}

export function TranslatedContentForm({ content, onChange }: TranslatedContentProps) {

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
            />
          </FormField>
        </div>

        <FormField label="Description">
          <Textarea
            value={content.description}
            onChange={(e) => onChange({ ...content, description: e.target.value })}
            rows={3}
          />
        </FormField>

        <FormField label="About Content">
          <MarkdownEditor
            value={content.about_content}
            onChange={(value) => onChange({ ...content, about_content: value })}
            rows={8}
          />
        </FormField>

        <FormField label="Social Media Message">
          <Input
            type="text"
            value={content.social_media_message}
            onChange={(e) => onChange({ ...content, social_media_message: e.target.value })}
          />
        </FormField>
      </div>
    </div>
  );
}
