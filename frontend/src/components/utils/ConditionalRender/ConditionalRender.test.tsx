/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ConditionalRender from "./ConditionalRender";
import { render, screen } from "@testing-library/react";
import { it, expect, describe } from "vitest";

describe("ConditionalRender Component", () => {
  it("should render children when condition is true", () => {
    render(
      <ConditionalRender condition={true} fallback={<div>fallback</div>}>
        <div>children</div>
      </ConditionalRender>
    );

    expect(document.body.contains(screen.getByText("children"))).toBe(true);
    expect(document.body.contains(screen.queryByText("fallback"))).toBe(false);
  });

  it("should render fallback when condition is false", () => {
    render(
      <ConditionalRender condition={false} fallback={<div>fallback</div>}>
        <div>children</div>
      </ConditionalRender>
    );

    expect(document.body.contains(screen.getByText("fallback"))).toBe(true);
    expect(document.body.contains(screen.queryByText("children"))).toBe(false);
  });

  it("should render nothing when fallback is not provided and condition is false", () => {
    const { container } = render(
      <ConditionalRender condition={false}>
        <div>children</div>
      </ConditionalRender>
    );

    expect(container.firstChild).toBeNull();
  });
});
