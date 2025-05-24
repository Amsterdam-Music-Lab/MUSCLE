/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import RenderHtml from "./RenderHtml";

describe("HTML", () => {
  it("renders the HTML content correctly", () => {
    const htmlContent = "<p>Test content</p>";
    const { container } = render(<RenderHtml html={htmlContent} />);
    expect(container.innerHTML).to.include(htmlContent);
  });

  it("applies a custom inner className", () => {
    const customClass = "custom-class";
    const { getByTestId } = render(
      <RenderHtml html="<div>Test</div>" innerClassName={customClass} />
    );
    const innerDiv = getByTestId("html-content");
    expect(innerDiv).toBeTruthy();
    expect(innerDiv.classList.contains(customClass)).toBe(true);
    expect(innerDiv.classList.contains("text-center")).toBe(false);
    expect(innerDiv.classList.contains("pb-3")).toBe(false);
  });

  it("renders complex HTML content", () => {
    const complexHTML = `
      <div>
        <h1>Title</h1>
        <p>Paragraph <strong>with bold text</strong></p>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
        </ul>
      </div>
    `;
    const { getByTestId } = render(<RenderHtml html={complexHTML} />);
    const inner = getByTestId("html-content");
    expect(inner.innerHTML).to.include("<h1>Title</h1>");
    expect(inner.innerHTML).to.include("<strong>with bold text</strong>");
    expect(inner.innerHTML).to.include("<li>Item 2</li>");
  });

  it("renders the outer html class", () => {
    const { container } = render(<RenderHtml html="<div>Test</div>" />);
    const outerDiv = container.firstChild;
    expect(outerDiv).toBeTruthy();
    expect(outerDiv.classList.contains("html")).toBe(true);
  });

  it("handles empty body content", () => {
    const { getByTestId } = render(<RenderHtml html="" />);
    expect(getByTestId("html-content").innerHTML).to.equal("");
  });

  it("handles TrustedHTML type for body prop", () => {
    const trustedHTML = {
      toString: () => "<p>Trusted HTML</p>",
    } as TrustedHTML;
    const { container } = render(<RenderHtml html={trustedHTML} />);
    expect(container.innerHTML).to.include("<p>Trusted HTML</p>");
  });
});
