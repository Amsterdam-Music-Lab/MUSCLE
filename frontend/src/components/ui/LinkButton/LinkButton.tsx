import type { AnchorHTMLAttributes, ElementType, ReactNode } from "react";
import type { LinkProps } from "react-router-dom";
import type { Variant } from "@/theme/themes";
import type { ButtonProps } from "../Button";

import classNames from "classnames";
import { Link } from "react-router-dom";
import { Button } from "../Button";
import "./LinkButton.module.scss";
import buttonStyles from "../Button/Button.module.scss";

type ElementProps<T extends ElementType> = T extends "a"
  ? AnchorHTMLAttributes<HTMLAnchorElement>
  : T extends typeof Button
  ? ButtonProps
  : T extends typeof Link
  ? LinkProps
  : Record<string, unknown>;

type BaseProps = {
  link?: string;
  variant?: Variant;
  // clickOnce?: boolean;
  // title?: string;
  children?: ReactNode;
  className?: string;
};

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
  ...props
}: LinkButtonProps<T>) {
  props = {
    "data-testid": "button-link",
    className: classNames(
      className,
      buttonStyles.button
      // "btn btn-primary btn-lg mcg-btn bg-subtle-yellow-pink"
    ),
    variant,
    children,
    ...props,
  };

  let Component;
  if (!link) {
    Component = Button;
  } else if (isRelativeUrl(link)) {
    Component = "Link";
    props = { to: `/redirect${link}`, ...props };
  } else {
    Component = "a";
    props = {
      href: link,
      target: "_blank",
      rel: "noopener noreferrer",
      ...props,
    };
  }
  return <Component {...(props as any)} />;
}

export default LinkButton;
