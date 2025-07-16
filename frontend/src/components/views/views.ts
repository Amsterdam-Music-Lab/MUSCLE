import type {
  ViewDependency,
  GetViewPropsArgs,
} from "@/components/application/View/View";

// Non lazily-loaded
import { lazy } from "react";
import { ErrorView, LoadingView } from "@/components/views";
import convertTutorial from "@/util/convertTutorial";
import frontendConfig from "@/config/frontend";

type ViewMeta = {
  dependencies?: ViewDependency[];
  usesOwnLayout?: boolean;
  getViewProps?: (props: GetViewPropsArgs | any) => P;
};

export const views: Record<string, { component: any; meta: ViewMeta }> = {};

views.about = {
  component: lazy(() => import("@/components/views/AboutView/AboutView")),
  meta: {
    usesOwnLayout: true,
    getViewProps: ({ experiment }) => ({
      experiment,
      content: experiment.aboutContent,
      slug: experiment.slug,
      backButtonText: experiment.backButtonText,

      // Passed on to ExperimentLayout
      disclaimerHtml: experiment?.disclaimer,
      privacyHtml: experiment?.privacy,
      logos: experiment?.theme?.footer?.logos,
      showFooter: experiment?.theme?.footer,
    }),
  },
};

views.consent = {
  component: lazy(() => import("@/components/views/ConsentView/ConsentView")),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ participant, onNext, experiment }) => ({
      experimentSlug: experiment.slug,
      consentHtml: experiment.consent.text,
      participant,
      onConfirm: onNext,
      title: experiment.consent.title,
      confirmLabel: experiment.consent.confirm,
      denyLabel: experiment.consent.deny,
    }),
    dependencies: ["participant"],
  },
};

views.consentDenied = {
  component: () =>
    import("@/components/views/ConsentDeniedView/ConsentDeniedView"),
  meta: { usesOwnLayout: false },
};

views.dashboard = {
  component: () => import("@/components/views/DashboardView/DashboardView"),
  meta: {
    usesOwnLayout: true,
    getViewProps: ({ experiment, participant }) => ({
      name: experiment.name,
      slug: experiment.slug,
      description: experiment.description,
      totalScore: experiment.totalScore,
      nextBlock: experiment.nextBlock,
      header: experiment?.theme?.header ?? {},
      socialMediaConfig: experiment.socialMediaConfig,
      participantId: participant?.participant_id_url,
      dashboard: experiment.dashboard,

      // Passed on to ExperimentLayout
      disclaimerHtml: experiment?.disclaimer,
      privacyHtml: experiment?.privacy,
      logos: experiment?.theme?.footer?.logos,
      showFooter: experiment?.theme?.footer,
    }),
    dependencies: ["participant"],
  },
};

views.error = {
  component: ErrorView,
  meta: { usesOwnLayout: false },
};

views.explainer = {
  component: lazy(
    () => import("@/components/views/ExplainerView/ExplainerView")
  ),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ action, onNext }) => {
      return {
        instruction: action.instruction,
        buttonText: action.button_label,
        steps: action.steps,
        timer: action.timer,
        onNext,
      };
    },
    dependencies: ["action"],
  },
};

views.final = {
  component: lazy(() => import("@/components/views/FinalView/FinalView")),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ block, action, participant, onNext, experiment }) => {
      const timeline = frontendConfig?.tunetwins?.timeline;
      const numSteps = timeline?.symbols.length ?? timeline?.steps.length ?? 0;
      const sessionsPlayed = experiment.playedSessions ?? 0;
      const timelineStep = (sessionsPlayed % numSteps) + 1;

      return {
        block,
        participant,
        action_texts: action.action_texts,
        button: action.button,
        onNext,
        show_participant_link: action.show_participant_link,
        participant_id_only: action?.participant_id_only,
        show_profile_link: action.show_profile_link,
        social: action.social,
        feedback_info: action.feedback_info,
        percentile: action.percentile,
        score: action.score,
        totalScore: experiment.accumulatedScore + action.score,
        timeline: { ...timeline, currentStep: timelineStep },
      };
    },
    dependencies: ["block", "participant"],
  },
};

