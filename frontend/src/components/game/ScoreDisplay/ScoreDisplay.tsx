/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react"
import classNames from "classnames";
import "./ScoreDisplay.scss"

interface ScoreProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The score */
  score?: number;

  /** A descriptive label shown underneath the score */
  label?: string;

  /** The unit shown as a superscript. Default "pts". */
  units?: string;

  /** A placeholder shown when no score is specified. Default "??" */
  placeholder?: string;

  /** The size of the score in rems. Default 4 */
  size: number;
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
  placeholder="??",
  ...props
}: ScoreProps) {
  const { className, style, ...rest } = props;
  return (
    <div 
      className={classNames("score-display", className)} 
      style={{"--score-display-font-size": size, ...style }} 
      {...rest}
    >
      <div className="score">
        <div className={`value ${score ? 'text-subtle-yellow-pink' : 'text-light-gray'}`}>{score || placeholder}</div>
        {(units && score) && <span className="units small text-subtle-yellow-pink">{units}</span>}
      </div>
      {label && <div className="label text-muted small">{label}</div>}
    </div>
  )
}
