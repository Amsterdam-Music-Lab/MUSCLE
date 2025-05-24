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
import { Link } from "react-router-dom";
import { RenderHtml } from "@/components/utils";
import { ShareOptions } from "@/components/ui";
import { Cup, ScoreCounter } from "@/components/game";

interface HeaderProps {
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
  description,
  nextBlockSlug,
  nextBlockButtonText,
  aboutButtonText,
  experimentSlug,
  totalScore,
  scoreDisplayConfig,
  socialMediaConfig,
}) => {
  return (
    <div className="hero">
      <div className="intro">
        <RenderHtml html={description} />
        <nav className="actions">
          {nextBlockSlug && (
            <a
              className="btn btn-lg btn-primary"
              href={`/block/${nextBlockSlug}`}
            >
              {nextBlockButtonText}
            </a>
          )}
          {aboutButtonText && (
            <Link
              className="btn btn-lg btn-outline-primary"
              to={`/${experimentSlug}/about`}
            >
              {aboutButtonText}
            </Link>
          )}
        </nav>
      </div>
      {scoreDisplayConfig && totalScore !== 0 && (
        <div className="results">
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
        </div>
      )}
      {scoreDisplayConfig && totalScore === 0 && (
        <h3>{scoreDisplayConfig.noScoreLabel}</h3>
      )}
    </div>
  );
};

export default Header;
