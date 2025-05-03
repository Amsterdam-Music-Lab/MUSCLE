/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginSpec } from "@/components/ui";
import type { LogoProps } from "@/components/svg";
import { Logo } from "@/components/svg";

function LogoPlugin(props: LogoProps) {
  return <Logo {...props} />;
}

LogoPlugin._defaults = {
  args: {
    variant: "primary",
    style: { height: "2.5em", marginLeft: "1em" },
  },
  style: { display: "flex", justifyContent: "start" },
} as Partial<PluginSpec>;

LogoPlugin._name = "logo";

export default LogoPlugin;
