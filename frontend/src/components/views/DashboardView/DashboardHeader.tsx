/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ScoreDisplayConfig } from "@/types/Theme";
import type { SocialMediaConfig } from "@/types/Experiment";

import React from "react";
import { RenderHtml } from "@/components/utils";
import { LinkButton } from "@/components/buttons";
import { Card } from "@/components/ui";
import { Cup, ScoreCounter, ShareOptions } from "@/components/modules";

export interface DashboardHeaderProps {
  title?: string;
  description: string;
  nextBlockSlug: string | undefined;
  nextBlockButtonText: string;
  experimentSlug: string;
  aboutButtonText: string;
  totalScore: number;
  scoreDisplayConfig?: ScoreDisplayConfig;
  socialMediaConfig?: SocialMediaConfig;
}

export default function DashboardHeader({
  title = "Dashboard",
  description,
  nextBlockSlug,
  nextBlockButtonText = "Play next experiment",
  aboutButtonText = "About this experiment",
  experimentSlug,
  totalScore,
  scoreDisplayConfig,
  socialMediaConfig,
}: DashboardHeaderProps) {
  return (
    <>
      <Card>
        <Card.Header title={title}>
          {description && (
            <RenderHtml html={description} style={{ marginBottom: ".75em" }} />
          )}
          {aboutButtonText && (
            <LinkButton link={`/${experimentSlug}/about`}>
              {aboutButtonText}
            </LinkButton>
          )}
        </Card.Header>
      </Card>

      {nextBlockSlug && (
        <LinkButton
          link={`/block/${nextBlockSlug}`}
          variant="secondary"
          rounded={false}
          stretch={true}
        >
          {nextBlockButtonText}
        </LinkButton>
      )}

      {scoreDisplayConfig && totalScore !== 0 && (
        // TODO use ScoreBadge from ProfileView
        <Card>
          <Card.Header title="Your total score">
            <Cup type={scoreDisplayConfig.scoreClass} label={false} />
            <h4>
              <ScoreCounter
                score={totalScore}
                label={scoreDisplayConfig.scoreLabel}
              />
            </h4>
            {socialMediaConfig?.channels?.length && (
              <ShareOptions config={socialMediaConfig} />
            )}
          </Card.Header>
        </Card>
      )}

      {scoreDisplayConfig && totalScore === 0 && (
        <Card>
          <Card.Header>{scoreDisplayConfig.noScoreLabel}</Card.Header>
        </Card>
      )}
    </>
  );
}
