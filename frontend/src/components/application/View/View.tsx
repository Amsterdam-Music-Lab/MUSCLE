import {
  ErrorView,
  InfoView,
  ExplainerView,
  FinalView,
  LandingView,
  LoadingView,
  PlaylistsView,
  ProfileView,
  ScoreView,
  StoreProfileView,
  Trial,
  ConsentView,
} from "@/components/views";
import { NarrowLayout } from "@/components/layout";
import { SurveyView } from "@/components/views/SurveyView";

const viewComponents = {
  [ConsentView.viewName]: ConsentView,
  [ErrorView.viewName]: ErrorView,
  [ExplainerView.viewName]: ExplainerView,
  [FinalView.viewName]: FinalView,
  [InfoView.viewName]: InfoView,
  [LandingView.viewName]: LandingView,
  [LoadingView.viewName]: LoadingView,
  [PlaylistsView.viewName]: PlaylistsView,
  profileView: ProfileView,
  // [ProfileView.viewName]: ProfileView,
  [ScoreView.viewName]: ScoreView,
  [SurveyView.viewName]: SurveyView,
  [StoreProfileView.viewName]: StoreProfileView,

  // using [Trial.viewName] raises testing issues?!
  trial: Trial,
};

export default function View({
  name,
  state,
  block,
  participant,
  experiment,
  onNext,
  onResult,
  session,
  playlist,
  ...viewPropsOverrides
}) {
  let viewProps = {};
  const ViewComponent = viewComponents[name] || ErrorView;
  if (!Object.keys(viewComponents).includes(name)) {
    viewProps.message = `Invalid view name "${name}"`;
  }

  if (typeof ViewComponent.getViewProps === "function") {
    if (!ViewComponent?.dependencies) {
      throw new Error("The dependencies of getViewProps are not specified.");
    }

    // Ensure all the required dependencies are defined and throw an error otherwise
    const deps = ViewComponent.dependencies;
    const throwError = (varName) => {
      throw new Error(
        `Required dependency "${varName}" for view "${ViewComponent.viewName}" is not defined`
      );
    };
    if (deps.includes("state") && !state) throwError("state");
    if (deps.includes("block") && !block) throwError("block");
    if (deps.includes("participant") && !participant) throwError("participant");
    if (deps.includes("session") && !session) throwError("session");
    if (deps.includes("playlist") && !playlist) throwError("playlist");
    if (deps.includes("experiment") && !experiment) throwError("experiment");
    if (deps.includes("onNext") && !onNext) throwError("onNext");
    if (deps.includes("onResult") && !onResult) throwError("onResult");

    // Compute the views default props
    const defaultProps = ViewComponent.getViewProps({
      state,
      block,
      participant,
      session,
      playlist,
      experiment,
      onNext,
      onResult,
    });
    viewProps = { ...defaultProps, ...viewProps };
  }

  viewProps = { ...viewProps, ...viewPropsOverrides };
  if (ViewComponent.usesOwnLayout !== false) {
    return <ViewComponent {...viewProps} />;
  } else {
    return (
      <NarrowLayout>
        <ViewComponent {...viewProps} />
      </NarrowLayout>
    );
  }
}
