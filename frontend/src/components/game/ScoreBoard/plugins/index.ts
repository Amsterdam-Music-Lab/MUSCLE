/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Ranking from "./RankingPlugin";
import LogoPlugin from "./LogoPlugin";
import ScoresPlugin from "./ScoresPlugin";
import TimelinePlugin from "./TimelinePlugin";
import SharePlugin from "./SharePlugin";

export const components = {
  Ranking,
  LogoPlugin,
  ScoresPlugin,
  TimelinePlugin,
  SharePlugin,
};

export const plugins = Object.fromEntries(
  Object.values(components).map((Component) => [Component._name, Component])
);
