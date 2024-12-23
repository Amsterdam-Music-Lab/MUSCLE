export interface TranslatedContent {
  id?: number;
  index: number;
  language: string;
  name: string;
  description: string;
  about_content: string;
  social_media_message: string;
}

export interface Block {
  id?: number;
  index: number;
  slug: string;
  rounds: number;
  bonus_points: number;
  rules: string;
  phase?: number;  // Make phase optional
}

export interface Phase {
  id?: number;
  index: number;
  dashboard: boolean;
  randomize: boolean;
  blocks: Block[];
}

export interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
  translated_content: TranslatedContent[];
  phases: Phase[];
}

export type Selection = {
  type: 'phase' | 'block';
  phaseIndex: number;
  blockIndex?: number;
};
