/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import { render, RenderOptions } from "@testing-library/react";
import { i18n } from "@lingui/core";
import { I18nProvider } from "@lingui/react";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { messages as messagesEn } from "@/locales/en/messages";

const Providers = ({ children }: { children: ReactNode }) => {
  // i18n setup
  i18n.load("en", messagesEn);
  i18n.activate("en");

  // Add other providers if needed
  return (
    <I18nProvider i18n={i18n}>
      <ThemeProvider>{children}</ThemeProvider>
    </I18nProvider>
  );
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
