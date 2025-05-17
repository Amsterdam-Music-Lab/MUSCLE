/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { AllPluginSpec } from "@/components/plugins/pluginRegistry";

export interface ViewConfig {
  /** An iterable of plugins to show on this view */
  plugins?: AllPluginSpec[];
}
export interface FinalViewConfig extends ViewConfig {}

export interface LandingViewConfig extends ViewConfig {}

export interface FrontendConfig {
  /** Whether to show the landing view */
  showLanding: boolean;

  /** Landing view configuration */
  landing?: LandingViewConfig;

  /** Final view */
  final?: FinalViewConfig;
}
