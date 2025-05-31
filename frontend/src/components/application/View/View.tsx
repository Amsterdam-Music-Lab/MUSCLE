/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ComponentType } from "react";
import { Fragment } from "react";
import { NarrowLayout } from "@/components/layout";
import { FloatingActionButton } from "@/components/ui";
import { UserFeedbackForm } from "@/components/user";

// Simple views
import {
  AboutView,
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
  SurveyView,
  ConsentView,
  ConsentDeniedView,
  DashboardView,
} from "@/components/views";

// Controller views
import { Trial } from "../";

// Other views
import { TuneTwins } from "@/components/matching-pairs";
import useBoundStore from "@/util/stores";

export type ViewDependency =
  | "state"
  | "block"
  | "participant"
  | "experiment"
  | "onNext"
  | "onResult"
  | "session"
  | "playlist";

export interface BaseViewComponent<P = any> {
  viewName: string;
  dependencies?: ViewDependency[];
  usesOwnLayout?: boolean;
  getViewProps?: (deps: Record<string, any>) => P;
}

export type ViewComponent<P = any> = ComponentType<P> & BaseViewComponent<P>;

const viewComponents: Record<string, ViewComponent<any>> = {
  [AboutView.viewName]: AboutView,
  [ConsentView.viewName]: ConsentView,
  [ConsentDeniedView.viewName]: ConsentDeniedView,
  dashboard: DashboardView,
  [ErrorView.viewName]: ErrorView,
  [ExplainerView.viewName]: ExplainerView,
  [FinalView.viewName]: FinalView,
  [InfoView.viewName]: InfoView,
  [LandingView.viewName]: LandingView,
  [LoadingView.viewName]: LoadingView,
  [PlaylistsView.viewName]: PlaylistsView,
  [ProfileView.viewName]: ProfileView,
  // [ProfileView.viewName]: ProfileView,
  [ScoreView.viewName]: ScoreView,
  [SurveyView.viewName]: SurveyView,
  [StoreProfileView.viewName]: StoreProfileView,

  // using [Trial.viewName] raises testing issues?!
  trial: Trial,

  [TuneTwins.viewName]: TuneTwins,
};

export interface ViewProps {
  name: string;
  state?: any;
  block?: any;
  participant?: any;
  experiment?: any;
  onNext?: (...args: any[]) => void;
  onResult?: (...args: any[]) => void;
  session?: any;
  playlist?: any;
  [key: string]: any; // for overrides
}

export default function View({
  name,
  state,
  experiment,
  onNext,
  onResult,
  playlist,
  ...viewPropsOverrides
}: ViewProps) {
  // Use state
  const participant = useBoundStore((state) => state.participant);
  const block = useBoundStore((state) => state.block);
  const session = useBoundStore((state) => state.session);
  const setError = useBoundStore((state) => state.setError);

  const ViewComponent = viewComponents[name];
  const deps = ViewComponent.dependencies ?? [];
  if (!Object.keys(viewComponents).includes(name)) {
    setError(`Invalid view name "${name}"`);
  }

  let viewProps = {};
  if (typeof ViewComponent.getViewProps === "function") {
    // Ensure all the required dependencies are defined and throw an error otherwise
    // This is mostly for debuggin purposes
    const throwError = (varName: ViewDependency) => {
      setError(
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
    let defaultProps;
    try {
      defaultProps = ViewComponent.getViewProps({
        state,
        block,
        participant,
        session,
        playlist,
        experiment,
        onNext,
        onResult,
        ...viewPropsOverrides,
      });
    } catch (e) {
      setError(
        `An error occurred while trying to render the view "${name}". The properties required to show the view could not be computed.\n (${e})`
      );
    }
    viewProps = { ...defaultProps, ...viewProps };
  }

  const Wrapper = ViewComponent.usesOwnLayout ? Fragment : NarrowLayout;

  viewProps = { ...viewProps, ...viewPropsOverrides };
  return (
    <Wrapper>
      <ViewComponent {...viewProps} />

      {block && block?.feedback_info?.show_float_button && (
        <FloatingActionButton>
          <UserFeedbackForm
            blockSlug={block.slug}
            participant={participant}
            feedbackInfo={block.feedback_info}
            inline={false}
          />
        </FloatingActionButton>
      )}
    </Wrapper>
  );
}
