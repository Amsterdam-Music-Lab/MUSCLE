/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import {
  Children,
  isValidElement,
  type CSSProperties,
  type HTMLAttributes,
} from "react";
import classNames from "classnames";
import styles from "./Board.module.scss";

interface BoardProps extends HTMLAttributes<HTMLDivElement> {
  /** The number of columns */
  columns: number;
}

/**
 * A playing board that organizes its children in a square grid
 * with a given number of columns.
 */
function Board({ columns = 4, children, className, ...props }: BoardProps) {
  const childrenArray = Children.toArray(children);
  return (
    <div
      className={classNames(
        styles.board,
        "sharp-border bg-inset-lg md-flush",
        className
      )}
      {...props}
    >
      <div
        className="square-grid"
        style={{ "--columns": columns } as CSSProperties}
      >
        {childrenArray.map((child, i) => (
          <div
            key={isValidElement(child) && child.key ? child.key : i}
            className={classNames(styles.slot)}
          >
            {child}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Board;
