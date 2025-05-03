/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { CardProps, CardSectionProps } from "../Card";
import { Card } from "../Card";

export interface PluginSpec extends CardSectionProps {
  /**
   * Name of the component. Should correspond to a component
   * in the components map.
   */
  name: string;

  /** Arguments of the plugin. */
  args?: any;

  /**
   * Optional function that returns the props passed to Card.Section.
   * This can be used to e.g. set the title etc.
   */
  getProps?: (args: any) => Partial<CardSectionProps>;

  /** Order plugins using this argument */
  order?: number;

  /** A function to determine whether the plugin is visible  */
  isVisible?: (args: any) => boolean;

  /** Whether to hide the plugin. */
  hide?: boolean;
}

export interface PluginCardProps extends CardProps {
  /**
   * An array of plugins
   */
  plugins?: PluginSpec[];
  components?: Record<string, any>;
}

/**
 * A card whose content can be specified using a plugin system. You pass it an
 * array of plugins, and an object mapping component names to components.
 *
 * A plugin is specified using an object of the form
 *    { name: "componentName", args: { ... myComponentArgs }, getProps, ...sectionProps}.
 */
function PluginCard({
  plugins = [],
  components = {},
  children,
  ...cardProps
}: PluginCardProps) {
  // Order plugins. Ordered plugins appear before non-ordered ones
  plugins = plugins.sort(
    (a, b) =>
      (a.order === undefined ? Infinity : a.order) -
      (b.order === undefined ? Infinity : b.order)
  );

  return (
    <Card {...cardProps}>
      {plugins.map(
        ({ name, getProps, args, isVisible, hide, ...props }, index) => {
          // Check if the plugin should be shown at all
          if (hide === true) {
            return null;
          } else if (typeof isVisible === "function" && !isVisible(args)) {
            return null;
          }

          // Check if it can be shown
          if (!name) {
            console.warn(`Cannot render plugin ${index}: nas no name`);
            return null;
          }
          if (!components[name]) {
            console.warn(`Component "${name}" not found.`);
            return null;
          }

          const Component = components[name];
          if (typeof getProps === "function") {
            props = { ...props, ...getProps(args) };
          }

          return (
            <Card.Section key={index} {...props}>
              <Component {...args} />
            </Card.Section>
          );
        }
      )}
      {children}
    </Card>
  );
}

export default PluginCard;
