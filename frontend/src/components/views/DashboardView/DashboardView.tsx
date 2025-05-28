/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type IBlock from "@/types/Block";
import type Experiment from "@/types/Experiment";
import { useNavigate } from "react-router-dom";
import { Header } from "./Header";
import { ExperimentLayout } from "@/components/layout";
import "./DashboardView.module.scss"; // TODO: not modular yet
import { Card } from "@/components/ui";

export interface DashboardViewProps {
  experiment: Experiment;
  participantIdUrl: string | null;
  totalScore: number;
}

export default function DashboardView({
  experiment,
  participantIdUrl,
  totalScore,
}: DashboardViewProps) {
  const navigate = useNavigate();
  const getExperimentHref = (slug: string) =>
    `/block/${slug}${
      participantIdUrl ? `?participant_id=${participantIdUrl}` : ""
    }`;
  const header = experiment.theme?.header ?? {};
  return (
    <ExperimentLayout experiment={experiment}>
      <Header
        title={experiment.name}
        nextBlockSlug={experiment.nextBlock?.slug}
        experimentSlug={experiment.slug}
        totalScore={totalScore}
        description={experiment.description}
        scoreDisplayConfig={header?.score}
        nextBlockButtonText={header?.nextBlockButtonText}
        aboutButtonText={header?.aboutButtonText}
        socialMediaConfig={experiment.socialMediaConfig}
      />

      <Card data-testid="dashboard-experiments">
        <Card.Header title="Experiments" />
        {experiment.dashboard.map((exp: IBlock) => (
          <Card.Option
            key={exp.slug}
            title={`Go to experiment '${exp.name}'`}
            spacing="narrow"
            onClick={() => navigate(getExperimentHref(exp.slug))}
          >
            {exp.image?.file && (
              <img
                src={exp.image?.file}
                alt={exp.image?.alt ?? exp.description}
              />
            )}
            {exp.description}
          </Card.Option>
        ))}
        {experiment.dashboard.length === 0 && (
          <Card.Option>No experiments found</Card.Option>
        )}
      </Card>
    </ExperimentLayout>
  );
}

DashboardView.viewName = "dashboard";
DashboardView.usesOwnLayout = true;
DashboardView.getViewProps = ({ experiment }) => ({ experiment });
DashboardView.dependencies = ["experiment"];
