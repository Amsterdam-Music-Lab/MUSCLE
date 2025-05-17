/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import "./Cup.scss";

export interface CupProps extends HTMLAttributes<HTMLDivElement> {
  className:
    | string
    | "diamond"
    | "platinum"
    | "gold"
    | "silver"
    | "bronze"
    | "plastic";
  text: string;
}

export default function Cup({ className, text, ...divProps }: CupProps) {
  return (
    <div
      className={classNames("aha__cup", className, {
        offsetCup: text,
      })}
      data-testid="cup"
      {...divProps}
    >
      <div className="cup" data-testid="cup-animation" />
      <h4 data-testid="cup-text">{text}</h4>
    </div>
  );
}
