/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { LogoName } from "@/components/svg/Logo/Logo";
import Logo from "@/components/svg/Logo/Logo";

export interface FooterPluginArgs {
  logos?: LogoName[];
  disclaimer?: string;
}

export interface FooterPluginMeta extends PluginMeta<FooterPluginArgs> {
  name: "footer";
}

export interface FooterPluginSpec extends PluginSpec<FooterPluginArgs> {
  name: "footer";
}

function FooterPlugin({ logos = [], disclaimer }: FooterPluginArgs) {
  return (
    <div style={{ marginTop: "1rem", padding: "1rem", opacity: 0.5 }}>
      {logos.length > 0 && (
        <div style={{ display: "flex", gap: "2em" }}>
          {logos.map((name) => (
            <Logo
              name={name}
              fill="#fff"
              style={{ height: name == "nwo" ? "2.5em" : "1.5em" }}
              key={name}
            />
          ))}
        </div>
      )}
      {disclaimer && (
        <p className="small" style={{ color: "#fff", marginTop: "1em" }}>
          {disclaimer}
        </p>
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
