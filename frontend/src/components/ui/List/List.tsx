/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import type { BaseListItem } from "./ListItem";
import classNames from "classnames";
import ListItem from "./ListItem";
import styles from "./List.module.scss";

export interface ListProps extends HTMLAttributes<HTMLUListElement> {
  items: BaseListItem[];

  /**
   * Whether to show an ordered list. This determines which HTML element
   * is used: `ol` when `ordered=true`, and `ul` otherwise.
   */
  ordered?: boolean;

  /**
   * Whether to animate the list items: show them one by one.
   * Default true.
   */
  animate?: boolean;

  /**
   * Delay in ms between the list items. Ignored when `animate=false`;
   * default 250ms.
   */
  delay?: number;
}

/**
 * A list component that supports Markdown content and can render
 * the items one-by-one, if desired. The `items` prop expects a list
 * of objects with a `content` and optional `label` key. If you omit
 * the label, it will default to numbering the items:
 *
 * ```ts
 * const items = [
 *  { label: "A", content: "First item" },
 *  { content: "Second item" }, // Label will be "2"
 *  //...
 * ]
 * ```
 *
 */
export default function List({
  items,
  animate = true,
  ordered = true,
  delay = 250,
  className = undefined,
  ...ulProps
}) {
  const ListEl = ordered ? "ol" : "ul";
  return (
    <ListEl
      className={classNames(styles.list, animate && styles.animate, className)}
      {...ulProps}
    >
      {items.map((item, index) => (
        <ListItem
          key={index}
          label={item.label ?? index + 1}
          content={item.content}
          animate={animate}
          delay={index * delay}
        />
      ))}
    </ListEl>
  );
}
