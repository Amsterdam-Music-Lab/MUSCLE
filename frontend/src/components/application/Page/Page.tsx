/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import useBoundStore from "@/util/stores";
import { useTheme } from "@/theme/ThemeProvider";
import { GradientCircles } from "@/components/svg";
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

  /**
   * Show the gradient circles background. If not set, the settings in the
   * frontend theme are used; otherwise defaults to true.
   */
  showGradientCircles?: boolean;

  /**
   * Show the background image if there is one? If not set, the settings
   * in the frontend are used, and otherwise defaults to true.
   */
  showBackgroundImage?: boolean;

  /**
   * Use the backend theme? Defaults to true.
   *
   * This option is mostly there so that you can also render 'static' pages that do
   * not require a state, for example as a landing page.
   */
  useBackendTheme?: boolean;
}

/**
 * Page with a background, that can be either an image or a gradient circles fill.
 * The component defaults to a gradient circles fill, unless a background image is
 * set by specifying backgroundUrl.
 */
export default function Page({
  title,
  children,
  className,
  backgroundUrl,
  showAppBar,
  useBackendTheme = true,
  showGradientCircles,
  showBackgroundImage,
  ...divProps
}: PageProps) {
  const { theme: frontendTheme } = useTheme();

  // Settings that default to the value in frontendTheme.
  showAppBar =
    showAppBar !== undefined ? showAppBar : frontendTheme.showAppBar ?? true;
  showGradientCircles =
    showGradientCircles !== undefined
      ? showGradientCircles
      : frontendTheme.showGradientCircles ?? true;
  showBackgroundImage =
    showBackgroundImage !== undefined
      ? showBackgroundImage
      : frontendTheme.showBackgroundImage ?? true;

  let backendTheme;
  backendTheme = useBoundStore((state) => state.theme);
  if (useBackendTheme) {
    backgroundUrl = backendTheme?.backgroundUrl ?? backgroundUrl;
  }

  return (
    <>
      {/* Main page content */}
      <div className={classNames(styles.page, className)} {...divProps}>
        {showAppBar && <AppBar title={title ?? ""} />}
        {children}
      </div>

      {/* Background div */}
      {(showGradientCircles || (showBackgroundImage && backgroundUrl)) && (
        <div className={styles.bg}>
          {showBackgroundImage && backgroundUrl && (
            <div
              className={styles.bgImg}
              data-testid="background-image"
              style={{
                backgroundImage: `url(${backgroundUrl})`,
              }}
            />
          )}
          {showGradientCircles && <GradientCircles blur={50} animate={true} />}
        </div>
      )}
    </>
  );
}
