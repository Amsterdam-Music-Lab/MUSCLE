/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import { render, RenderOptions } from "@testing-library/react";
import { ThemeProvider } from "@/theme/ThemeProvider";

const Providers = ({ children }: { children: ReactNode }) => {
  // Add other providers if needed
  return <ThemeProvider>{children}</ThemeProvider>;
};

export const renderWithProviders = (
  ui: React.ReactElement,
  options: RenderOptions = {}
) => {
  let { wrapper, ...rest } = options;
  if (!wrapper) {
    wrapper = ({ children }) => children;
  }
  return render(ui, {
    wrapper: ({ children }) => <Providers children={wrapper({ children })} />,
    ...rest,
  });
};
