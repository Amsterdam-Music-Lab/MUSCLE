/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

// Logo plugin
import type { LogoPluginMeta, LogoPluginSpec } from "./plugins/LogoPlugin";
import { logoPlugin } from "./plugins/LogoPlugin";

// Scores plugin
import type {
  ScoresPluginMeta,
  ScoresPluginSpec,
} from "./plugins/ScoresPlugin";
import { scoresPlugin } from "./plugins/ScoresPlugin";

// Share plugin
import type { SharePluginMeta, SharePluginSpec } from "./plugins/SharePlugin";
import { sharePlugin } from "./plugins/SharePlugin";

// Timeline
import type {
  TimelinePluginMeta,
  TimelinePluginSpec,
} from "./plugins/TimelinePlugin";
import { timelinePlugin } from "./plugins/TimelinePlugin";

// Ranking
import type {
  RankingPluginMeta,
  RankingPluginSpec,
} from "./plugins/RankingPlugin";
import { rankingPlugin } from "./plugins/RankingPlugin";

// Overall ranking
import type {
  OverallRankingPluginMeta,
  OverallRankingPluginSpec,
} from "./plugins/OverallRankingPlugin";
import { overallRankingPlugin } from "./plugins/OverallRankingPlugin";

import type {
  ScoreboardPluginMeta,
  ScoreboardPluginSpec,
} from "./plugins/ScoreboardPlugin";
import { scoreboardPlugin } from "./plugins/ScoreboardPlugin";

import type {
  UserPagesPluginMeta,
  UserPagesPluginSpec,
} from "./plugins/UserPagesPlugin";
import { userPagesPlugin } from "./plugins/UserPagesPlugin";

import type {
  UserFeedbackPluginMeta,
  UserFeedbackPluginSpec,
} from "./plugins/UserFeedbackPlugin";
import { userFeedbackPlugin } from "./plugins/UserFeedbackPlugin";

import type {
  ParticipantLinkPluginMeta,
  ParticipantLinkPluginSpec,
} from "./plugins/ParticipantLinkPlugin";
import { participantLinkPlugin } from "./plugins/ParticipantLinkPlugin";

import type {
  LinkButtonPluginMeta,
  LinkButtonPluginSpec,
} from "./plugins/LinkButtonPlugin";
import { linkButtonPlugin } from "./plugins/LinkButtonPlugin";

import type {
  FooterPluginMeta,
  FooterPluginSpec,
} from "./plugins/FooterPlugin";
import { footerPlugin } from "./plugins/FooterPlugin";

import type {
  MarkdownPluginMeta,
  MarkdownPluginSpec,
} from "./plugins/MarkdownPlugin";
import { markdownPlugin } from "./plugins/MarkdownPlugin";

import type { CardPluginMeta, CardPluginSpec } from "./plugins/CardPlugin";
import { cardPlugin } from "./plugins/CardPlugin";

import type {
  QRCodePluginMeta,
  QRCodePluginSpec,
} from "./plugins/QRCodePlugin";
import { qrCodePlugin } from "./plugins/QRCodePlugin";

import type { FlexPluginMeta, FlexPluginSpec } from "./plugins/FlexPlugin";
import { flexPlugin } from "./plugins/FlexPlugin";

import type {
  TrophyPluginMeta,
  TrophyPluginSpec,
} from "./plugins/TrophyPlugin";
import { trophyPlugin } from "./plugins/TrophyPlugin";

//
// Combine all types
//

export type AllPluginMeta =
  | LogoPluginMeta
  | ScoresPluginMeta
  | SharePluginMeta
  | TimelinePluginMeta
  | RankingPluginMeta
  | OverallRankingPluginMeta
  | ScoreboardPluginMeta
  | UserPagesPluginMeta
  | UserFeedbackPluginMeta
  | ParticipantLinkPluginMeta
  | LinkButtonPluginMeta
  | FooterPluginMeta
  | MarkdownPluginMeta
  | CardPluginMeta
  | QRCodePluginMeta
  | FlexPluginMeta
  | TrophyPluginMeta;

export type AllPluginSpec =
  | LogoPluginSpec
  | ScoresPluginSpec
  | SharePluginSpec
  | TimelinePluginSpec
  | RankingPluginSpec
  | OverallRankingPluginSpec
  | ScoreboardPluginSpec
  | UserPagesPluginSpec
  | UserFeedbackPluginSpec
  | ParticipantLinkPluginSpec
  | LinkButtonPluginSpec
  | FooterPluginSpec
  | MarkdownPluginSpec
  | CardPluginSpec
  | QRCodePluginSpec
  | FlexPluginSpec
  | TrophyPluginSpec;

export type PluginRegistry = Record<AllPluginMeta["name"], AllPluginMeta>;

// Registry of all plugin meta objects
export const pluginMetaRegistry: PluginRegistry = {
  [logoPlugin.name]: logoPlugin,
  [scoresPlugin.name]: scoresPlugin,
  [sharePlugin.name]: sharePlugin,
  [timelinePlugin.name]: timelinePlugin,
  [rankingPlugin.name]: rankingPlugin,
  [overallRankingPlugin.name]: overallRankingPlugin,
  [scoreboardPlugin.name]: scoreboardPlugin,
  [userPagesPlugin.name]: userPagesPlugin,
  [userFeedbackPlugin.name]: userFeedbackPlugin,
  [participantLinkPlugin.name]: participantLinkPlugin,
  [linkButtonPlugin.name]: linkButtonPlugin,
  [footerPlugin.name]: footerPlugin,
  [markdownPlugin.name]: markdownPlugin,
  [cardPlugin.name]: cardPlugin,
  [qrCodePlugin.name]: qrCodePlugin,
  [flexPlugin.name]: flexPlugin,
  [trophyPlugin.name]: trophyPlugin,
};
