/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type TBlock from "@/types/Block";
import type { Header as THeader } from "@/types/Theme";
import type { SocialMediaConfig } from "@/types/Experiment";

import { useNavigate } from "react-router-dom";
import { ExperimentLayout, ExperimentLayoutProps } from "@/components/layout";
import { Card } from "@/components/ui";
import DashboardHeader from "./DashboardHeader";
import { routes } from "@/config";

export interface DashboardViewProps extends ExperimentLayoutProps {
  slug: string;
  name: string;
  description: string;
  dashboard: TBlock;
  nextBlock: TBlock | null;
  aboutContent: string;
  totalScore: number;
  socialMediaConfig?: SocialMediaConfig;
  participantId: string | null;
  header: Partial<THeader>;
}

export default function DashboardView({
  name,
  slug,
  description,
  nextBlock,
  totalScore,
  socialMediaConfig,
  participantId,
  dashboard,
  header = {},
  ...layoutProps
}: DashboardViewProps) {
  const navigate = useNavigate();
  const hasDashboard = dashboard && dashboard.length > 0;
  return (
    <ExperimentLayout {...layoutProps}>
      <DashboardHeader
        title={name}
        experimentSlug={slug}
        totalScore={totalScore}
        nextBlockSlug={nextBlock?.slug}
        description={description}
        socialMediaConfig={socialMediaConfig}
        scoreDisplayConfig={header?.score}
        nextBlockButtonText={header?.nextBlockButtonText}
        aboutButtonText={header?.aboutButtonText}
      />

      <Card data-testid="dashboard-experiments">
        <Card.Header title="Experiments" />

        {hasDashboard ? (
          dashboard.map((exp: TBlock) => {
            const path = routes.block(exp.slug, {
              participant_id: participantId,
            });
            return (
              <Card.Option
                key={exp.slug}
                title={`Go to experiment '${exp.name}'`}
                spacing="narrow"
                onClick={() => navigate(path)}
              >
                {exp.image?.file && (
                  <img
                    src={exp.image?.file}
                    alt={exp.image?.alt ?? exp.description}
                  />
                )}
                {exp.description}
              </Card.Option>
            );
          })
        ) : (
          <Card.Option>No experiments found</Card.Option>
        )}
      </Card>
    </ExperimentLayout>
  );
}

DashboardView.viewName = "dashboard";
DashboardView.usesOwnLayout = true;
DashboardView.getViewProps = ({ experiment, participant }) => ({
  name: experiment.name,
  slug: experiment.slug,
  description: experiment.description,
  totalScore: experiment.totalScore,
  nextBlock: experiment.nextBlock,
  header: experiment?.theme?.header ?? {},
  socialMediaConfig: experiment.socialMediaConfig,
  participantId: participant?.participant_id_url,
  dashboard: experiment.dashboard,

  // Passed on to ExperimentLayout
  disclaimerHtml: experiment?.disclaimer,
  privacyHtml: experiment?.privacy,
  logos: experiment?.theme?.footer?.logos,
  showFooter: experiment?.theme?.footer,
});
DashboardView.dependencies = ["experiment", "participant"];
