/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { describe, expect, test } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useTutorial } from "./useTutorial";
import type { Tutorial } from "@/types/tutorial";

const tutorial: Tutorial = {
  steps: [
    { id: "a", content: "Step A" },
    { id: "b", content: "Step B" },
  ],
  allowMultipleActiveSteps: false,
};

describe("useTutorial", () => {
  test("initially hides all steps", () => {
    const { result } = renderHook(() => useTutorial({ tutorial }));
    expect(result.current.getActiveSteps()).toHaveLength(0);
  });

  test("shows a step", () => {
    const { result } = renderHook(() => useTutorial({ tutorial }));
    act(() => {
      result.current.showStep("a");
    });
    const activeStep = result.current.getActiveStep();
    expect(activeStep.content).toBe("Step A");
    expect(activeStep.order).toBe(0);
    expect(activeStep.visible).toBeTruthy();
  });

  test("completes a step and hides it", () => {
    const { result } = renderHook(() => useTutorial({ tutorial }));
    act(() => {
      result.current.showStep("a");
      result.current.completeStep("a");
    });
    expect(result.current.getActiveSteps()).toHaveLength(0);
  });

  test("disables completed steps if configured", () => {
    const { result } = renderHook(() => useTutorial({ tutorial }));
    act(() => {
      result.current.showStep("a");
      result.current.completeStep("a");
      result.current.showStep("a");
    });
    expect(result.current.getActiveSteps()).toHaveLength(0);
  });

  test("getActiveStep returns the single active step", () => {
    const { result } = renderHook(() => useTutorial({ tutorial }));
    act(() => {
      result.current.showStep("b");
    });
    expect(result.current.getActiveStep()?.id).toBe("b");
  });

  test("throws if getActiveStep is used with allowMultipleActiveSteps=true", () => {
    const { result } = renderHook(() =>
      useTutorial({ tutorial, allowMultipleActiveSteps: true })
    );
    expect(() => result.current.getActiveStep()).toThrow();
  });
});
