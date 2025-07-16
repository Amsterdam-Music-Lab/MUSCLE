/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ReactNode } from "react";
import { useEffect } from "react";
import { Button } from "@/components/buttons";
import { Card, List } from "@/components/ui";
import { Explainer as ExplainerAction } from "@/types/Action";
import { Logo } from "@/components/svg";
import { useLingui } from "@lingui/react/macro";

//  asdf

export interface ExplainerViewProps extends ExplainerAction {
  onNext: () => void;

  /** Label to show on the button. Default to "next" */
  buttonText?: ReactNode;

  /** Title for the card. Default to "Instructions" */
  title?: ReactNode;
}

/**
 * Explainer is a block view that shows a list of steps.
 * If the button has not been clicked, `onNext` will be called automatically after the timer expires (in milliseconds).
 * If `timer == null`, `onNext` will only be called after the button is clicked.
 */
export default function ExplainerView({
  instruction,
  buttonText,
  steps = [],
  timer = null,
  onNext,
  title,
}: ExplainerViewProps) {
  const { t } = useLingui();
  useEffect(() => {
    if (timer != null) {
      const id = setTimeout(onNext, timer);
      return () => {
        clearTimeout(id);
      }; // if button has been clicked, clear timeout
    }
  }, [onNext, timer]);

  return (
    <>
      {/* TODO Use plugin system! */}
      <Logo name="tunetwins" fill="#fff" style={{ height: "3em" }} />

      <Card data-testid="explainer">
        <Card.Header title={title ?? t`Instructions`}>
          {instruction}
        </Card.Header>

        {steps.length > 0 && (
          <Card.Section>
            <List
              items={steps.map((step) => ({
                content: step.description,
                label: step.number,
              }))}
              delay={250}
            />
          </Card.Section>
        )}
      </Card>

      <Button
        className="anim anim-fade-in anim-speed-300"
        onClick={onNext}
        style={{ animationDelay: steps.length * 300 + "ms" }}
        stretch={true}
        size="lg"
        rounded={false}
        variant="secondary"
      >
        {buttonText ?? t`Next`}
      </Button>
    </>
  );
}
