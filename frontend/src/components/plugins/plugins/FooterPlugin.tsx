/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { LogoName } from "@/components/svg/Logo/Logo";

import ReactMarkdown from "react-markdown";
import { Logos } from "@/components/svg";

export interface FooterPluginArgs {
  /** A list of logo names */
  logos?: LogoName[];

  /** Markdown disclaimer string */
  disclaimer?: string;
}

export interface FooterPluginMeta extends PluginMeta<FooterPluginArgs> {
  name: "footer";
}

export interface FooterPluginSpec extends PluginSpec<FooterPluginArgs> {
  name: "footer";
}

/**
 * A footer plugin that displays some logo's and a disclaimer text.
 */
function FooterPlugin({ logos = [], disclaimer }: FooterPluginArgs) {
  return (
    <div style={{ marginTop: "1rem", padding: "1rem" }}>
      {logos.length > 0 && <Logos logos={logos} />}
      {disclaimer && (
        <div className="small" style={{ color: "#fff", marginTop: "1em" }}>
          <ReactMarkdown>{disclaimer}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export const footerPlugin: FooterPluginMeta = {
  name: "footer",
  component: FooterPlugin,
  description: "Displays a footer",
  defaultArgs: {},
};
