/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { RenderHtml } from "@/components/utils";
import { ExperimentLayout } from "@/components/layout";
import Experiment from "@/types/Experiment";
import { Card, LinkButton } from "@/components/ui";

export interface AboutViewProps {
  content: string;
  slug: string;
  backButtonText: string;
  experiment: Experiment;
  title?: string;
}

export default function AboutView({
  experiment,
  content,
  slug,
  backButtonText,
  title = "About",
}: AboutViewProps) {
  console.log(experiment);
  return (
    <ExperimentLayout experiment={experiment} className="container">
      <Card>
        <Card.Header title={title} />
        <Card.Section>
          <RenderHtml html={content} innerClassName="prose" />
        </Card.Section>
      </Card>
      <LinkButton link={`/${slug}`} variant="secondary" rounded={false}>
        <i className="fas fa-arrow-left mr-2"></i>
        {backButtonText}
      </LinkButton>
    </ExperimentLayout>
  );
}

AboutView.viewName = "about";
AboutView.usesOwnLayout = true;
AboutView.getViewProps = ({ experiment }) => ({
  experiment,
  content: experiment.aboutContent,
  slug: experiment.slug,
  backButtonText: experiment.backButtonText,
});
AboutView.dependencies = ["experiment"];
