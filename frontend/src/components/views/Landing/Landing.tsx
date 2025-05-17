/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PageProps } from "@/components/application";
import type { AllPluginSpec } from "@/components/plugins";

import { Page } from "@/components/application";
import { NarrowLayout } from "@/components/layout";
import { PluginRenderer } from "@/components/plugins";
import { Card } from "@/components/ui";

interface LandingPageProps extends PageProps {
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

export default function LandingPage({
  experimentUrl,
  plugins = DEFAULT_PLUGINS,
  ...pageProps
}: LandingPageProps) {
  if (plugins) {
    plugins = plugins.map((plugin) => {
      const updated: AllPluginSpec = { args: {}, ...plugin };
      if (plugin.name == "linkButton") {
        updated.args = { ...updated.args, link: experimentUrl };
      }
      return updated;
    });
  }
  return (
    <Page useBackendTheme={false} {...pageProps}>
      <NarrowLayout>
        {plugins ? (
          <PluginRenderer plugins={plugins as AllPluginSpec[]} />
        ) : (
          // Superfluous fallback
          <Card>
            <Card.Section title="An error occured">
              No plugins were specified, and so this page is empty...
            </Card.Section>
          </Card>
        )}
      </NarrowLayout>
    </Page>
  );
}
