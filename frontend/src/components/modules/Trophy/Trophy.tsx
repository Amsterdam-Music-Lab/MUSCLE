/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes, ReactNode, ComponentProps } from "react";
import type { SVGSymbolName, SVGSymbolProps } from "@/types/svg";

import { useState, lazy, Suspense } from "react";
import classNames from "classnames";
import { useTheme } from "@/theme/ThemeProvider";
import { symbols as svgSymbols } from "@/components/svg";
import styles from "./Trophy.module.scss";

const ConfettiExplosion = lazy(() => import("react-confetti-explosion"));

export interface TrophyProps extends HTMLAttributes<HTMLDivElement> {
  /** Name of the svg icon */
  iconName: SVGSymbolName;

  /** Optional header text node */
  header?: ReactNode;

  /** Optional body text node */
  body?: ReactNode;

  /** Optional properties passed to the icon */
  iconProps?: SVGSymbolProps;

  /** Whether to show the confetti */
  showConfetti?: boolean;

  /** Optional properties passed to the ConfettiExplosion */
  confettiProps?: Partial<ComponentProps<typeof ConfettiExplosion>>;

  /* Whether to wobble trophy (slowly rotate back and forth). Default true. */
  wobble?: boolean;

  /**
   * The maximum angle of the wobble in degrees. Determines how strongly
   * the trophy wobbles. Default 6 degrees.
   */
  wobbleAngle?: number;

  /** The duration of the wobble in ms. Default 4000ms */
  wobbleDuration?: number;
}

/**
 * A trophy icon with confetti and a message next to it it.
 * The icon should currently be an SVG icon and so is specified by
 * the icon name (e.g. `"star-6"`). The icon is animated (rotates)
 * and the whole trophy wobbles. Both animations can be turned off.
 * Confetti can also be turned off using `showConfett=false`.
 */
export default function Trophy({
  iconName,
  header,
  body,
  className,
  iconProps = {},
  showConfetti = true,
  confettiProps = {},
  wobble = true,
  wobbleAngle = 6,
  wobbleDuration = 4000,
  style = {},
  ...divProps
}: TrophyProps) {
  const [exploding, setExploding] = useState(true);
  const { theme } = useTheme();

  if (!svgSymbols[iconName]) {
    console.warn(`Trophy icon "${iconName}" not found. Using default "star"`);
    iconName = "star";
  }
  const Trophy = svgSymbols[iconName];
  const { className: iconClassName, ...otherIconProps } = iconProps;
  return (
    <div
      className={classNames(styles.trophy, wobble && styles.wobble, className)}
      style={{
        "--wobble-angle": `${wobbleAngle}deg`,
        "--wobble-duration": `${wobbleDuration}ms`,
        ...style,
      }}
      {...divProps}
    >
      <div className={styles.trophyIcon}>
        {showConfetti && exploding && (
          <Suspense>
            <ConfettiExplosion
              data-testid="confetti-explosion"
              force={2}
              duration={6000}
              particleCount={250}
              width={2000}
              colors={[
                theme?.primary?.startColor,
                theme?.primary?.endColor,
                theme?.secondary?.startColor,
                theme?.secondary?.endColor,
              ].filter((c) => c)}
              {...confettiProps}
              onComplete={() => {
                setExploding(false);
                if (confettiProps?.onComplete) confettiProps.onComplete();
              }}
            />
          </Suspense>
        )}
        <Trophy
          size={100}
          variant="secondary"
          className={classNames(styles.trophyIcon, iconClassName)}
          {...otherIconProps}
        />
      </div>
      {(header || body) && (
        <div className={styles.trophyText}>
          {header && <h3>{header}</h3>}
          {body && <p>{body}</p>}
        </div>
      )}
    </div>
  );
}
