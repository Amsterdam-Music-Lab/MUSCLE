import { type ButtonHTMLAttributes, type TouchEvent, useRef } from "react";
import classNames from "classnames";
import { audioInitialized } from "@/util/audio";
import styles from "./Button.module.scss";
import { Variant } from "@/theme/themes";

export interface ButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick" | "value"> {
  value: string | boolean;
  onClick: (value?: string | boolean) => void;
  clickOnce?: boolean;
  variant: Variant;
}

// Button is a button that can only be clicked one time by default
const Button = ({
  title,
  children,
  onClick,
  className,
  disabled = false,
  value,
  variant = "primary",
  clickOnce = true,
  ...btnProps
}: ButtonProps) => {
  const clicked = useRef(false);

  // Only handle the first click
  const clickOnceGuard = () => {
    if (!clickOnce) {
      return onClick(value);
    }

    if (disabled || clicked.current) {
      return;
    }
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
      className={classNames(
        `fill-${variant}`,
        "hover-lighter",
        styles.button,
        className
      )}
      onClick={clickOnceGuard}
      disabled={disabled}
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
