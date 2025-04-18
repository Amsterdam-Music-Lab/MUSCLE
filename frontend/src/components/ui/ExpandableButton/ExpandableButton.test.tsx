/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it } from "vitest";
import { fireEvent } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import ExpandableButton from "./ExpandableButton";
import styles from "./ExpandableButton.module.scss";

describe("Button component", () => {
  it("renders the button with the correct title and no expanded content by default", () => {
    const { container, getByText } = render(
      <ExpandableButton title="Click me">Content</ExpandableButton>
    );
    const button = getByText("Click me");
    const content = container.querySelector(`.${styles.content}`);
    expect(button).toBeInTheDocument();
    expect(content).toBeVisible();
  });

  it("expands the content when the button is clicked", () => {
    const { getByText, getByTestId } = render(
      <ExpandableButton title="Click me" data-testid="container">
        <div data-testid="content">Content</div>
      </ExpandableButton>
    );

    fireEvent.click(getByText("Click me"));
    expect(getByTestId("content")).toBeVisible();
    expect(getByTestId("container")).toHaveAttribute("data-expanded", "true");
  });

  it("collapses the content when clicking outside the button", () => {
    const { getByTestId } = render(
      <div>
        <ExpandableButton
          title="Click me"
          expanded={true}
          data-testid="container"
        >
          Content
        </ExpandableButton>
        <div data-testid="outside">Outside</div>
      </div>
    );
    fireEvent.mouseDown(getByTestId("outside"));
    expect(getByTestId("container")).toHaveAttribute("data-expanded", "false");
  });

  it("does not collapse the button when disabled=true and expanded=true, even if clicking outside", () => {
    const { getByText, getByTestId } = render(
      <div>
        <ExpandableButton
          title="More"
          disabled={true}
          expanded={true}
          data-testid="container"
        >
          Content{" "}
        </ExpandableButton>
        <div data-testid="outside">Outside</div>
      </div>
    );
    fireEvent.mouseDown(getByTestId("outside"));
    expect(getByTestId("container")).toHaveAttribute("data-expanded", "true");
  });
});
