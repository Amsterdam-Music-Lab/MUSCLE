/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ShareConfig } from "@/types/share";
import type { TimelineConfig } from "@/types/timeline";
import type { CardProps, PluginSpec } from "@/components/ui";

import classNames from "classnames";
import { Card } from "@/components/ui";
import styles from "./ScoreBoard.module.scss";
import PluginRenderer from "@/components/plugins/PluginRenderer";

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

  plugins?: PluginSpec[];
}

const DEFAULT_PLUGINS: PluginSpec[] = [
  { name: "ranking" },
  { name: "scores" },
  { name: "share" },
];

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
    const updated: PluginSpec = { ...plugin };
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
      <PluginRenderer plugins={plugins} wrapper={Card.Section} />
      {/* Star */}
      {/* {showTrophy && hasTrophy && (
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
        )} */}
    </Card>
  );
}
