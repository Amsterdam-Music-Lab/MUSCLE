import { ExplainerProps } from "@/components/Explainer/Explainer";
import { FinalProps } from "@/components/Final/Final";
import { InfoProps } from "@/components/Info/Info";
import { LoadingProps } from "@/components/Loading/Loading";
import { PlaylistProps } from "@/components/Playlist/Playlist";
import { RedirectProps } from "@/components/Redirect/Redirect";
import { ScoreProps } from "@/components/Score/Score";
import { TrialProps } from "@/components/Trial/Trial";

interface SharedActionProps {
  title?: string;
  config?: object;
  style?: object;
}

export type Action = SharedActionProps &
  (
    | { view: "EXPLAINER" } & ExplainerProps
    | { view: "INFO" } & InfoProps
    | { view: "TRIAL_VIEW" } & TrialProps
    | { view: 'SCORE' } & ScoreProps
    | { view: 'FINAL' } & FinalProps
    | { view: 'PLAYLIST' } & PlaylistProps
    | { view: 'REDIRECT' } & RedirectProps
    | { view: "LOADING" } & LoadingProps
  )
