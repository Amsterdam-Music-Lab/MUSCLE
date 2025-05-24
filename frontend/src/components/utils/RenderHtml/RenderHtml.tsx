/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./RenderHtml.module.scss";

export interface RenderHtmlProps extends HTMLAttributes<HTMLDivElement> {
  html: string | TrustedHTML;
  innerClassName?: string;
}

/** HTML is an block view, that shows custom HTML and a Form */
export default function RenderHtml({
  html = "",
  className,
  innerClassName = "",
  ...divProps
}: RenderHtmlProps) {
  return (
    <div
      className={classNames(styles.htmlContainer, "html", className)}
      {...divProps}
    >
      <div
        className={classNames(styles.htmlContent, innerClassName)}
        data-testid="html-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
}
