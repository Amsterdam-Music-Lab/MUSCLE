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
import { Card, LinkButton, ShareOptions } from "@/components/ui";
import { Cup, ScoreCounter } from "@/components/game";

export interface HeaderProps {
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

export const Header: React.FC<HeaderProps> = ({
  title = "Dashboard",
  description,
  nextBlockSlug,
  nextBlockButtonText = "Play next experiment",
  aboutButtonText = "About this experiment",
  experimentSlug,
  totalScore,
  scoreDisplayConfig,
  socialMediaConfig,
}) => {
  return (
    <>
      <Card>
        <Card.Header title={title}>
          <RenderHtml html={description} />
          {aboutButtonText && (
            <LinkButton
              className="btn btn-lg btn-outline-primary"
              link={`/${experimentSlug}/about`}
            >
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
        <h3>{scoreDisplayConfig.noScoreLabel}</h3>
      )}
    </>
  );
};

export default Header;
