/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect } from "react";
import classNames from "classnames";
import { Button } from "@/components/buttons";
import { Card } from "@/components/ui";
import { Explainer as ExplainerAction } from "@/types/Action";
import { Logo } from "@/components/svg";
import styles from "./ExplainerView.module.scss";

export interface ExplainerViewProps extends ExplainerAction {
  onNext: () => void;
}

/**
 * Explainer is a block view that shows a list of steps
 * If the button has not been clicked, onNext will be called automatically after the timer expires (in milliseconds).
 * If timer == null, onNext will only be called after the button is clicked.
 */
export default function ExplainerView({
  instruction,
  button_label: buttonText = "Next",
  steps = [],
  timer = null,
  onNext,
  title = "Instructions...",
}: ExplainerViewProps) {
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
      <Card data-testid="explainer" className={classNames(styles.explainer)}>
        <Card.Header title={title}>{instruction}</Card.Header>

        {steps.length > 0 && (
          <Card.Section>
            <ul>
              {steps.map((step, index) => (
                <ExplainerItem
                  key={index}
                  number={step.number}
                  description={step.description}
                  delay={index * 250}
                />
              ))}
            </ul>
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
        {buttonText}
      </Button>
    </>
  );
}

ExplainerView.viewName = "explainer";
ExplainerView.usesOwnLayout = false;
ExplainerView.getViewProps = ({ action, onNext }) => ({
  instruction: action.instruction,
  button_label: action.button_label,
  steps: action.steps,
  timer: action.timer,
  onNext,
});
ExplainerView.dependencies = ["action", "onNext"];

interface ExplainerItemProps {
  number: number | null;
  description: string;
  delay?: number;
}

/** ExplainerItems renders an item in the explainer list, with optional icon or number */
const ExplainerItem = ({
  number = null,
  description,
  delay = 0,
}: ExplainerItemProps) => (
  <li
    className="anim anim-fade-in-slide-left anim-speed-300"
    style={{ animationDelay: delay + "ms" }}
  >
    {number != null && <span className={styles.number}>{number}</span>}
    <span>{description}</span>
  </li>
);
