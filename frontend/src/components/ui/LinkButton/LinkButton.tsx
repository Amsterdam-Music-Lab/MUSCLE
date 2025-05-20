/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { AnchorHTMLAttributes, ElementType, ReactNode } from "react";
import type { LinkProps } from "react-router-dom";
import type { ButtonProps, GetButtonClassesProps } from "../Button/Button";
import { Link } from "react-router-dom";
import classNames from "classnames";
import Button, { getButtonClasses } from "../Button/Button";
import "./LinkButton.module.scss";
import styles from "./LinkButton.module.scss";

type ElementProps<T extends ElementType> = T extends "a"
  ? AnchorHTMLAttributes<HTMLAnchorElement>
  : T extends typeof Button
  ? ButtonProps
  : T extends typeof Link
  ? LinkProps
  : Record<string, unknown>;

interface BaseProps extends GetButtonClassesProps {
  link?: string;
  children?: ReactNode;
  className?: string;
}

export type LinkButtonProps<T extends ElementType> = BaseProps &
  ElementProps<T>;

/**
 * Test whether an url is relative
 */
export const isRelativeUrl = (url: string): boolean => {
  return url ? url.startsWith("/") : false;
};

export default function LinkButton<T extends ElementType = "button">({
  link,
  className,
  children,
  variant,
  size,
  outline,
  stretch,
  rounded,
  ...props
}: LinkButtonProps<T>) {
  const classes = getButtonClasses(
    {
      variant,
      size,
      outline,
      stretch,
      rounded,
    },
    className
  );

  props = {
    "data-testid": "button-link",
    children,
    ...props,
  };

  let Component;
  if (!link) {
    Component = Button;
    props = { className, variant, size, outline, rounded, stretch, ...props };
  } else if (isRelativeUrl(link)) {
    Component = Link;
    props = {
      to: `/redirect${link}`,
      className: classNames(styles.anchorButton, classes),
      ...props,
    };
  } else {
    Component = "a";
    props = {
      href: link,
      target: "_blank",
      rel: "noopener noreferrer",
      className: classNames(classes, styles.anchorButton),
      ...props,
    };
  }
  return <Component {...(props as any)} />;
}
