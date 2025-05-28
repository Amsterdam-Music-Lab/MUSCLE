/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import { it, expect, describe } from "vitest";
import AboutView from "./AboutView";

describe("AboutView", () => {
  it("shows the about page content", () => {
    const { getByText } = render(<AboutView content={"Hello world"} />, {
      wrapper: Router,
    });
    expect(getByText("Hello world")).not.toBeFalsy();
  });

  it('shows a "Terug" button with a link to the previous page based on a given slug', () => {
    const { getByText } = render(
      <AboutView content={"foo"} slug="some_slug" backButtonText="Terug" />,
      { wrapper: Router }
    );
    expect(getByText("Terug").getAttribute("href")).toBe("/redirect/some_slug");
  });
});
