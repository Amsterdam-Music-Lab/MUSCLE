/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";

export interface ConditionalRenderProps {
  /**
   * The condition to be tested. The children are only returned if
   * the condition is true.
   */
  condition: boolean;

  /** Children shown when condition is `true`. */
  children?: ReactNode;

  /** A fallback component that is shown if condition is `false`. */
  fallback?: ReactNode;
}

/**
 * Returns the children if the specified condition is met, or otherwise
 * the fallback component.
 */
export default function ConditionalRender({
  condition,
  children,
  fallback,
}: ConditionalRenderProps) {
  return condition ? children : fallback || null;
}
