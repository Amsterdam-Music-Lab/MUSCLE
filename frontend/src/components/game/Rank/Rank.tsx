/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import type { ScoreCounterProps } from "../ScoreCounter";
import type { CupProps } from "../Cup";

import classNames from "classnames";
import { ScoreCounter } from "../ScoreCounter";
import { Cup } from "../Cup";
import styles from "./Rank.module.scss";

interface RankProps extends HTMLAttributes<HTMLDivElement> {
  cup: CupProps;
  score: ScoreCounterProps;
}

/**
 * Rank shows a decorated representation of a rank
 */
export default function Rank({
  cup,
  score,
  className,
  ...divProps
}: RankProps) {
  return (
    <div
      data-testid="rank"
      className={classNames(styles.rank, className)}
      {...divProps}
    >
      <Cup className={cup.className} text={cup.text} />
      <h4>
        <ScoreCounter score={score.score} label={score.label} />
      </h4>
    </div>
  );
}
