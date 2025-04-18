/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ButtonHTMLAttributes, MouseEvent } from "react";
import type { GetButtonClassesProps } from "../Button/Button";

import { useState, useRef, useEffect } from "react";
import classNames from "classnames";
import { Button } from "../Button";
import styles from "./ExpandableButton.module.scss";

interface ExpandableButtonProps
  extends GetButtonClassesProps,
    HTMLAttributes<HTMLDivElement> {
  expanded?: boolean;
  disabled?: boolean;
  buttonProps?: Partial<
    Omit<ButtonHTMLAttributes<HTMLButtonElement>, "disabled">
  >;
}

export default function ExpandableButton({
  title,
  children,
  className,
  expanded = false,
  rounded = false,
  size,
  variant,
  outline,
  disabled = false,
  buttonProps = {},

  ...divProps
}: ExpandableButtonProps) {
  const [expand, setExpand] = useState(expanded);
  const ref = useRef<HTMLDivElement>(null);

  // Collapse when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: globalThis.MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node) && !disabled) {
        setExpand(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
    setExpand((prev) => !prev);
    if (buttonProps.onClick) buttonProps.onClick(e);
  };

  return (
    <div
      ref={ref}
      className={classNames(styles.expandableButton, className)}
      data-expanded={expand}
      {...divProps}
    >
      <Button
        variant={variant}
        size={size}
        outline={outline}
        stretch={false}
        allowMultipleClicks={true}
        rounded={rounded}
        disabled={disabled}
        onClick={handleClick}
        {...buttonProps}
      >
        {title}
      </Button>
      <div className={classNames(styles.content, rounded && styles.rounded)}>
        <div className={styles.innerContent}>{children}</div>
      </div>
    </div>
  );
}
