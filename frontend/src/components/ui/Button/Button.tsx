import { type ButtonHTMLAttributes, type TouchEvent, useRef } from "react";
import classNames from "classnames";
import { audioInitialized } from "@/util/audio";
import styles from "./Button.module.scss";
import { Variant } from "@/theme/themes";

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
  value: string | boolean;
  onClick: (value?: string | boolean) => void;

  /** Whether you can click multiple times. Defaults to false! */
  allowMultipleClicks?: boolean;
}

/**
 * A button that can only be clicked one time by default
 */
const Button = ({
  title,
  children,
  onClick,
  className,
  disabled = false,
  value,
  allowMultipleClicks = false,
  variant = "primary",
  size = "md",
  stretch = false,
  outline = true,
  rounded = true,
  ...btnProps
}: ButtonProps) => {
  const clicked = useRef(false);
  

  // Only handle the first click
  const clickOnceGuard = () => {
    if (allowMultipleClicks) onClick(value);
    if (disabled || clicked.current) return;
    clicked.current = true;
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
        className
      )}
      onClick={clickOnceGuard}
      disabled={disabled || (!allowMultipleClicks && clicked.current)}
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
