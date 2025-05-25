/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type IBlock from "@/types/Block";
import type Experiment from "@/types/Experiment";

import { Link } from "react-router-dom";
import { Header } from "../Header";
import { Logo } from "@/components/application";
import "./Dashboard.module.scss"; // TODO: not modular yet

export interface DashboardProps {
  experiment: Experiment;
  participantIdUrl: string | null;
  totalScore: number;
}

export default function Dashboard({
  experiment,
  participantIdUrl,
  totalScore,
}: DashboardProps) {
  const { dashboard, description } = experiment;
  const { nextBlockButtonText, aboutButtonText } = experiment.theme?.header || {
    nextBlockButtonText: "",
    aboutButtonText: "",
  };

  const scoreDisplayConfig = experiment.theme?.header?.score;
  const nextBlockSlug = experiment.nextBlock?.slug;
  const showHeader = experiment.theme?.header;
  const socialMediaConfig = experiment.socialMediaConfig;

  const getExperimentHref = (slug: string) =>
    `/block/${slug}${
      participantIdUrl ? `?participant_id=${participantIdUrl}` : ""
    }`;

  return (
    <div className="aha__dashboard">
      <Logo />
      {showHeader && (
        <Header
          nextBlockSlug={nextBlockSlug}
          experimentSlug={experiment.slug}
          totalScore={totalScore}
          description={description}
          scoreDisplayConfig={scoreDisplayConfig}
          nextBlockButtonText={nextBlockButtonText}
          aboutButtonText={aboutButtonText}
          socialMediaConfig={socialMediaConfig}
        />
      )}
      {/* Experiments */}
      <div role="menu" className="dashboard toontjehoger">
        <ul>
          {dashboard.map((exp: IBlock) => (
            <li key={exp.slug}>
              <Link to={getExperimentHref(exp.slug)} role="menuitem">
                <ImageOrPlaceholder
                  imagePath={exp.image?.file}
                  alt={exp.image?.alt ?? exp.description}
                />
                <h3>{exp.name}</h3>
                <p>{exp.description}</p>
              </Link>
            </li>
          ))}
          {dashboard.length === 0 && <p>No experiments found</p>}
        </ul>
      </div>
    </div>
  );
}

const ImageOrPlaceholder = ({
  imagePath,
  alt,
}: {
  imagePath?: string;
  alt: string;
}) => {
  const imgSrc = imagePath ?? null;

  return imgSrc ? (
    <img src={imgSrc} alt={alt} />
  ) : (
    <div className="placeholder" />
  );
};
