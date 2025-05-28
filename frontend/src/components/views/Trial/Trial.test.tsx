/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render, fireEvent, waitFor } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { QuestionViews } from "@/types/Question";
import Trial from "./Trial";

function MockView({ name, ...props }) {
  if (name === "survey") {
    return <div data-testid="mock-view-survey" onClick={props.submitResult} />;
  } else {
    return <div data-testid={`mock-view-${name}`} />;
  }
}

vi.mock("@/components/application", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/application")>()),
  View: MockView,
}));

vi.mock("@/components/playback", () => ({
  Playback: vi.fn(({ finishedPlaying, onPreloadReady }) => (
    <div
      data-testid="mock-playback"
      onClick={() => {
        finishedPlaying();
        onPreloadReady();
      }}
    >
      Mock Playback
    </div>
  )),
}));

vi.mock("@/components/utils", () => ({
  RenderHtml: ({ html }) => <div data-testid="mock-html">{html}</div>,
}));

const feedback_form = {
  form: [
    {
      key: "test_question",
      view: QuestionViews.BUTTON_ARRAY,
      question: ["What is the average speed of a Swallow?"],
      choices: { slow: "1 km/h", fast: "42 km/h" },
      style: {},
    },
  ],
  submit_label: "Submit",
  skip_label: "Skip",
  is_skippable: false,
};

const defaultConfig = {
  listen_first: false,
  auto_advance: false,
  response_time: 5000,
  show_continue_button: false,
};

describe("Trial", () => {
  const mockOnNext = vi.fn();
  const mockOnResult = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders itself", () => {
    const { container } = render(
      <Trial
        feedback_form={feedback_form}
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    // Not ideal but the trial doesn't export any constant elements,
    // (it exports a fragment), so what else to do...
    expect(container.innerHTML).toBeTruthy();
  });

  it("renders Playback component when playback prop is provided", () => {
    const { getByTestId } = render(
      <Trial
        playback={{ somePlaybackProp: true }}
        feedback_form={feedback_form}
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    expect(getByTestId("mock-playback")).toBeTruthy();
  });

  it("renders HTML component when html prop is provided", () => {
    const htmlBody = "Test HTML content";
    const { getByTestId } = render(
      <Trial
        html={{ body: htmlBody }}
        feedback_form={feedback_form}
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    const htmlComponent = getByTestId("mock-html");
    expect(htmlComponent).toBeTruthy();
    expect(htmlComponent.textContent).toBe(htmlBody);
  });

  it("renders FeedbackForm when feedback_form prop is provided", () => {
    const { getByTestId } = render(
      <Trial
        feedback_form={feedback_form}
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    expect(getByTestId("mock-view-survey")).toBeTruthy();
  });

  it("shows continue button when config.show_continue_button is true", () => {
    const config = {
      ...defaultConfig,
      show_continue_button: true,
      continue_label: "Continue",
    };
    const { getByText } = render(
      <Trial config={config} onNext={mockOnNext} onResult={mockOnResult} />
    );
    expect(getByText("Continue")).toBeTruthy();
  });

  it("calls onResult when FeedbackForm submits result", async () => {
    const { getByTestId } = render(
      <Trial
        feedback_form={feedback_form}
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    fireEvent.click(getByTestId("mock-view-survey"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
    });
  });

  it("calls finishedPlaying when Playback component finishes", () => {
    // TODO does this test actually check if finishedPlaying is called?
    const config = { ...defaultConfig, auto_advance: true };
    const { getByTestId } = render(
      <Trial
        playback={{ view: "AUTOPLAY" }}
        config={config}
        onNext={mockOnNext}
        onResult={mockOnResult}
        feedback_form={feedback_form}
      />
    );
    fireEvent.click(getByTestId("mock-playback"));
    expect(getByTestId("mock-view-survey")).toBeTruthy();
  });

  it("auto-advances after specified timer when config.auto_advance_timer is set", async () => {
    const config = {
      ...defaultConfig,
      auto_advance: true,
      auto_advance_timer: 42,
    };
    const { getByTestId } = render(
      <Trial
        playback={{ view: "BUTTON" }}
        config={config}
        feedback_form={feedback_form}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    fireEvent.click(getByTestId("mock-playback"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
      expect(mockOnResult).toHaveBeenCalledWith(
        expect.objectContaining({
          decision_time: expect.any(Number),
          form: expect.arrayContaining([
            expect.objectContaining({
              key: "test_question",
              value: "TIMEOUT",
            }),
          ]),
        })
      );
    });
  });

  it("calls onResult when form is not defined", async () => {
    // TODO Does this test really make sense, or does it essentially test whether the
    // mock fires a click event correctly?
    const formless_feedback_form = {
      ...feedback_form,
      form: undefined,
    };
    const { getByTestId } = render(
      <Trial
        config={defaultConfig}
        onNext={mockOnNext}
        onResult={mockOnResult}
        feedback_form={formless_feedback_form}
      />
    );
    fireEvent.click(getByTestId("mock-view-survey"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
    });
  });

  it("calls onResult and onNext when form is not defined and break_round_on is met", async () => {
    const formless_feedback_form = {
      ...feedback_form,
      form: undefined,
    };
    const config = {
      ...defaultConfig,
      break_round_on: { NOT: ["fast"] },
    };
    const { getByTestId } = render(
      <Trial
        config={config}
        onNext={mockOnNext}
        onResult={mockOnResult}
        feedback_form={formless_feedback_form}
      />
    );
    fireEvent.click(getByTestId("mock-view-survey"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
      expect(mockOnNext).toHaveBeenCalled();
    });
  });
});