views.info = {
  component: lazy(() => import("@/components/views/InfoView/InfoView")),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ action, onNext }) => ({
      html: action?.body,
      title: action?.heading,
      buttonText: action?.button_label,
      buttonLink: action?.button_link,
      onButtonClick: onNext,
    }),
    dependencies: ["action"],
  },
};

views.landing = {
  component: lazy(() => import("@/components/views/LandingView/LandingView")),
  meta: { usesOwnLayout: false },
};

views.loading = {
  component: LoadingView,
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ label }) => ({ label }),
  },
};

views.playlists = {
  component: lazy(
    () => import("@/components/views/PlaylistsView/PlaylistsView")
  ),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ playlist, block, onNext, action }) => ({
      playlist,
      playlists: block?.playlists,
      onSelect: onNext,
      instruction: action.instruction,
      title: "Playlists...",
    }),
    dependencies: ["block", "action"],
  },
};

views.profile = {
  component: lazy(() => import("@/components/views/ProfileView/ProfileView")),
  meta: { usesOwnLayout: false },
};

views.trial = {
  component: lazy(() => import("@/components/application/Trial/Trial")),
  meta: {
    usesOwnLayout: true,
    getViewProps: ({ action, onNext, onResult, experiment }) => {
      let survey;
      if (action.feedback_form) {
        survey = {
          questions: action.feedback_form?.form,
          skippable: action.feedback_form?.is_skippable,
          submitLabel: action.feedback_form?.submit_label,
          skipLabel: action.feedback_form?.skip_label,
        };
      }

      return {
        playback: action.playback,
        html: action.html,
        survey,
        onNext,
        onResult,
        experiment,
        responseTime: action.config.response_time,
        autoAdvance: action.config.auto_advance,
        autoAdvanceTimer: action.config.auto_advance_timer,
        listenFirst: action.config.listen_first,
        showContinueButton: action.config.show_continue_button,
        continueLabel: action.config.continue_label,
        breakRoundOn: action.config.break_round_on,
      };
    },
    dependencies: ["action"],
  },
};

views.tunetwins = {
  component: lazy(
    () => import("@/components/matching-pairs/TuneTwins/TuneTwins")
  ),
  meta: {
    usesOwnLayout: true,
    getViewProps: ({
      playbackArgs,
      submitResult,
      onFinishedPlaying,
      playSection,
      experiment,
    }) => {
      const cards = playbackArgs.sections.map((section, index) => ({
        id: index,
        data: { boardposition: index + 1, ...section },
      }));
      const tutorial = convertTutorial(playbackArgs.tutorial);
      const timeline = frontendConfig?.tunetwins?.timeline;
      const numSteps = timeline?.symbols.length ?? timeline?.steps.length ?? 0;
      const sessionsPlayed = experiment.playedSessions ?? 0;
      const timelineStep = sessionsPlayed % numSteps;

      return {
        cards,
        animate: playbackArgs.show_animation,
        onGameEnd: () => submitResult({}),
        onTurnEnd: onFinishedPlaying,
        onSelectCard: (card) => playSection(card.id),
        tutorial,
        timeline: { ...timeline, currentStep: timelineStep },
        feedbackMessages: frontendConfig?.tunetwins?.feedbackMessages,
      };
    },
  },
};

views.score = {
  component: lazy(() => import("@/components/views/ScoreView/ScoreView")),
  meta: {
    usesOwnLayout: false,
    getViewProps: ({ action, onNext }) => ({
      last_song: action.last_song,
      score_meesage: action.score_meesage,
      total_score: action.total_score,
      texts: action.texts,
      icon: action.icon,
      feedback: action.feedback,
      timer: action.timer,
      onNext,
    }),
    dependencies: ["action"],
  },
};

views.storeProfile = {
  component: lazy(
    () => import("@/components/views/StoreProfileView/StoreProfileView")
  ),
  meta: { usesOwnLayout: false },
};

views.survey = {
  component: lazy(() => import("@/components/views/SurveyView/SurveyView")),
  meta: { usesOwnLayout: true },
};
