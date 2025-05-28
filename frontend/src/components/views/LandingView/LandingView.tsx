/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { NarrowLayoutProps } from "@/components/layout";
import type { AllPluginSpec } from "@/components/plugins";
import { PluginRenderer } from "@/components/plugins";

interface LandingViewProps extends NarrowLayoutProps {
  /**
   * Url to the actual experiment
   */
  experimentUrl: string;

  /**
   * Plugins to render on the landing page. In particular, the linkButton
   * plugin will be populated with the experimentUrl.
   */
  plugins?: AllPluginSpec[];
}

const DEFAULT_PLUGINS = [
  {
    name: "linkButton",
    args: {
      children: "Start the game!",
    },
  },
] as AllPluginSpec[];

export default function LandingView({
  experimentUrl,
  plugins = DEFAULT_PLUGINS,
  ...layoutProps
}: LandingViewProps) {
  if (plugins) {
    plugins = plugins.map((plugin) => {
      const updated: AllPluginSpec = { args: {}, ...plugin };
      if (plugin.name === "linkButton") {
        updated.args = { ...updated.args, link: experimentUrl };
      }
      return updated;
    });
  }
  return <PluginRenderer plugins={plugins as AllPluginSpec[]} />;
}

LandingView.viewName = "landing";
LandingView.usesOwnLayout = false;
LandingView.getViewProps = undefined;
