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
import styles from "./Background.module.scss";

export interface BackgroundProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Url of the background image.
   */
  backgroundUrl?: string;

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
 * Background component that shows either an image or a gradient circles fill.
 * The component defaults to a gradient circles fill, unless a background image is
 * set by specifying backgroundUrl.
 */
export default function Background({
  backgroundUrl,
  useBackendTheme = true,
  showGradientCircles,
  showBackgroundImage,
  children,
  className,
  ...divProps
}: BackgroundProps) {
  const { theme: frontendTheme } = useTheme();

  // Settings that default to the value in frontendTheme.
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
    (showGradientCircles || (showBackgroundImage && backgroundUrl)) && (
      <div className={classNames(styles.bg, className)} {...divProps}>
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
        {children}
      </div>
    )
  );
}
