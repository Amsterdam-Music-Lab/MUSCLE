/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ComponentType } from "react";
import { NarrowLayout } from "@/components/layout";

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
  DashboardView,
} from "@/components/views";

// Controller views
import { Trial } from "../";

// Other views
import { TuneTwins } from "@/components/matching-pairs";

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
  [DashboardView.viewName]: DashboardView,
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
  block,
  participant,
  experiment,
  onNext,
  onResult,
  session,
  playlist,
  ...viewPropsOverrides
}: ViewProps) {
  let viewProps = {};
  const ViewComponent = viewComponents[name] || ErrorView;
  if (!Object.keys(viewComponents).includes(name)) {
    viewProps.message = `Invalid view name "${name}"`;
  }

  if (typeof ViewComponent.getViewProps === "function") {
    // Ensure all the required dependencies are defined and throw an error otherwise
    const deps = ViewComponent.dependencies ?? [];
    const throwError = (varName: ViewDependency) => {
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
      ...viewPropsOverrides,
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
