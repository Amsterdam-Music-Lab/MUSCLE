/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import type { ShareConfig } from "@/types/share";
import type { TimelineConfig } from "@/types/timeline";
import type { CardProps } from "@/components/ui";
import type { AllPluginSpec } from "@/components/plugins/pluginRegistry";
import type { SVGSymbolName, SVGSymbolProps } from "@/types/svg";

import classNames from "classnames";
import { Card } from "@/components/ui";
import { PluginRenderer } from "@/components/plugins";
import { symbols as svgSymbols } from "@/components/svg";
import styles from "./ScoreBoard.module.scss";

interface TrophyProps extends HTMLAttributes<HTMLDivElement> {
  icon: SVGSymbolName;
  message?: string;
  iconProps?: SVGSymbolProps;
}

/**
 * Shows a trophy icon with a message above it.
 */
function Trophy({
  icon,
  message,
  iconProps = {},
  className,
  ...divProps
}: TrophyProps) {
  const Trophy = svgSymbols[icon];
  if (!Trophy) {
    console.warn(`Trophy icon "${icon}" not found.`);
  }
  const props: SVGSymbolProps = {
    size: 100,
    variant: "secondary",
    ...iconProps,
  };
  props.className = classNames(styles.trophyIcon, iconProps.className);
  return (
    <div className={classNames(styles.trophy, className)} {...divProps}>
      {message && <p className={styles.trophyLabel}>{message}</p>}
      <Trophy {...props} />
    </div>
  );
}

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

  /**
   * Name of the trophy icon to show
   */
  trophyIcon?: SVGSymbolName;

  /**
   * Message to show below the trophy icon
   */
  trophyMessage?: string;

  /**
   * Whether to show the trophy if there is one. Default true.
   */
  showTrophy?: boolean;

  plugins?: AllPluginSpec[];
}

const DEFAULT_PLUGINS = [
  { name: "ranking" },
  { name: "scores" },
  { name: "share" },
] as AllPluginSpec[];

/**
 * A scoreboard that can render a range of plugins:
 *
 * - **ranking**: a progress bar showing the percentile,
 * - **scores**: the turn and total score,
 * - **share**: a button to share the score on social media,
 * - **timeline**: a timeline showing the progress of the game.
 *
 * Moreover, you can add plugins like **logo**, **markdown**, etc.
 * The order of the plugins, their parameters etc, can all be
 * configured in the `plugins` prop.
 */
export default function ScoreBoard({
  turnScore,
  totalScore,
  percentile,
  timeline,
  timelineStep,
  shareConfig,
  trophyIcon,
  trophyMessage = "Yay, you've earned a trophy!",
  showTrophy = true,
  plugins = DEFAULT_PLUGINS,
  className,
  ...cardProps
}: ScoreBoardProps) {
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
    <Card className={classNames(styles.scoreBoard, className)} {...cardProps}>
      {showTrophy && trophyIcon && (
        <Trophy icon={trophyIcon} message={trophyMessage} />
      )}

      <PluginRenderer
        plugins={plugins as AllPluginSpec[]}
        wrapper={Card.Section}
      />
    </Card>
  );
}
