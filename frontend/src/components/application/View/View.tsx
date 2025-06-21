/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ComponentType } from "react";
import { Fragment } from "react";
import { NarrowLayout, ViewTransition } from "@/components/layout";
import { FloatingActionButton } from "@/components/buttons";
import { UserFeedbackForm } from "@/components/modules";

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
import Action from "@/types/Action";
import Block from "@/types/Block";
import Participant from "@/types/Participant";
import Session from "@/types/Session";

export type ViewDependency = "block" | "action" | "participant" | "session";

interface GetViewPropsArgs {
  action?: Action;
  block?: Block;
  participant?: Participant;
  session?: Session;
}

export interface BaseViewComponent<P = any> {
  viewName: string;
  dependencies?: ViewDependency[];
  usesOwnLayout?: boolean;
  getViewProps?: (props: GetViewPropsArgs | any) => P;
}

export type ViewComponent<P = any> = ComponentType<P> & BaseViewComponent<P>;

const viewComponents: Record<string, ViewComponent<any>> = {
  [AboutView.viewName]: AboutView,
  [ConsentView.viewName]: ConsentView,
  [ConsentDeniedView.viewName]: ConsentDeniedView,
  [ErrorView.viewName]: ErrorView,
  [ExplainerView.viewName]: ExplainerView,
  [FinalView.viewName]: FinalView,
  [InfoView.viewName]: InfoView,
  [LandingView.viewName]: LandingView,
  [LoadingView.viewName]: LoadingView,
  [PlaylistsView.viewName]: PlaylistsView,
  [ProfileView.viewName]: ProfileView,
  [ScoreView.viewName]: ScoreView,
  [SurveyView.viewName]: SurveyView,
  [StoreProfileView.viewName]: StoreProfileView,
  [TuneTwins.viewName]: TuneTwins,

  // Use name directly as [View.viewName] raises test issues
  dashboard: DashboardView,
  trial: Trial,
};

export interface ViewProps {
  name: string;
  block?: Block;
  action?: Action;
  session?: Session;
  participant?: Participant;
}

export default function View({ name, ...viewProps }: ViewProps) {
  // Use state
  const setError = useBoundStore((state) => state.setError);
  const block = useBoundStore((state) => state.block);
  const action = useBoundStore((state) => state.currentAction);
  const session = useBoundStore((state) => state.session);
  const participant = useBoundStore((state) => state.participant);

  if (!Object.keys(viewComponents).includes(name)) {
    setError(`Invalid view name "${name}"`);
  }

  const ViewComponent = viewComponents[name];
  if (typeof ViewComponent.getViewProps === "function") {
    // Ensure all the required dependencies are defined and throw an error otherwise
    // This is mostly for debuggin purposes
    const throwError = (varName: ViewDependency) => {
      setError(
        `Required dependency "${varName}" for view "${ViewComponent.viewName}" is not defined`
      );
    };
    const deps = ViewComponent.dependencies ?? [];
    if (deps.includes("block") && !block) throwError("block");
    if (deps.includes("action") && !action) throwError("action");
    if (deps.includes("participant") && !participant) throwError("participant");
    if (deps.includes("session") && !session) throwError("session");

    // Compute the views default props
    try {
      viewProps = ViewComponent.getViewProps({
        block,
        action,
        participant,
        session,
        ...viewProps,
      });
    } catch (e) {
      setError(
        `An error occurred while trying to render the view "${name}". The properties required to show the view could not be computed.\n (${e})`
      );
    }
  }

  const Wrapper = ViewComponent.usesOwnLayout ? Fragment : NarrowLayout;

  return (
    <ViewTransition transitionKey={name}>
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
    </ViewTransition>
  );
}
