/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import {
  isValidElement,
  type CSSProperties,
  type HTMLAttributes,
  type ReactNode,
} from "react";
import classNames from "classnames";
import styles from "./Board.module.scss";

export interface SlotProps extends HTMLAttributes<HTMLDivElement> {
  /** If true, no styling will be applied to the slot */
  invisible?: boolean;
}

interface BoardProps extends Omit<HTMLAttributes<HTMLDivElement>, "children"> {
  /** The number of columns */
  columns: number;

  /**
   * Children can be either dom nodes, or tuples of the form [node, slotProps]
   * where slotProps will be passed to the parent slot.
   */
  children?: ReactNode | [ReactNode, SlotProps] | [ReactNode, SlotProps][];

  /**
   * Instead of passing the [node, slotProps] array as children, you can also
   * pass them to `items` directly. This is mostly meant to work around a problem
   * with Storybook which doesn't accept objects as children.
   */
  items?: [ReactNode, SlotProps][];
}

/**
 * A playing board that organizes its children in a square grid with a given
 * number of columns. Every child is placed in a container div, the slot.
 * You can either pass children as React nodes, or as tuples `[node, slotProps]`
 * where `slotProps` will be passed to the slot divs. This allows you to style the
 * slots, for example.
 */
function Board({
  columns = 4,
  children,
  items,
  className,
  ...props
}: BoardProps) {
  // Construct an array of [child, slotProps] tuples.
  let itemsArray: Array<[ReactNode, SlotProps]> = [];
  if (items !== undefined) {
    itemsArray = items;
  } else if (children !== undefined) {
    const rawChildren = Array.isArray(children) ? children : [children];
    itemsArray = rawChildren.map((child) =>
      Array.isArray(child) ? child : [child, {}]
    ) as [ReactNode, SlotProps][];
  }

  return (
    <div
      className={classNames(
        styles.board,
        "sharp-border bg-inset-lg",
        className
      )}
      {...props}
    >
      <div
        className={classNames(styles.squareGrid, "square-grid")}
        style={{ "--columns": columns } as CSSProperties}
      >
        {itemsArray.map(([child, slotProps], i) => {
          const { className: slotClassName, invisible, ...rest } = slotProps;
          return (
            <div
              key={isValidElement(child) && child.key ? child.key : i}
              className={classNames(
                styles.slot,
                invisible && styles.invisible,
                slotClassName
              )}
              {...rest}
            >
              {child}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Board;
