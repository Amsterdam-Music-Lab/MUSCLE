import { IFeedbackForm } from "@/components/Trial/Trial";
import { PlaybackArgs } from "./Playback";
import { TrialConfig } from "./Trial";

export interface Action {
  view: string;

  // Optional properties depending on the view
  instruction?: string;
  button_label?: string;
  steps?: Array<{
    number: number;
    description: string;
  }>;
  timer?: number | null;
  title?: string;
  config?: TrialConfig;
  style?: {
    root: string;
  };
  playback?: PlaybackArgs;
  html?: { body: string | TrustedHTML };
  feedback_form?: IFeedbackForm;
}

export type Round = Action[];

export interface RoundResponse {
  next_round: Round;
}
