/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import classNames from "classnames";
import Histogram, { HistogramProps } from "@/components/Histogram/Histogram";
import Card, { type CardProps } from "../Card/Card";
import styles from "./AudioCard.module.scss"

interface AudioCardProps extends CardProps, Omit<HistogramProps, "variant"> {};

export default function AudioCard({ 
  running=true, 
  bars=6, 
  random=true, 
  interval=300, 
  className,
  variantFront='primary',
  ...cardProps 
}: AudioCardProps) {
  return (
    <Card className={classNames(styles.audio, className)} {...cardProps}>
      <Card.Front className={variantFront ? `fill-${variantFront}` : ""}>
        <Histogram
          running={running}
          bars={bars}
          random={random}
          interval={interval} 
          color="white" />
      </Card.Front>
    </Card>
  )
}
