/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import classNames from "@/util/classNames";

// import TuneTwins from "@/components/MCGTheme/logos/TuneTwins";
import Timeline, {
  TIMELINE_SYMBOLS,
  TimelineConfig,
} from "@/components/game/Timeline/Timeline";
import { ScoreBar } from "../ScoreBar";
import { ScoreDisplay as Score } from "../ScoreDisplay";
import { renderTemplate } from "@/util/renderTemplate";

// TODO use scoped scss
import styles from "./ScoreBoard.module.scss";

interface SectionLabelProps extends React.HTMLProps<HTMLParagraphElement> {
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
  score: "Last game",
  totalScore: "Total score",
  percentileAboveCutoff:
    "Congrats! You did better than {{percentile}}% of players at this level",
  percentileBelowCutoff:
    "Congrats! You did better than {{percentileCutoff}}% of players at this level",
  trophy: "Yay, you've earned a star!",
  timeline: "Your progress",
};

interface ScoreBoardProps {
  score?: number;

  /** Total score */
  totalScore?: number;

  /** The percentile */
  percentile?: number;

  /** The timeline configuration */
  timeline?: TimelineConfig;

  /** The current step on the timeline */
  step?: number;

  /** The percentile cutoff below which another message is shown. */
  percentileCutoff: number;

  /** An optional logo displayed at the top */
  logo: React.ReactNode;

  /** Whether to show the percentile progres bar */
  showPercentile: boolean;

  /** Whether to show the scores */
  showScores: boolean;

  /** Whether to show the timelie */
  showTimeline: boolean;

  /** Whether to sho the trophy */
  showTrophy: boolean;

  /**
   * Labels used in the scoreboard. These are template strings of the form
   * "You scored {{score}} points". You can access the variables score, totalScore
   * percentile, percentileCutoff, step, numSteps.
   */
  labels?: Record<string, string>;
}

export default function ScoreBoard({
  score,
  totalScore,
  percentile,
  timeline,
  step,
  logo,
  percentileCutoff = 30,
  showPercentile = true,
  showScores = true,
  showTimeline = true,
  showTrophy = true,
  labels = {},
}: ScoreBoardProps) {
  const hasPercentile =
    typeof percentile === "number" && percentile >= 0 && percentile <= 100;
  const hasTimeline = timeline !== undefined && step !== undefined;
  const hasTrophy = hasTimeline && timeline[step].trophy;
  const Trophy =
    hasTrophy && timeline[step].symbol
      ? TIMELINE_SYMBOLS[timeline[step].symbol]
      : null;

  // Label templates
  const templates = { ...defaultLabels, ...labels };
  const templateData = {
    score,
    totalScore,
    percentile: percentile !== undefined ? Math.round(percentile) : undefined,
    percentileCutoff,
    step,
    numSteps: timeline?.length,
  };

  return (
    <div className={classNames(styles.scoreBoard, "card")}>
      {/* Capture this */}
      {/* A square card that fits inside the rounded card and should be captured */}
      {/* as an image for sharing on social media */}
      <div className={styles.capture}>
        {/* TuneTwins logo */}
        {logo && <div className="pl-2 px-4">{logo}</div>}

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

        <div className="list-group list-group-flush bg-transparent">
          {/* Percentile */}
          {showPercentile && hasPercentile && percentile > 0 && (
            <div className="list-group-item p-4 bg-transparent">
              {percentile > percentileCutoff ? (
                <>
                  <SectionLabel style={{ maxWidth: "70%" }}>
                    {renderTemplate(
                      templates.percentileAboveCutoff,
                      templateData
                    )}
                  </SectionLabel>
                  <ScoreBar value={percentile} variant="primary" />
                </>
              ) : (
                <>
                  <SectionLabel>
                    {renderTemplate(
                      templates.percentileBelowCutoff,
                      templateData
                    )}
                  </SectionLabel>
                  <ScoreBar value={percentileCutoff} variant="primary" />
                </>
              )}
            </div>
          )}

          {/* Ranking */}
          {/* Note that falls back gracefully when score or totalScore are missing. */}
          {showScores && (
            <div className="list-group-item p-4 bg-transparent">
              {/* <SectionLabel>Your scores</SectionLabel> */}
              <div className="d-flex">
                <div style={{ width: "50%" }}>
                  <Score
                    score={score}
                    label={renderTemplate(templates.score, templateData)}
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
            </div>
          )}

          {/* Progress */}
          {showTimeline && hasTimeline && (
            <div className="list-group-item p-4 bg-transparent">
              {/* The label should depend on the step in the timeline */}
              <SectionLabel>
                {renderTemplate(templates.timeline, templateData)}
              </SectionLabel>
              <Timeline
                timeline={timeline}
                step={step + 1}
                spine={true}
                variant="primary"
              />
            </div>
          )}
        </div>
      </div>
      {/* End of capture */}

      {/* Share and options */}
      <div className="list-group-item p-4 bg-transparent border-left-0 border-right-0 border-bottom-0">
        <button className="btn bg-indigo-red text-white rounded-lg px-4 py-1">
          Share
        </button>
      </div>
    </div>
  );
}
