/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { CardProps } from "@/components/ui";
import classNames from "classnames";

import { Cup, CupType } from "@/components/modules";
import { routes } from "@/config";

import { Card } from "@/components/ui";
import { LinkButton } from "@/components/buttons";
import styles from "./ScoreBadge.module.scss";

export interface ScoreBadgeProps extends CardProps {
  score: number;
  block_slug: string;
  block_name: string;
  date?: string;
  cupLabel?: string;
  cupType?: CupType;
  finished_at: string;
}

export default function ScoreBadge({
  score,
  date,
  cupType,
  cupLabel,
  blockName,
  blockSlug,
  pointsLabel = "points",
  className,
  ...cardProps
}: ScoreBadgeProps) {
  return (
    <Card className={classNames(styles.badge, className)} {...cardProps}>
      <Cup className={styles.cup} type={cupType} text={cupLabel} radius={150} />
      {(blockSlug || score) && (
        <Card.Header title={score && `${score} ${pointsLabel}`}>
          {blockSlug && (
            <>
              <p>
                {blockName ?? `Block "${blockSlug}"`}{" "}
                {date && (
                  <>
                    <span className={styles.sep}>•</span> {date}
                  </>
                )}
              </p>
              <LinkButton
                link={routes.block(blockSlug)}
                size="sm"
                stretch={true}
              >
                Go to {blockName ?? `Block "${blockSlug}"`}
              </LinkButton>
            </>
          )}
        </Card.Header>
      )}
    </Card>
  );
}
