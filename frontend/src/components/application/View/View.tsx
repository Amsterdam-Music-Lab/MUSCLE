/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { ComponentType } from "react";
import { Suspense, Fragment, useMemo } from "react";
import { NarrowLayout, ViewTransition } from "@/components/layout";
import { FloatingActionButton } from "@/components/buttons";
import { FeedbackForm } from "@/components/modules";

import { useLingui } from "@lingui/react/macro";
import { views, LoadingView } from "@/components/views";
import useBoundStore from "@/util/stores";
import Action from "@/types/Action";
import Block from "@/types/Block";
import Participant from "@/types/Participant";
import Session from "@/types/Session";
import { RenderHtml } from "@/components/utils";
import { useSubmitFeedback } from "@/components/modules";

export type ViewDependency = "block" | "action" | "participant" | "session";

export interface GetViewPropsArgs {
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

export interface ViewProps {
  name: string;
  block?: Block;
  action?: Action;
  session?: Session;
  participant?: Participant;
}

export default function View({ name, ...viewProps }: ViewProps) {
  const { t } = useLingui();
  // Use state
  const setError = useBoundStore((state) => state.setError);
  const block = useBoundStore((state) => state.block);
  const action = useBoundStore((state) => state.currentAction);
  const session = useBoundStore((state) => state.session);
  const participant = useBoundStore((state) => state.participant);

  // Get ViewComponent and viewMeta
  const entry = useMemo(() => views[name], [name]);
  if (!entry) {
    console.error(`View "${name}" not found`);
    setError(t`Invalid view name "${name}"`);
  }
  const { component: ViewComponent, meta: viewMeta } = entry;

  // Compute viewProps (memoized for performance reasons)
  const computedViewProps = useMemo(() => {
    if (typeof viewMeta.getViewProps !== "function") {
      return viewProps;
    }
    const deps = viewMeta.dependencies ?? [];

    // Validate required dependencies
    const throwError = (varName: ViewDependency) => {
      setError(
        t`Required dependency "${varName}" for view "${name}" is not defined`
      );
    };

    if (deps.includes("block") && !block) throwError("block");
    if (deps.includes("action") && !action) throwError("action");
    if (deps.includes("participant") && !participant) throwError("participant");
    if (deps.includes("session") && !session) throwError("session");

    try {
      return viewMeta.getViewProps({
        block,
        action,
        participant,
        session,
        ...viewProps,
      });
    } catch (e) {
      setError(
        t`An error occurred while trying to render the view "${name}". The properties required to show the view could not be computed.\n (${e})`
      );
      return viewProps; // fallback
    }
  }, [
    viewMeta,
    viewProps,
    block,
    action,
    participant,
    session,
    name,
    setError,
    t
  ]);

  const Wrapper = viewMeta.usesOwnLayout ? Fragment : NarrowLayout;

  const onSubmitFeedback = useSubmitFeedback(block?.slug, participant);

  return (
    <ViewTransition transitionKey={name}>
      <Wrapper>
        <Suspense fallback={<LoadingView />}>
          <ViewComponent {...computedViewProps} />
        </Suspense>

        {block && block?.feedback_info?.show_float_button && (
          <FloatingActionButton
            iconName="comment"
            title={t`Your feedback`}
            showFooter={false}
          >
            <FeedbackForm
              onSubmit={onSubmitFeedback}
              thanks={block?.feedback_info.thank_you}
              // header={block?.feedback_info?.header}
              footer={
                <RenderHtml
                  html={block?.feedback_info?.contact_body}
                  className="text-muted"
                />
              }
            />
          </FloatingActionButton>
        )}
      </Wrapper>
    </ViewTransition>
  );
}
