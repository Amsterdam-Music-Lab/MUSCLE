import type { ComponentType } from "react";

export type PluginKind = "component" | "content";

export interface PluginSpec<Args = any> {
  /** The name of the plugin, corresponding to a component in the registry */
  name: string;

  /** Static or dynamic arguments passed to the component */
  args: Args;

  /**
   * Dynamically derive props for a wrapper element around the plugin.
   */
  getWrapperProps?: (args: Args) => Record<string, any>;

  /** Default wrapper props */
  wrapperProps?: Record<string, any>;

  /** For positioning within layouts that support named regions */
  slot?: string;

  /** Order within the slot (or in flat layout if no slots) */
  order?: number;

  /** Whether the plugin is enabled at all. */
  enabled?: boolean;

  /**
   * Determines whether the plugin is rendered (e.g. based on args or runtime state).
   * Default: always visible
   */
  isVisible?: (args: Args) => boolean;
}

export interface PluginMeta<Args = any> {
  /** Unique name, used to match PluginSpec.name */
  name: string;

  /** React component to render */
  component: ComponentType<Args>;

  /** Optional default args used when PluginSpec.args is missing */
  defaultArgs?: Partial<Args>;

  defaultSpecs?: Partial<PluginSpec<Args>>;

  /** Developer- or UI-facing description of the plugin */
  description?: string;

  /** Kind/category of plugin for filtering, UI, etc. */
  kind?: PluginKind;
}
