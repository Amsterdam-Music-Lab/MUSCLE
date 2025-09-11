/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { MouseEvent } from "react";
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { BaseButtonProps } from "@/components/buttons";
import { LinkButton } from "@/components/buttons";

export interface LinkButtonPluginArgs extends BaseButtonProps {
  link?: string;
  onClick?: (e: MouseEvent) => void;
}

export interface LinkButtonPluginMeta extends PluginMeta<LinkButtonPluginArgs> {
  name: "linkButton";
}

export interface LinkButtonPluginSpec extends PluginSpec<LinkButtonPluginArgs> {
  name: "linkButton";
}

export const linkButtonPlugin: LinkButtonPluginMeta = {
  name: "linkButton",
  component: LinkButton,
  description: "Displays a link",
  defaultArgs: {
    variant: "secondary",
    size: "lg",
    rounded: false,
  },
};
