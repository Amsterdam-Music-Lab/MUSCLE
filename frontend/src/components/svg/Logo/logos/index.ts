/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import UvA from "./UvA";
import MCG from "./MCG";
import AML from "./AML";
import TuneTwins from "./TuneTwins";

export const components = { AML, MCG, TuneTwins, UvA };

export const logos = Object.fromEntries(
  Object.values(components).map((Component) => [Component._name, Component])
);
