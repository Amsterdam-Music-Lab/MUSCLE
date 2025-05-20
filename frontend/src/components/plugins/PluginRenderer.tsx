/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginSpec } from "@/types/plugin";
import type { ReactNode, ComponentType } from "react";
import { Fragment, createElement } from "react";
import { pluginMetaRegistry } from "./pluginRegistry";
import type { AllPluginSpec, PluginRegistry } from "./pluginRegistry";

interface PluginRendererProps {
  plugins: AllPluginSpec[];

  registry?: PluginRegistry;

  /** Optional wrapper to surround each plugin */
  wrapper?: ComponentType;

  /** Optional slot renderer function */
  renderSlot?: (slotName: string, children: ReactNode) => ReactNode;
}

export function PluginRenderer({
  plugins,
  registry = pluginMetaRegistry,
  wrapper,
  renderSlot,
}: PluginRendererProps) {
  // Update plugin args and specs with default arguments
  plugins = plugins
    .filter((p) => p)
    .map((plugin) => {
      const meta = registry[plugin.name as keyof PluginRegistry];
      if (!meta) {
        console.warn(`Plugin component not found: ${plugin.name}`);
        return null;
      }
      const updated = { ...meta.defaultSpecs, ...plugin };
      updated.args = { ...meta.defaultArgs, ...plugin.args };
      return updated;
    })
    .filter((p) => p) as AllPluginSpec[];

  // Filter out disabled and invisible plugins, group by slot
  const grouped = plugins
    .filter((p) => p.enabled !== false)
    .filter((p) =>
      typeof p.isVisible === "function" ? p.isVisible(p.args) : true
    )
    .reduce<Record<string, PluginSpec[]>>((acc, plugin) => {
      const slot = plugin.slot ?? "__default";
      acc[slot] = acc[slot] || [];
      acc[slot].push(plugin);
      return acc;
    }, {});

  return (
    <>
      {Object.entries(grouped).map(([slot, slotPlugins]) => {
        const sorted = slotPlugins.sort(
          (a, b) => (a.order ?? Infinity) - (b.order ?? Infinity)
        );

        const children = sorted.map((plugin, index) => {
          const meta = registry[plugin.name as keyof PluginRegistry];
          const Component = meta.component;
          const wrapperProps = plugin.getWrapperProps?.(plugin.args) ?? {};

          return wrapper
            ? createElement(
                wrapper,
                {
                  key: `${slot}-${index}`,
                  ...plugin.wrapperProps,
                  ...wrapperProps,
                },
                createElement(Component, { ...plugin.args })
              )
            : createElement(Component, {
                key: `${slot}-${index}`,
                ...plugin.args,
              });
        });

        return renderSlot ? (
          renderSlot(slot, children)
        ) : (
          <Fragment key={slot}>{children}</Fragment>
        );
      })}
    </>
  );
}

export default PluginRenderer;
