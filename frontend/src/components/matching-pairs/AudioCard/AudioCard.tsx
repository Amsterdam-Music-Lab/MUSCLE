/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { SpectrumProps } from "@/components/play";
import classNames from "classnames";
import { Spectrum } from "@/components/play";
import Card, { type CardProps } from "../Card/Card";
import styles from "./AudioCard.module.scss";

interface AudioCardProps
  extends CardProps,
    Omit<SpectrumProps, "variant" | "data"> {}

export default function AudioCard({
  running = false,
  bars = 6,
  random = true,
  interval = 300,
  className,
  variantFront = "primary",
  ...cardProps
}: AudioCardProps) {
  return (
    <Card className={classNames(styles.audio, className)} {...cardProps}>
      <Card.Front className={variantFront ? `fill-${variantFront}` : ""}>
        <Spectrum
          running={running}
          bars={bars}
          random={random}
          interval={interval}
          color="white"
        />
      </Card.Front>
    </Card>
  );
}
