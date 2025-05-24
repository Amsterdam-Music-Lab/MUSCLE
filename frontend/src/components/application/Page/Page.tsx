/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import { useTheme } from "@/theme/ThemeProvider";
import { AppBar } from "../AppBar";
import styles from "./Page.module.scss";

export interface PageProps extends HTMLAttributes<HTMLDivElement> {
  /** Title of the page */
  title?: string;

  /**
   * Whether to show the app bar. If not set, the settings from the frontend
   * theme are used, and otherwise defaults to true.
   */
  showAppBar?: boolean;

  showBackgroundFill: boolean;
}

/**
 * Page with a background, that can be either an image or a gradient circles fill.
 * The component defaults to a gradient circles fill, unless a background image is
 * set by specifying backgroundUrl.
 */
export default function Page({
  title,
  showAppBar,
  children,
  className,
  showBackgroundFill,
  ...divProps
}: PageProps) {
  const { theme: frontendTheme } = useTheme();

  // Settings that default to the value in frontendTheme.
  showAppBar =
    showAppBar !== undefined ? showAppBar : frontendTheme.showAppBar ?? true;

  return (
    <div
      className={classNames(
        styles.page,
        showBackgroundFill && styles.bgFill,
        className
      )}
      {...divProps}
    >
      {showAppBar && <AppBar title={title ?? ""} />}
      {children}
    </div>
  );
}
