/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { type ButtonHTMLAttributes, type TouchEvent } from "react";
import type { Variant } from "@/types/themeProvider";
import { useState } from "react";
import classNames from "classnames";
import { audioInitialized } from "@/util/audio";
import styles from "./Button.module.scss";

export interface GetButtonClassesProps {
  /** Theme color variant to use */
  variant?: Variant;

  /** Size of the button */
  size?: "sm" | "md" | "lg";

  /** Whether the button has round caps */
  rounded?: boolean;

  /** Whether to stretch the button to 100% width */
  stretch?: boolean;

  /** Whether to show the soft outline */
  outline?: boolean;
}

/**
 * Utility that returns the right classes based on the button parameters:
 * the variant, size, stretch and outline.
 */
export function getButtonClasses(
  {
    variant = "primary",
    size = "md",
    rounded = true,
    stretch = false,
    outline = true,
  }: GetButtonClassesProps,
  ...otherClasses
) {
  return classNames(
    styles.button,
    stretch && styles.stretch,
    outline && styles.outline,
    rounded && styles.rounded,
    {
      [styles.sm]: size === "sm",
      [styles.md]: size === "md",
      [styles.lg]: size === "lg",
    },
    `fill-${variant}`,
    "hover-darker",
    ...otherClasses
  );
}

export interface ButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick" | "value">,
    GetButtonClassesProps {
  value?: string | boolean;

  // TODO is this used?
  onClick?: (value?: string | boolean) => void;

  /** Whether you can click multiple times. Defaults to false! */
  allowMultipleClicks?: boolean;
}

/**
 * A button that can only be clicked one time by default
 */
const Button = ({
  title,
  children,
  onClick = () => {},
  className,
  disabled: initialDisabled = false,
  value,
  allowMultipleClicks = false,
  variant = "primary",
  size = "md",
  stretch = false,
  outline = true,
  rounded = true,
  ...btnProps
}: ButtonProps) => {
  const [disabled, setDisabled] = useState(initialDisabled);
  // const clicked = useRef(false);

  // Only handle the first click
  const clickOnceGuard = () => {
    if (disabled === true) return;
    if (allowMultipleClicks === false) setDisabled(true);
    onClick(value);
  };

  // Only support touch events as the audio is initialized
  // Otherwise iOS-Safari users can start the player (by a touchstart)
  // Without the browser having registered any user interaction (e.g. click)
  if (audioInitialized) {
    btnProps.onTouchStart = (e: TouchEvent) => {
      e.stopPropagation();
      clickOnceGuard();
      return false;
    };
  }

  return (
    <button
      className={getButtonClasses(
        {
          variant,
          size,
          outline,
          stretch,
          rounded,
        },
        className,

        // Using classes instead of disabled={disabled}
        // to fix some issues when disabled="" appears in html
        disabled === true && styles.disabled
      )}
      onClick={clickOnceGuard}
      tabIndex={0}
      onKeyDown={clickOnceGuard}
      type="button"
      {...btnProps}
    >
      {title}
      {children}
    </button>
  );
};

export default Button;
