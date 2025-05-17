/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ShareConfig } from "@/types/share";
import type { TimelineConfig } from "@/types/timeline";
import type { CardProps } from "@/components/ui";
import type { AllPluginSpec } from "@/components/plugins/pluginRegistry";

import { Card } from "@/components/ui";
import PluginRenderer from "@/components/plugins/PluginRenderer";
// import styles from "./ScoreBoard.module.scss";

// const defaultLabels = {
//   trophy: "Yay, you've earned a star!",
// };

export interface ScoreBoardProps extends CardProps {
  /** Score in the last turn */
  turnScore?: number;

  /** Total score */
  totalScore?: number;

  /** The percentile */
  percentile?: number;

  /** The timeline configuration */
  timeline?: TimelineConfig;

  /** The current step on the timeline */
  timelineStep?: number;

  shareConfig?: ShareConfig;

  plugins?: AllPluginSpec[];
}

const DEFAULT_PLUGINS = [
  { name: "ranking" },
  { name: "scores" },
  { name: "share" },
] as AllPluginSpec[];

export default function ScoreBoard({
  turnScore,
  totalScore,
  percentile,
  timeline,
  timelineStep,
  shareConfig,
  plugins = DEFAULT_PLUGINS,
  ...cardProps
}: ScoreBoardProps) {
  // const hasTimeline = timeline !== undefined && timelineStep !== undefined;
  // const hasTrophy = hasTimeline && timeline[timelineStep].trophy;
  // const Trophy =
  //   hasTrophy && timeline[timelineStep].symbol
  //     ? TIMELINE_SYMBOLS[timeline[timelineStep].symbol]
  //     : null;

  // Label templates
  // const templates = { ...defaultLabels, ...labels };
  // const templateData = {
  //   turnScore,
  //   totalScore,
  //   percentile: percentile !== undefined ? Math.round(percentile) : undefined,
  //   percentileCutoff,
  //   timelineStep,
  //   numSteps: timeline?.length,
  // };

  // Pass dynamic attributes to all plugins
  plugins = plugins.map((plugin) => {
    const updated: AllPluginSpec = { ...plugin };
    switch (plugin.name) {
      case "ranking":
        updated.args = { ...updated.args, percentile };
        break;

      case "scores":
        updated.args = { ...updated.args, turnScore, totalScore };
        break;

      case "share":
        updated.args = { ...updated.args, config: shareConfig };
        break;

      case "timeline":
        updated.args = { ...updated.args, step: timelineStep };
    }

    return updated;
  });

  return (
    <Card {...cardProps}>
      <PluginRenderer
        plugins={plugins as AllPluginSpec[]}
        wrapper={Card.Section}
      />
      {/* Star */}
      {/* {showTrophy && hasTrophy && ( */}
      {/* <div className={styles.trophy}>
        <p className={styles.trophyLabel}>Yay, you've earned a trophy!</p>

        {Trophy && (
          <Trophy
            className={styles.trophyIcon}
            variant="secondary"
            size={100}
            circleStrokeWidth={0.15}
          />
        )}
      </div> */}
      {/* )} */}
    </Card>
  );
}
