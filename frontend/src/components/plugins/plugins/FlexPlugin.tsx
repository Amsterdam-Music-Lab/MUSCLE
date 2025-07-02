/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { CSSProperties } from "react";
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import PluginRenderer, { PluginRendererProps } from "../PluginRenderer";
import { AllPluginSpec } from "../pluginRegistry";

type Optional<T> = {
  [K in keyof T]?: T[K];
};

export interface FlexPluginArgs
  extends Optional<Pick<CSSProperties, "gap" | "flexDirection">>,
    PluginRendererProps {
  plugins: AllPluginSpec[];
  style?: CSSProperties;
}

function FlexPlugin({
  plugins,
  gap = "1em",
  flexDirection = "row",
  style = {},
  ...pluginRendererProps
}: FlexPluginArgs) {
  return (
    <div
      style={{
        display: "flex",
        gap,
        flexDirection,
        ...style,
      }}
    >
      <PluginRenderer plugins={plugins} {...pluginRendererProps} />
    </div>
  );
}

export interface FlexPluginMeta extends PluginMeta<FlexPluginArgs> {
  name: "flex";
}

export interface FlexPluginSpec extends PluginSpec<FlexPluginArgs> {
  name: "flex";
}

export const flexPlugin: FlexPluginMeta = {
  name: "flex",
  component: FlexPlugin,
  description: "Displays a flex container with plugins",
};
