/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginSpec } from "@/components/ui";
import { ShareOptions, ExpandableButton, Card } from "@/components/ui";
import { ShareConfig } from "@/types/share";

import { Variant } from "@/types/themeProvider";

interface SharePluginProps {
  config: ShareConfig;
  variant?: Variant;
  label?: string;
}

function SharePlugin({
  config,
  label = "Share",
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

SharePlugin._defaults = { isVisible } as Partial<PluginSpec>;
SharePlugin._name = "share";

export default SharePlugin;
