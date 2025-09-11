/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { LogoProps } from "@/components/svg/Logo/Logo";
import Logo from "@/components/svg/Logo/Logo";

export interface LogoPluginArgs extends LogoProps {
  /** Height of the logo in ems */
  height?: number;

  /** Whether to center the logo */
  center?: boolean;
}

/**
 * Plugin that shows a logo. The alignment (centered true/false) and height (in ems)
 * can be specified.
 */
function LogoPlugin({ height = 3, center = true, ...props }: LogoPluginArgs) {
  return (
    <Logo
      {...props}
      style={{
        height: `${height}em`,
        alignSelf: center ? "center" : "baseline",
      }}
    />
  );
}

export interface LogoPluginMeta extends PluginMeta<LogoPluginArgs> {
  name: "logo";
}

export interface LogoPluginSpec extends PluginSpec<LogoPluginArgs> {
  name: "logo";
}

export const logoPlugin: LogoPluginMeta = {
  name: "logo",
  component: LogoPlugin,
  description: "Displays a logo",
  defaultArgs: {
    name: "matching-pairs",
  },
};
