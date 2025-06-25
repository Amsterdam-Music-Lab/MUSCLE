/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, describe, it, expect } from "vitest";
import { render, fireEvent, waitFor } from "@testing-library/react";
import FeedbackForm from "./FeedbackForm";

const mockOnSubmit = vi.fn();

describe("FeedbackForm", () => {
  it("renders the feedback form", () => {
    const { getByText, getByRole } = render(
      <FeedbackForm
        onSubmit={mockOnSubmit}
        header={<p>My header</p>}
        footer={<p>My footer</p>}
      />
    );

    expect(getByText("My header")).toBeTruthy();
    expect(getByRole("textbox")).toBeTruthy();
    expect(getByText("My footer")).toBeTruthy();
  });

  it("allows input to be entered", () => {
    const { getByRole } = render(<FeedbackForm onSubmit={mockOnSubmit} />);
    const input = getByRole("textbox");
    fireEvent.change(input, { target: { value: "Great experience!" } });
    expect(input.value).toBe("Great experience!");
  });

  it("submits feedback and shows thank you message on success", async () => {
    const mockOnSubmit = vi.fn(() => ({ status: "ok" }));
    const { getByRole, findByText } = render(
      <FeedbackForm onSubmit={mockOnSubmit} thanks={<p>Thanks</p>} />
    );
    fireEvent.change(getByRole("textbox"), { target: { value: "Great!" } });
    fireEvent.click(getByRole("button"));

    await waitFor(() => expect(mockOnSubmit).toHaveBeenCalledWith("Great!"));
    expect(await findByText("Thanks")).toBeInTheDocument();
  });
});
