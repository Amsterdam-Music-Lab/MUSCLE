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

export interface LogoPluginArgs extends LogoProps {}

export interface LogoPluginMeta extends PluginMeta<LogoPluginArgs> {
  name: "logo";
}

export interface LogoPluginSpec extends PluginSpec<LogoPluginArgs> {
  name: "logo";
}

export const logoPlugin: LogoPluginMeta = {
  name: "logo",
  component: Logo,
  description: "Displays a logo",
  defaultArgs: {
    name: "matching-pairs",
  },
};
