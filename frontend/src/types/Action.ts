import Social from "@/types/Social";
import Block, { FeedbackInfo } from "@/types/Block";
import IButton from  "@/types/Button";
import Participant from "@/types/Participant";
import { PlaybackAction } from "./Playback";
import Question from "./Question";
import { BreakRoundOn } from "./Trial";
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
  button: IButton;
  steps?: Array<ExplainerStep>;
  timer: number | null;
}

export interface InfoAction {
  view: "INFO";
  heading?: string;
  body: string | TrustedHTML;
  button: IButton;
}

export interface FeedbackForm {
  form: Question[];
  submitButton: IButton;
  skipButton: IButton;
}

export interface ITrial {
  playback: PlaybackAction;
  html: { body: string | TrustedHTML };
  feedbackForm: FeedbackForm;
  responseTime: number;
  autoAdvance: boolean;
  listenFirst: boolean;
  continueButton?: IButton;
  breakRoundOn?: BreakRoundOn;
}

export interface ScoreAction {
  view: "SCORE";
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

export interface FinalAction {
  score: number;
  percentile?: number;
  finalText: string | TrustedHTML;
  actionTexts: {
    allExperiments: string;
    profile: string;
    playAgain: string;
  };
  button: IButton;
  showParticipantLink: boolean;
  participantIdOnly: boolean;
  showProfileLink: boolean;
  social: Social;
  feedbackInfo?: FeedbackInfo;
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
