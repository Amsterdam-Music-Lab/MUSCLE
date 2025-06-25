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

function MockView({ name, onSubmit, questions, ...props }) {
  if (name === "survey") {
    return (
      <div data-testid="mock-view-survey" onClick={() => onSubmit(questions)} />
    );
  } else {
    return <div data-testid={`mock-view-${name}`} />;
  }
}

function MockPlayback({ finishedPlaying, onPreloadReady }) {
  return (
    <div
      data-testid="mock-playback"
      onClick={() => {
        finishedPlaying();
        onPreloadReady();
      }}
    >
      Mock Playback
    </div>
  );
}

vi.mock("@/components/application", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/application")>()),
  View: MockView,
  Playback: MockPlayback,
}));

vi.mock("@/components/utils", () => ({
  RenderHtml: ({ html }) => <div data-testid="mock-html">{html}</div>,
}));

const testQuestion = {
  key: "test_question",
  view: QuestionViews.BUTTON_ARRAY,
  question: ["What is the average speed of a Swallow?"],
  choices: { slow: "1 km/h", fast: "42 km/h" },
  style: {},
};

const survey = {
  questions: [testQuestion],
  submitLabel: "Submit",
  skipLabel: "Skip",
  skippable: false,
};

const defaultProps = {
  listenFirst: false,
  autoAdvance: false,
  responseTime: 5000,
  showContinueButton: false,
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
        {...defaultProps}
        survey={survey}
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
        {...defaultProps}
        playback={{ somePlaybackProp: true }}
        survey={survey}
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
        {...defaultProps}
        html={{ body: htmlBody }}
        survey={survey}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    const htmlComponent = getByTestId("mock-html");
    expect(htmlComponent).toBeTruthy();
    expect(htmlComponent.textContent).toBe(htmlBody);
  });

  it("renders FeedbackForm when surveyConfig prop is provided", () => {
    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        survey={survey}
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    expect(getByTestId("mock-view-survey")).toBeTruthy();
  });

  it("shows continue button when config.show_continue_button is true", () => {
    const { getByText } = render(
      <Trial
        {...defaultProps}
        showContinueButton={true}
        continueLabel="Continue"
        onNext={mockOnNext}
        onResult={mockOnResult}
      />
    );
    expect(getByText("Continue")).toBeTruthy();
  });

  it("calls onResult when FeedbackForm submits result", async () => {
    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        survey={survey}
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
    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        autoAdvance={true}
        playback={{ view: "AUTOPLAY" }}
        onNext={mockOnNext}
        onResult={mockOnResult}
        survey={survey}
      />
    );
    fireEvent.click(getByTestId("mock-playback"));
    expect(getByTestId("mock-view-survey")).toBeTruthy();
  });

  it("auto-advances after specified timer when config.auto_advance_timer is set", async () => {
    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        autoAdvance={true}
        autoAdvanceTimer={42}
        playback={{ view: "BUTTON" }}
        survey={survey}
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

    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        onNext={mockOnNext}
        onResult={mockOnResult}
        survey={{ ...survey, questions: undefined }}
      />
    );
    fireEvent.click(getByTestId("mock-view-survey"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
    });
  });

  it("calls onResult and onNext when form is not defined and break_round_on is met", async () => {
    const { getByTestId } = render(
      <Trial
        {...defaultProps}
        breakRoundOn={{ NOT: ["fast"] }}
        onNext={mockOnNext}
        onResult={mockOnResult}
        survey={{ ...survey, questions: undefined }}
      />
    );
    fireEvent.click(getByTestId("mock-view-survey"));
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalled();
      expect(mockOnNext).toHaveBeenCalled();
    });
  });
});
