/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, test, expect } from "vitest";
import createStarPath from "./createStarPath";

describe("createStarPath", () => {
  test("returns a valid path string with expected number of points", () => {
    const path = createStarPath({
      cx: 50,
      cy: 50,
      numPoints: 5,
      innerRadius: 20,
      outerRadius: 40,
    });

    // Should start with M and end with Z
    expect(path.startsWith("M")).toBe(true);
    expect(path.endsWith("Z")).toBe(true);

    // Should have 10 points = 9 "L" commands (first is "M")
    const segments = path.split(" ").filter((s) => s === "L");
    expect(segments.length).toBe(9);
  });

  test("returns a closed path even with 3 points", () => {
    const path = createStarPath({
      cx: 0,
      cy: 0,
      numPoints: 3,
      innerRadius: 5,
      outerRadius: 10,
    });

    expect(path.startsWith("M")).toBe(true);
    expect(path.endsWith("Z")).toBe(true);
    expect((path.match(/L/g) || []).length).toBe(5); // 6 points total
  });

  test("generates symmetric points for 4-point star centered at origin", () => {
    const path = createStarPath({
      cx: 0,
      cy: 0,
      numPoints: 4,
      innerRadius: 0,
      outerRadius: 10,
    });

    // Should produce a diamond (0,10)-(10,0)-(0,-10)-(-10,0)
    expect(path).toContain("M 10,0");
    expect(path).toContain("L 0,10");
    expect(path).toContain("L -10,0");
    expect(path).toContain("L 0,-10");
    expect(path.endsWith("Z")).toBe(true);
  });
});
