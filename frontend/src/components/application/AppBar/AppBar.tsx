/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { Variant } from "@/types/themeProvider";
import classNames from "classnames";
import { URLS, LOGO_TITLE } from "@/config";
import { Link } from "react-router-dom";
import useBoundStore from "@/util/stores";
import { Logo } from "@/components/svg";
import styles from "./AppBar.module.scss";

interface LogoLinkProps extends HTMLAttributes<HTMLAnchorElement> {}

/**
 * Logo is a Link in case of relative url (/abc),
 * and a-element for absolute urls (https://www.example.com/)
 */
function LogoLink({ children, ...props }: LogoLinkProps) {
  const theme = useBoundStore((state) => state.theme);
  const { alt, title, target, rel } = theme?.logo || {};
  const href = theme?.logo?.href || URLS.AMLHome;

  const sharedProps = {
    alt: alt || LOGO_TITLE,
    title: title || LOGO_TITLE,
    target: target || "_self",
    rel: rel || "noopener noreferrer",
  };

  return href.startsWith("http") ? (
    <a href={href} {...sharedProps} {...props}>
      {children}
    </a>
  ) : (
    <Link to={href} {...sharedProps} {...props}>
      {children}
    </Link>
  );
}

interface AppBarProps extends HTMLAttributes<HTMLDivElement> {
  title?: string;
  variant?: Variant;
}

/**
 * AppBar is a bar on top of the app, with navigation and title
 */
const AppBar = ({ className, title, variant, ...divProps }: AppBarProps) => {
  return (
    <div
      className={classNames(styles.appBar, "navbar", className)}
      {...divProps}
    >
      <LogoLink className={styles.logo}>
        <Logo name="aml" fill="#666" aria-label="logo" />
      </LogoLink>
      {title && (
        <div
          className={classNames(
            styles.title,
            variant && `text-fill-${variant}`
          )}
        >
          {title}
        </div>
      )}
      {/* <span className={styles.actionRight}></span> */}
    </div>
  );
};
export default AppBar;
