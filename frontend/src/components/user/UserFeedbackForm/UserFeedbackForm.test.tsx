/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, describe, it, expect } from "vitest";
import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import UserFeedbackForm from "./UserFeedbackForm";
import { postFeedback } from "@/API";

// Mock the API call
vi.mock("@/API", () => ({ postFeedback: vi.fn() }));

describe("UserFeedbackForm", () => {
  const mockBlockSlug = "test-slug";
  const mockParticipant = { id: 1 };
  const mockFeedbackInfo = {
    header: "Your Feedback",
    button: "Submit",
    contact_body: "Contact us at test@example.com",
    thank_you: "Thank you for your feedback!",
    show_float_button: true,
  };

  it("renders the feedback form", () => {
    const { getByText, getByRole } = render(
      <UserFeedbackForm
        blockSlug={mockBlockSlug}
        participant={mockParticipant}
        feedbackInfo={mockFeedbackInfo}
      />
    );

    expect(getByText(mockFeedbackInfo.header)).toBeTruthy();
    expect(getByRole("textbox")).toBeTruthy();
    expect(getByText(mockFeedbackInfo.button)).toBeTruthy();
  });

  it("allows input to be entered", () => {
    const { getByRole } = render(
      <UserFeedbackForm
        blockSlug={mockBlockSlug}
        participant={mockParticipant}
        feedbackInfo={mockFeedbackInfo}
      />
    );

    const input = getByRole("textbox");
    fireEvent.change(input, { target: { value: "Great experience!" } });

    expect(input.value).toBe("Great experience!");
  });

  it("submits feedback and shows thank you message", async () => {
    (postFeedback as any).mockResolvedValueOnce({});

    render(
      <UserFeedbackForm
        blockSlug={mockBlockSlug}
        participant={mockParticipant}
        feedbackInfo={mockFeedbackInfo}
      />
    );

    const textarea = screen.getByRole("textbox");
    const button = screen.getByRole("button", {
      name: mockFeedbackInfo.button,
    });

    fireEvent.change(textarea, { target: { value: "Great experience!" } });
    fireEvent.click(button);

    await waitFor(() =>
      expect(postFeedback).toHaveBeenCalledWith({
        blockSlug: mockBlockSlug,
        feedback: "Great experience!",
        participant: mockParticipant,
      })
    );

    expect(
      await screen.findByText(mockFeedbackInfo.thank_you)
    ).toBeInTheDocument();
  });
});
