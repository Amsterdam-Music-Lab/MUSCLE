/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { describe, test, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import InfoView from "./InfoView";

describe("InfoView Component", () => {
  test("renders without crashing", () => {
    render(<InfoView html="Test body" />);
    expect(screen.getByText("Test body")).toBeTruthy();
  });

  test("renders heading when provided", () => {
    render(<InfoView title="Test Heading" html="Test body" />);
    expect(screen.getByText("Test Heading")).toBeTruthy();
  });

  test("does not render heading when not provided", () => {
    render(<InfoView html="Test body" />);
    expect(screen.queryByRole("heading")).toBeNull();
  });

  test("renders button link when button_label & button_link is provided", () => {
    render(
      <InfoView
        html="Test body"
        buttonText="Click me"
        buttonLink="https://example.com"
        responsiveHeight={true}
      />
    );
    const anchor = screen.getByText("Click me");
    expect(anchor).toBeTruthy();
    expect(anchor?.textContent).toBe("Click me");
    expect(anchor.tagName).toBe("A");
  });

  test("renders button when button_label & onNext is provided", () => {
    render(
      <InfoView
        html="Test body"
        buttonText="Click me"
        onButtonClick={vi.fn()}
      />
    );
    const button = screen.queryByRole("button");
    expect(button).toBeTruthy();
    expect(button?.textContent).toBe("Click me");
    expect(button?.tagName).toBe("BUTTON");
  });

  test("does not render button without link and onNext when only button_label is provided", () => {
    render(<InfoView html="Test body" buttonText="Click me" />);
    expect(screen.queryByRole("button")).toBeNull();
  });

  test("does not render button when button_label is not provided", () => {
    render(<InfoView html="Test body" />);
    expect(screen.queryByRole("button")).toBeNull();
  });

  test("renders anchor tag when button_link is provided", () => {
    render(
      <InfoView
        html="Test body"
        buttonText="Click me"
        buttonLink="https://example.com"
      />
    );
    const anchor = screen.getByText("Click me");
    expect(anchor.getAttribute("href")).toBe("https://example.com");
    expect(anchor.getAttribute("target")).toBe("_blank");
    expect(anchor.getAttribute("rel")).toBe("noopener noreferrer");
  });

  test("renders button without link when only button_label is provided", () => {
    const onNextMock = vi.fn();
    render(
      <InfoView
        html="Test body"
        buttonText="Click me"
        onButtonClick={onNextMock}
      />
    );
    const button = screen.getByText("Click me");
    expect(button.tagName).toBe("BUTTON");
  });

  test("calls onNext when button is clicked", () => {
    const onNextMock = vi.fn();
    render(
      <InfoView
        html="Test body"
        buttonText="Click me"
        onButtonClick={onNextMock}
      />
    );
    fireEvent.click(screen.getByText("Click me"));
    expect(onNextMock).toHaveBeenCalledTimes(1);
  });

  test("renders body content as HTML", () => {
    const html = "<p>Test <strong>body</strong></p>";
    const { getByTestId } = render(<InfoView html={html} />);
    expect(getByTestId("info-body").innerHTML).to.contain(html);
  });

  test("applies max-height style to info-body", () => {
    const { getByTestId } = render(
      <InfoView html="Test body" responsiveHeight={true} />
    );
    expect(getByTestId("info-body").style.maxHeight).toBeTruthy();
  });

  test("updates max-height on window resize", async () => {
    const { rerender } = render(
      <InfoView html="Test body" responsiveHeight={true} />
    );
    const initialHeight = screen.getByTestId("info-body").style.maxHeight;

    // Simulate window resize
    window.innerHeight = 1001;
    window.dispatchEvent(new Event("resize"));
    rerender(<InfoView html="Test body" />);

    const updatedHeight =
      screen.getByText("Test body").parentElement?.style.maxHeight;
    expect(updatedHeight).not.toBe(initialHeight);
  });
});
