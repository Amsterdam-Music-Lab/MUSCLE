import type { AnchorHTMLAttributes, ElementType, ReactNode } from "react";
import type { LinkProps } from "react-router-dom";
import type { Variant } from "@/theme/themes";
import type { ButtonProps, GetButtonClassesProps } from "../Button/Button";

import classNames from "classnames";
import { Link } from "react-router-dom";
import Button, { getButtonClasses } from "../Button/Button";
import "./LinkButton.module.scss";
import styles from "./LinkButton.module.scss";
import buttonStyles from "../Button/Button.module.scss";

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

type LinkButtonProps<T extends ElementType> = BaseProps & ElementProps<T>;

/**
 * Test whether an url is relative
 */
const isRelativeUrl = (url: string): boolean => {
  return url ? url.startsWith("/") : false;
};

function LinkButton<T extends ElementType = "button">({
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
      rounded
    },
    className
  );

  props = {
    "data-testid": "button-link",
    variant,
    children,
    ...props,
  };

  let Component;
  if (!link) {
    Component = Button;
    props = { className, ...props };
  } else if (isRelativeUrl(link)) {
    Component = "Link";
    props = { to: `/redirect${link}`, className: classes, ...props };
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

export default LinkButton;
