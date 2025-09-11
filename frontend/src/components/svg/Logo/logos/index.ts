/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

export const logos = {
  uva: () => import("@/components/svg/Logo/logos/UvA"),
  aml: () => import("@/components/svg/Logo/logos/AML"),
  tunetwins: () => import("@/components/svg/Logo/logos/TuneTwins"),
  nwo: () => import("@/components/svg/Logo/logos/NWO"),
  mcg: () => import("@/components/svg/Logo/logos/MCG"),
};
