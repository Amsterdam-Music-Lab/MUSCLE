import { QuestionViews } from "@/types/Question";

import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Survey from "./Survey";

const form = [
  {
    key: "test_question",
    view: QuestionViews.BUTTON_ARRAY,
    question: ["What is the average speed of a Swallow?"],
    choices: { slow: "1 km/h", fast: "42 km/h" },
  },
];

describe("Survey", () => {
  it("renders a heading, and a group of radio buttons", () => {
    render(<Survey form={form} />);
    const heading = screen.getByRole("heading", {
      name: "What is the average speed of a Swallow?",
    });
    expect(heading).toBeTruthy();
    expect(heading.textContent).toBe("What is the average speed of a Swallow?");
    expect(screen.getByRole("group")).toBeTruthy();
    expect(screen.queryAllByRole("radio")[0]).toBeTruthy();
  });
});
