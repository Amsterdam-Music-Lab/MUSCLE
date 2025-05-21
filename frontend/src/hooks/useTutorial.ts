/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState } from "react";
import { type Tutorial, type TutorialStep } from "@/types/tutorial";

const DEFAULT_CONFIG = {
  disableCompleted: true,
  allowMultipleActiveSteps: false,
  inferOrder: true,
};

interface UseTutorialProps extends Omit<Tutorial, "steps"> {
  /** The tutorial object */
  tutorial?: Tutorial;
}

/**
 * A hook for implementing tutorial functionality. You provide one tutorial object
 * that specifies all steps in the tutorial. The hook takes care of handling state.
 * In your use case, you can call `getActiveStep` to get the step objects which you
 * can then visualize in whatever way fits you. If `allowMultipleActiveSteps` is
 * true, you can use `getActiveSteps` to get all active steps.
 */
export const useTutorial = ({ tutorial, ...config }: UseTutorialProps) => {
  if (!tutorial) {
    return {
      steps: undefined,
      showStep: () => {},
      completeStep: () => {},
      getActiveSteps: () => false,
      getActiveStep: () => false,
    };
  }

  // Determine configuration: default values, values in the tutorial object,
  // or finally overrides passed to the hook.
  const { steps: _steps, ...rest } = tutorial;
  config = { ...DEFAULT_CONFIG, ...rest, ...config };

  const [steps, setSteps] = useState<Record<string, TutorialStep>>(() => {
    const initialSteps: Record<string, TutorialStep> = {};
    tutorial.steps.forEach((step, index) => {
      initialSteps[step.id] = {
        ...step,
        order: config.inferOrder ? index : step.order,
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
    if (config.disableCompleted && steps[id].completed) return;
    if (steps[id].visible) return;

    setSteps((prevSteps) => {
      const updatedSteps = { ...prevSteps };

      if (!config.allowMultipleActiveSteps) {
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
    if (config.allowMultipleActiveSteps === false) {
      return getActiveSteps()[0] || null;
    } else {
      throw new Error(
        "getActiveStep can only be used when allowMultipleActiveSteps is true."
      );
    }
  };

  return {
    steps,
    showStep,
    completeStep,
    getActiveSteps,
    getActiveStep,
  };
};
