/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { NarrowLayoutProps } from "../NarrowLayout";
import type Experiment from "@/types/Experiment";
import { Footer } from "./Footer";
import { NarrowLayout } from "../NarrowLayout";

export interface ExperimentLayoutProps extends NarrowLayoutProps {
  experiment: Experiment;
}

// TODO This whole component is redundant.
// The footer should be a plugin, and the About and Dashboard
// views should be plugin renderers

export default function ExperimentLayout({
  children,
  experiment,
  ...layoutProps
}: ExperimentLayoutProps) {
  return (
    <NarrowLayout {...layoutProps}>
      {children}
      {experiment?.theme?.footer && (
        <Footer
          disclaimerHtml={experiment?.disclaimer}
          logos={experiment?.theme?.footer?.logos}
          privacyHtml={experiment?.privacy}
        />
      )}
    </NarrowLayout>
  );
}
