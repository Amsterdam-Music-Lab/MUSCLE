import Social from "@/types/Social";
import Block, { FeedbackInfo } from "@/types/Block";
import IButton from  "@/types/Button";
import Participant from "@/types/Participant";
import { PlaybackArgs } from "./Playback";
import Question from "./Question";
import { TrialConfig } from "./Trial";
import { MutableRefObject } from "react";

interface SharedActionProps {
  title?: string;
  config?: object;
  style?: object;
}

interface ExplainerStep {
  number: number;
  description: string;
}

export interface Explainer {
  instruction: string;
  button: IButton;
  steps?: Array<ExplainerStep>;
  timer: number | null;
}

export interface Info {
  heading?: string;
  body: string | TrustedHTML;
  button: IButton;
}

export interface IFeedbackForm {
  form: Question[];
  submitButton: IButton;
  skipButton: IButton;
  is_skippable: boolean;
}

export interface Trial {
  playback: PlaybackArgs;
  html: { body: string | TrustedHTML };
  feedback_form: IFeedbackForm;
  config: TrialConfig;
}

export interface Score {
  last_song?: string;
  score: number;
  score_message: string;
  total_score?: number;
  texts: {
    score: string;
    listen_explainer: string;
  };
  button: IButton;
  icon?: string;
  feedback?: string;
  timer?: number;
}

export interface Final {
  block: Block;
  participant: Participant;
  score: number;
  percentile?: number;
  final_text: string | TrustedHTML;
  action_texts: {
    all_experiments: string;
    profile: string;
    play_again: string;
  };
  button: IButton;
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

export interface Playlist {
  instruction: string;
  playlist: MutableRefObject<string>;
}

export interface Redirect {
  url: string;
}

export interface Loading {
  duration?: number;
  loadingText?: string;
}

export type Action = SharedActionProps &
  (
    | { view: "EXPLAINER" } & Explainer
    | { view: "INFO" } & Info
    | { view: "TRIAL_VIEW" } & Trial
    | { view: 'SCORE' } & Score
    | { view: 'FINAL' } & Final
    | { view: 'PLAYLIST' } & Playlist
    | { view: 'REDIRECT' } & Redirect
    | { view: "LOADING" } & Loading
  )

export default Action;
