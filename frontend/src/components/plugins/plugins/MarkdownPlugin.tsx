/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import { lazy, Suspense } from "react";
const ReactMarkdown = lazy(() => import("react-markdown"));

export interface MarkdownPluginArgs {}

export function Markdown({ content }) {
  return (
    <Suspense fallback={<span className="transition-appear">Loading...</span>}>
      <ReactMarkdown children={content} />
    </Suspense>
  );
}

export interface MarkdownPluginMeta extends PluginMeta<MarkdownPluginArgs> {
  name: "markdown";
}

export interface MarkdownPluginSpec extends PluginSpec<MarkdownPluginArgs> {
  name: "markdown";
}

export const markdownPlugin: MarkdownPluginMeta = {
  name: "markdown",
  component: Markdown,
  description: "Renders markdown content",
};
