import Social from "@/types/Social";
import Block, { FeedbackInfo } from "@/types/Block";
import Participant from "@/types/Participant";
import { PlaybackArgs } from "./Playback";
import Question from "./Question";
import { TrialConfig } from "./Trial";
import { MutableRefObject } from "react";

export interface SharedActionProps {
  block: Block;
  participant: Participant;
  title?: string;
  config?: object;
  style?: object;
  onNext: (doBreak?: boolean) => void;
  onResult?: () => void;
}

interface ExplainerStep {
  number: number;
  description: string;
}

export interface ExplainerAction {
  view: "EXPLAINER";
  instruction: string;
  button_label: string;
  steps?: Array<ExplainerStep>;
  timer: number | null;
}

export interface InfoAction {
  view: "INFO";
  heading?: string;
  body: string | TrustedHTML;
  button_label?: string;
  button_link?: string;
}

export interface FeedbackForm {
  form: Question[];
  submit_label: string;
  skip_label: string;
  is_skippable: boolean;
}

export interface TrialAction {
  view: "TRIAL";
  playback: PlaybackArgs;
  html: { body: string | TrustedHTML };
  feedback_form: FeedbackForm;
  config: TrialConfig;
}

export interface ScoreAction {
  view: "SCORE";
  last_song?: string;
  score: number;
  score_message: string;
  total_score?: number;
  texts: {
    score: string;
    next: string;
    listen_explainer: string;
  };
  icon?: string;
  feedback?: string;
  timer?: number;
}

export interface FinalAction {
  score: number;
  percentile?: number;
  final_text: string | TrustedHTML;
  action_texts: {
    all_experiments: string;
    profile: string;
    play_again: string;
  };
  button: {
    text: string;
    link: string;
  };
  show_participant_link: boolean;
  participant_id_only: boolean;
  show_profile_link: boolean;
  social: Social;
  feedback_info?: FeedbackInfo;
  points: string;
  rank: {
    class: string;
    text: string;
  };
  logo: {
    image: string;
    link: string;
  };
}

export interface PlaylistAction {
  view: "PLAYLIST";
  instruction: string;
  playlist: MutableRefObject<string>;
}

export interface RedirectAction {
  view: "REDIRECT";
  url: string;
}

export interface LoadingAction {
  view: "LOADING";
  duration?: number;
  loadingText?: string;
}

export type Action = ( 
  ExplainerAction
    | InfoAction
    | TrialAction
    | ScoreAction
    | FinalAction
    | PlaylistAction
    | RedirectAction
    | LoadingAction
  )

export default Action;
