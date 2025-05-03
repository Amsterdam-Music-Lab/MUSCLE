/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLProps, ReactNode } from "react";
import type { ShareConfig } from "@/types/share";
import type { TimelineConfig } from "@/types/timeline";

import classNames from "@/util/classNames";
import { renderTemplate } from "@/util/renderTemplate";
import { ShareOptions, ExpandableButton, Card } from "@/components/ui";
import { Timeline } from "@/components/game";
import { TIMELINE_SYMBOLS } from "@/components/game/Timeline/Timeline";
import { ScoreBar } from "../ScoreBar";
import { ScoreDisplay as Score } from "../ScoreDisplay";

import styles from "./ScoreBoard.module.scss";
import { Logo } from "@/components/svg";

interface SectionLabelProps extends HTMLProps<HTMLParagraphElement> {
  variant?: "primary" | "secondary" | "tertiary";
}

const SectionLabel = ({
  children,
  variant = "primary",
  className,
  ...paragraphProps
}: SectionLabelProps) => (
  <p
    className={classNames(
      styles.sectionLabel,
      `text-fill-${variant}`,
      className
    )}
    {...paragraphProps}
  >
    {children}
  </p>
);

const defaultLabels = {
  turnScore: "Last game",
  totalScore: "Total score",
  scoreHeader: "",
  percentileAboveCutoff:
    "Congrats! You did better than {{percentile}}% of players at this level",
  percentileBelowCutoff:
    "Congrats! You did better than {{percentileCutoff}}% of players at this level",
  trophy: "Yay, you've earned a star!",
  timelineHeader: "Your progress",
};

export interface ScoreBoardProps {
  /** Score in the last turn */
  turnScore?: number;

  /** Total score */
  totalScore?: number;

  /** The percentile */
  percentile?: number;

  /** The percentile cutoff below which another message is shown. */
  percentileCutoff?: number;

  /** The timeline configuration */
  timeline?: TimelineConfig;

  /** The current step on the timeline */
  timelineStep?: number;

  shareConfig?: ShareConfig;

  /** An optional logo displayed at the top */
  logo?: ReactNode;

  /** Whether to show the percentile progres bar */
  showPercentile?: boolean;

  /** Whether to show the scores */
  showScores?: boolean;

  /** Whether to show the timelie */
  showTimeline?: boolean;

  /** Whether to sho the trophy */
  showTrophy?: boolean;

  showShare?: boolean;

  /**
   * Labels used in the scoreboard. These are template strings of the form
   * "You scored {{score}} points". You can access the variables score, totalScore
   * percentile, percentileCutoff, step, numSteps.
   */
  labels?: Record<string, string>;
}

export default function ScoreBoard({
  turnScore,
  totalScore,
  percentile,
  percentileCutoff = 30,
  timeline,
  timelineStep,
  shareConfig,
  logo,
  showPercentile = true,
  showScores = true,
  showTimeline = true,
  showTrophy = true,
  showShare = true,
  labels = {},
}: ScoreBoardProps) {
  showShare = showShare && Boolean(shareConfig);
  const hasPercentile =
    typeof percentile === "number" && percentile >= 0 && percentile <= 100;
  const hasTimeline = timeline !== undefined && timelineStep !== undefined;
  const hasTrophy = hasTimeline && timeline[timelineStep].trophy;
  const Trophy =
    hasTrophy && timeline[timelineStep].symbol
      ? TIMELINE_SYMBOLS[timeline[timelineStep].symbol]
      : null;

  // Label templates
  const templates = { ...defaultLabels, ...labels };
  const templateData = {
    turnScore,
    totalScore,
    percentile: percentile !== undefined ? Math.round(percentile) : undefined,
    percentileCutoff,
    timelineStep,
    numSteps: timeline?.length,
  };

  return (
    <Card className={classNames(styles.scoreBoard)}>
      <Card.Header style={{ display: "flex", justifyContent: "start" }}>
        <Logo
          name="tunetwins"
          variant="primary"
          style={{ height: "2.5em", marginLeft: "1em" }}
        />
      </Card.Header>

      {/* Star */}
      {showTrophy && hasTrophy && (
        <div className={styles.trophy}>
          <p className={styles.trophyLabel}>
            {renderTemplate(templates.trophy, templateData)}
          </p>

          {Trophy && (
            <Trophy
              className={styles.trophyIcon}
              variant="secondary"
              size={100}
              circleStrokeWidth={0.15}
            />
          )}
        </div>
      )}

      {/* Percentile */}
      {showPercentile && hasPercentile && percentile > 0 && (
        <Card.Section
          title={renderTemplate(
            percentile > percentileCutoff
              ? templates.percentileAboveCutoff
              : templates.percentileBelowCutoff,
            templateData
          )}
        >
          <ScoreBar
            value={
              percentile > percentileCutoff ? percentile : percentileCutoff
            }
            variant="primary"
          />
        </Card.Section>
      )}

      {/* Ranking */}
      {showScores && (
        <Card.Section title={labels.scoreHeader}>
          <div className="d-flex">
            <div style={{ width: "50%" }}>
              <Score
                score={turnScore}
                label={renderTemplate(templates.turnScore, templateData)}
                variant="secondary"
              />
            </div>
            <div style={{ width: "50%" }}>
              <Score
                score={totalScore}
                label={renderTemplate(templates.totalScore, templateData)}
                variant="secondary"
              />
            </div>
          </div>
        </Card.Section>
      )}

      {/* Progress */}
      {showTimeline && hasTimeline && (
        <Card.Section
          title={renderTemplate(templates.timelineHeader, templateData)}
        >
          <Timeline
            timeline={timeline}
            step={timelineStep + 1}
            spine={true}
            variant="primary"
          />
        </Card.Section>
      )}

      {/* Share and options */}
      {showShare && (
        <Card.Section>
          <ExpandableButton title="Share" rounded={true} variant="secondary">
            <ShareOptions config={shareConfig!} />
          </ExpandableButton>
        </Card.Section>
      )}
    </Card>
  );
}
