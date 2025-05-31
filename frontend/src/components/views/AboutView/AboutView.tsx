/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { RenderHtml } from "@/components/utils";
import { ExperimentLayout, ExperimentLayoutProps } from "@/components/layout";
import { Card, LinkButton } from "@/components/ui";

export interface AboutViewProps extends ExperimentLayoutProps {
  content: string;
  slug: string;
  backButtonText?: string;
  title?: string;
}

export default function AboutView({
  content,
  slug,
  backButtonText = "Back",
  title = "About",
  ...layoutProps
}: AboutViewProps) {
  return (
    <ExperimentLayout className="container" {...layoutProps}>
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

  // Passed on to ExperimentLayout
  disclaimerHtml: experiment?.disclaimer,
  privacyHtml: experiment?.privacy,
  logos: experiment?.theme?.footer?.logos,
  showFooter: experiment?.theme?.footer,
});
AboutView.dependencies = ["experiment"];
