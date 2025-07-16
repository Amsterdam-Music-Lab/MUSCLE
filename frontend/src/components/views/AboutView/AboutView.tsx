/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { RenderHtml } from "@/components/utils";
import { ExperimentLayout, ExperimentLayoutProps } from "@/components/layout";
import { LinkButton } from "@/components/buttons";
import { Card } from "@/components/ui";
import { t } from "@lingui/macro";

export interface AboutViewProps extends ExperimentLayoutProps {
  content: string;
  slug: string;
  backButtonText?: string;
  title?: string;
}

export default function AboutView({
  content,
  slug,
  backButtonText = t`Back`,
  title = t`About`,
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
