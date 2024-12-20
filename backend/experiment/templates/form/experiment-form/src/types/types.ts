export interface TranslatedContent {
  id?: number;
  index: number;
  language: string;
  name: string;
  description: string;
  about_content: string;
  social_media_message: string;
}

export interface Phase {
  id?: number;
  index: number;
  dashboard: boolean;
  randomize: boolean;
}

export interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
  translated_content: TranslatedContent[];
  phases: Phase[];
}
