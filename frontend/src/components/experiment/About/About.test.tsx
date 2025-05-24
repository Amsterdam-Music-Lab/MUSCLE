/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import { it, expect, describe } from "vitest";
import About from "./About";

describe("About", () => {
  it("shows the about page content", () => {
    const content = "## Hello World!\n\n**Lorem ipsum**";

    render(<About content={content} />, { wrapper: Router });

    expect(screen.getByRole("contentinfo").innerHTML).toContain("Hello World!");
    expect(screen.getByRole("contentinfo").innerHTML).toContain("Lorem ipsum");
  });

  it('shows a "Terug" button with a link to the previous page based on a given slug', () => {
    const content = "## Hello World!\n\n**Lorem ipsum**";

    render(
      <About content={content} slug="some_slug" backButtonText="Terug" />,
      { wrapper: Router }
    );

    expect(screen.getByRole("link").innerHTML).toContain("Terug");
    expect(screen.getByRole("link").getAttribute("href")).toBe("/some_slug");
  });
});
