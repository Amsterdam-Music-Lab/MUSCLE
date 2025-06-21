/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { type ButtonHTMLAttributes, type TouchEvent } from "react";
import type { Variant } from "@/types/themeProvider";
import { useState, forwardRef } from "react";
import classNames from "classnames";
import { audioInitialized } from "@/util/audio";
import styles from "./Button.module.scss";

export interface BaseButtonProps {
  /** Theme color variant to use */
  variant?: Variant;

  /** Size of the button */
  size?: "sm" | "md" | "lg" | "xl" | "huge";

  /** Whether the button has round caps */
  rounded?: boolean;

  /** Whether to stretch the button to 100% width */
  stretch?: boolean;

  /** Whether to show the soft outline */
  outline?: boolean;

  /** Whether the button is disabled */
  disabled?: boolean;

  /** Whether the button is hovered (adds a css class) */
  hover?: boolean;
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
    hover,
    disabled,
  }: BaseButtonProps,
  ...otherClasses: (string | Record<string, boolean>)[]
) {
  return classNames(
    styles.button,
    stretch && styles.stretch,
    outline && styles.outline,
    rounded && styles.rounded,
    hover && "hover",
    styles[size],
    `fill-${variant}`,
    disabled !== true && "hover-darker",
    ...otherClasses
  );
}

export interface ButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick" | "value">,
    BaseButtonProps {
  value?: string | boolean;

  // TODO is this used?
  onClick?: (value?: string | boolean) => void;

  /** Whether you can click multiple times. Defaults to true. */
  allowMultipleClicks?: boolean;
}

/**
 * A button that can only be clicked one time by default
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  {
    title,
    children,
    type = "button",
    onClick = () => {},
    className,
    disabled: initialDisabled = false,
    value,
    allowMultipleClicks = true,
    variant = "primary",
    size = "md",
    stretch = false,
    outline = true,
    rounded = true,
    hover,
    ...btnProps
  }: ButtonProps,
  ref
) {
  // Only use state to control disabled when allowMultipleClicks === false
  // TODO its a bit strange to have  allowMultipleClicks = true by default

  // Use internal state to avoid a conditional hook
  const [internalDisabled, setInternalDisabled] = useState(initialDisabled);
  const disabled = allowMultipleClicks ? initialDisabled : internalDisabled;

  // Only handle the first click
  const clickOnceGuard = () => {
    if (disabled === true) return;
    if (allowMultipleClicks === false) setInternalDisabled(true);
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
      ref={ref}
      type={type}
      // tabIndex={0}
      onClick={clickOnceGuard}
      onKeyDown={clickOnceGuard}
      className={getButtonClasses(
        {
          variant,
          size,
          outline,
          stretch,
          rounded,
          disabled,
          hover,
        },
        className,

        // Using classes instead of disabled={disabled}
        // to fix some issues when disabled="" appears in html
        disabled === true && styles.disabled
      )}
      {...btnProps}
    >
      {title}
      {children}
    </button>
  );
});

export default Button;
