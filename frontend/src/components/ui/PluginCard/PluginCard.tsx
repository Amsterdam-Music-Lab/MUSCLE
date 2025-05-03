/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";
import type { CardProps, CardSectionProps } from "../Card";
import { Card } from "../Card";
import classNames from "classnames";

export interface CardPlugin extends CardSectionProps {
  /**
   * Name of the component. Should correspond to a component
   * in the components map.
   */
  name?: string;

  /** Arguments of the plugin. */
  args?: any;

  /**
   * Optional function that returns the props passed to Card.Section.
   * This can be used to e.g. set the title etc.
   */
  propsFn?: (args: any) => Partial<CardSectionProps>;
}

export interface PluginCardProps extends CardProps {
  plugins: CardPlugin[];
  components: Record<string, any>;
}

/**
 * A card whose content can be specified using a plugin system. You pass it an
 * array of plugins, and an object mapping component names to components.
 *
 * A plugin is specified using an object of the form
 *    { name: "componentName", args: { ... myComponentArgs }, propsFn, ...sectionProps}.
 */
function PluginCard({
  plugins = [],
  components,
  children,
  ...cardProps
}: PluginCardProps) {
  return (
    <Card {...cardProps}>
      {plugins.map(({ name, propsFn, args, ...props }, index) => {
        const Component = components[name];
        if (typeof propsFn === "function") {
          props = { ...props, ...propsFn(args) };
        }

        return (
          <Card.Section key={index} {...props}>
            <Component {...args} />
          </Card.Section>
        );
      })}
      {children}
    </Card>
  );
}

export default PluginCard;
