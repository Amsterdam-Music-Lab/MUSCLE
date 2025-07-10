/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ReactNode, HTMLAttributes } from "react";
import ReactMarkdown from "react-markdown";
import classNames from "classnames";
import styles from "./List.module.scss";

export type BaseListItem = {
  label?: ReactNode;
  content?: ReactNode;
};

interface ListItemProps extends BaseListItem, HTMLAttributes<HTMLLIElement> {
  /** Whether to animate the list items */
  animate?: boolean;

  /** Delay in ms for moving in this list item */
  delay?: number;
}

/**
 * A list component that supports Markdown content and can render
 * the items one-by-one, if desired.
 */
export default function ListItem({
  label,
  content,
  animate = true,
  delay = 0,
  style,
  className,
  ...liProps
}: ListItemProps) {
  return (
    <li
      className={classNames(
        animate && "anim anim-fade-in-slide-left anim-speed-300",
        className
      )}
      style={{ animationDelay: delay + "ms", ...style }}
      {...liProps}
    >
      {label !== undefined && <span className={styles.label}>{label}</span>}
      <span>
        <ReactMarkdown children={content} />
      </span>
    </li>
  );
}
