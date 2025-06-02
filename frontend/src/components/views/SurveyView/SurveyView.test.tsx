/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { QuestionViews } from "@/types/Question";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import SurveyView from "./SurveyView";

const form = [
  {
    key: "test_question",
    view: QuestionViews.BUTTON_ARRAY,
    question: ["What is the average speed of a Swallow?"],
    choices: { slow: "1 km/h", fast: "42 km/h" },
  },
];

describe("SurveyView", () => {
  it("renders a heading, and a group of radio buttons", () => {
    render(<SurveyView form={form} />);
    const heading = screen.getByRole("heading", {
      name: "What is the average speed of a Swallow?",
    });
    expect(heading).toBeTruthy();
    expect(heading.textContent).toBe("What is the average speed of a Swallow?");
    expect(screen.getByRole("group")).toBeTruthy();
    expect(screen.queryAllByRole("radio")[0]).toBeTruthy();
  });
});
