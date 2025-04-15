/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, CSSProperties } from "react";
import type { Variant } from "@/theme/themes";
import classNames from "classnames";
import "./ScoreDisplay.scss";

interface ScoreProps extends HTMLAttributes<HTMLDivElement> {
  /** The score */
  score?: number;

  /** A descriptive label shown underneath the score */
  label?: string;

  /** The unit shown as a superscript. Default "pts". */
  units?: string;

  /** A placeholder shown when no score is specified. Default "??" */
  placeholder?: string;

  /** The size of the score in rems. Default 4 */
  size?: number;

  /** The variant color */
  variant?: Variant;
}

/**
 * A large score with optional units as superscript and an optional label below.
 * When no score is passed, a placeholder text (default "??") is shown.
 */
export default function ScoreDisplay({
  score,
  label,
  units = "pts",
  size = 4,
  placeholder = "??",
  variant = "primary",
  ...props
}: ScoreProps) {
  const { className, style, ...rest } = props;
  return (
    <div
      className={classNames("score-display", className)}
      style={{ "--score-display-font-size": size, ...style } as CSSProperties}
      {...rest}
    >
      <div className="score">
        <div
          className={`value ${
            score !== undefined ? `text-fill-${variant}` : "text-light-gray"
          }`}
        >
          {score === undefined ? placeholder : score}
        </div>
        {units && score !== undefined ? (
          <span className={`text-fill-${variant} units small`}>{units}</span>
        ) : null}
      </div>
      {label && <div className="label text-muted small">{label}</div>}
    </div>
  );
}
