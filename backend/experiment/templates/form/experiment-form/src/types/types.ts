export interface TranslatedContent {
  id?: number;
  index: number;
  language: string;
  name: string;
  description: string;
  about_content: string;
  social_media_message: string;
}

export interface BlockTranslatedContent {
  index: number;
  language: string;
  name: string;
  description: string;
}

export interface BlockPlaylist {
  id: string;
  name: string;
}

export interface Question {
  key: string;
  question: string;
  type: string;
}

export interface QuestionGroup {
  key: string;
  questions: string[];
}

export interface QuestionInSeries {
  key: string;
  index: number;
}

export interface BlockQuestionSeries {
  id?: number;
  name: string;
  index: number;
  randomize: boolean;
  questions: QuestionInSeries[];
}

export interface Block {
  id?: number;
  index: number;
  slug: string;
  rounds: number;
  bonus_points: number;
  rules: string;
  phase?: number;  // Make phase optional
  translated_contents: BlockTranslatedContent[];
  playlists: BlockPlaylist[];
  questionseries_set: BlockQuestionSeries[];
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

export enum QuestionTypeEnum {
  BooleanQuestion = "BooleanQuestion",
  ChoiceQuestion = "ChoiceQuestion",
  NumberQuestion = "NumberQuestion",
  TextQuestion = "TextQuestion",
  LikertQuestion = "LikertQuestion",
  LikertQuestionIcon = "LikertQuestionIcon",
  AutoCompleteQuestion = "AutoCompleteQuestion"
}

export type QuestionType = keyof typeof QuestionTypeEnum;

export interface QuestionChoice {
  key: string;
  text: string;
  index: number;
}
export interface QuestionData {
  key: string;
  question: string;
  type: QuestionType;
  choices?: QuestionChoice[];
  explainer?: string;
  scale_steps?: number;
  profile_scoring_rule?: string;
  min_value?: number;
  max_value?: number;
  max_length?: number;
  min_values?: number;
  is_skippable?: boolean;
  view?: string;
}
