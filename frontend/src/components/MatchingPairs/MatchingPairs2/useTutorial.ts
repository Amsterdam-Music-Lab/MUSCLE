/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import { useState } from "react";

/**
 * A tutorial object.
 * Note that it is not a list of steps, as this object may be extended
 * with other properties (e.g. description, title, ...)
 */
export interface Tutorial {
  steps: TutorialStep[];
}

export interface TutorialStep {
  /** A unique identifier for the step  */
  id: string;

  /** Title of the current step */
  title?: string;

  /** The content shown for this step */
  content?: string | React.ReactNode;

  /** Whether this step is visible */
  visible?: boolean;

  /** Whether this step has been completed */
  completed?: boolean;

  /** Order of the steps. */
  order?: number;
}

interface UseTutorialProps {
  /** The tutorial object */
  tutorial: Tutorial;

  /** Whether to disable completed steps (default: true) */
  disableCompleted?: boolean;

  /** Allow multiple steps to be active at the same time? (default: false) */
  allowMultipleActiveSteps?: boolean;

  /** Whether to infer the order of the steps from the input (default: true) */
  inferOrder?: boolean;
}

/**
 * A hook for implementing tutorial functionality. You provide one tutorial object
 * that specifies all steps in the tutorial. The hook takes care of handling state.
 * In your use case, you can call `getActiveStep` to get the step objects which you
 * can then visualize in whatever way fits you. If `allowMultipleActiveSteps` is
 * true, you can use `getActiveSteps` to get all active steps.
 */
export const useTutorial = ({
  tutorial,
  disableCompleted = true,
  inferOrder = true,
  allowMultipleActiveSteps = false,
}: UseTutorialProps) => {
  const [steps, setSteps] = useState<Record<string, TutorialStep>>(() => {
    const initialSteps: Record<string, TutorialStep> = {};
    tutorial.steps.forEach((step, index) => {
      initialSteps[step.id] = {
        ...step,
        order: inferOrder ? index : step.order,
        completed: step.completed ?? false,
        visible: step.visible ?? false,
      };
    });
    return initialSteps;
  });

  /**
   * Shows the step with the given id
   */
  const showStep = (id: string) => {
    if (!steps[id]) return;
    if (disableCompleted && steps[id].completed) return;
    if (steps[id].visible) return;

    setSteps((prevSteps) => {
      const updatedSteps = { ...prevSteps };

      if (!allowMultipleActiveSteps) {
        // Hide all other steps if multiple active steps are not allowed
        Object.keys(updatedSteps).forEach((key) => {
          updatedSteps[key].visible = false;
        });
      }

      updatedSteps[id].visible = true;
      return updatedSteps;
    });
  };

  /**
   * Completes the step with the given id
   */
  const completeStep = (id: string) => {
    if (!steps[id]) return;
    if (steps[id].completed) return;

    setSteps((prevSteps) => {
      const updatedSteps = { ...prevSteps };
      updatedSteps[id].completed = true;
      updatedSteps[id].visible = false;
      return updatedSteps;
    });
  };

  /**
   * Returns an array of all active steps
   */
  const getActiveSteps = () => {
    return Object.values(steps).filter((step) => step.visible);
  };

  /**
   * Return the active step, or null if no steps are active. Can only be used
   * when allowMultipleActiveSteps is true.
   */
  const getActiveStep = () => {
    if (allowMultipleActiveSteps === false) {
      return getActiveSteps()[0] || null;
    } else {
      throw new Error(
        "getActiveStep can only be used when allowMultipleActiveSteps is true."
      );
    }
  };

  return {
    showStep,
    completeStep,
    getActiveSteps,
    getActiveStep,
  };
};
