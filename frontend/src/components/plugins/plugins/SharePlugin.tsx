/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { Variant } from "@/types/themeProvider";
import type { ShareConfig } from "@/types/share";
import { t } from "@lingui/macro";
import { ShareOptions } from "@/components/modules";
import { ExpandableButton } from "@/components/buttons";

interface SharePluginProps {
  config: ShareConfig;
  variant?: Variant;
  label?: string;
}

function SharePlugin({
  config,
  label = t`Share`,
  variant = "secondary",
}: SharePluginProps) {
  return (
    <ExpandableButton title={label} rounded={true} variant={variant}>
      <ShareOptions config={config!} />
    </ExpandableButton>
  );
}

function isVisible(props: SharePluginProps) {
  return Boolean(props?.config);
}

export interface SharePluginArgs extends SharePluginProps {}

export interface SharePluginMeta extends PluginMeta<SharePluginArgs> {
  name: "share";
}

export interface SharePluginSpec extends PluginSpec<SharePluginArgs> {
  name: "share";
}

export const sharePlugin: SharePluginMeta = {
  name: "share",
  component: SharePlugin,
  description: "Displays an expandable button with sharing options",
  defaultSpecs: {
    isVisible,
  },
};
