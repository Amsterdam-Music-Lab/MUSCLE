/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import { Card, CardProps } from "@/components/ui";
import PluginRenderer from "../PluginRenderer";
import { AllPluginSpec } from "../pluginRegistry";

export interface CardPluginArgs extends CardProps {
  plugins: AllPluginSpec[];
}
function CardPlugin({ plugins, ...cardProps }: CardPluginArgs) {
  return (
    <Card {...cardProps}>
      <PluginRenderer plugins={plugins} wrapper={Card.Section} />
    </Card>
  );
}

export interface CardPluginMeta extends PluginMeta<CardPluginArgs> {
  name: "card";
}

export interface CardPluginSpec extends PluginSpec<CardPluginArgs> {
  name: "card";
}

export const cardPlugin: CardPluginMeta = {
  name: "card",
  component: CardPlugin,
  description: "Displays a card with plugins",
  defaultArgs: {
    name: "matching-pairs",
  },
};
