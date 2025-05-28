/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type IExperiment from "@/types/Experiment";

import { useState, useEffect } from "react";
import useBoundStore from "@/util/stores";
import { useExperiment } from "@/API";
import useHeadDataFromExperiment from "@/hooks/useHeadDataFromExperiment";

import { Route, Routes, useParams } from "react-router-dom";
import { View } from "@/components/application";
import { Redirect } from "@/components/utils";
import { About, Dashboard, Footer } from "../";
import "./Experiment.module.scss"; // TODO: not modular yet

export default function Experiment() {
  const { slug } = useParams();

  const [experiment, loadingExperiment] = useExperiment(slug!) as [
    IExperiment,
    boolean
  ];
  const [hasShownConsent, setHasShownConsent] = useState(false);
  const participant = useBoundStore((state) => state.participant);
  const setTheme = useBoundStore((state) => state.setTheme);
  const setHeadData = useBoundStore((state) => state.setHeadData);
  const resetHeadData = useBoundStore((state) => state.resetHeadData);
  const participantIdUrl = participant?.participant_id_url;
  const nextBlock = experiment?.nextBlock;
  const displayDashboard = experiment?.dashboard.length;
  const showConsent = experiment?.consent;
  const totalScore = experiment?.totalScore;

  useHeadDataFromExperiment(experiment, setHeadData, resetHeadData);

  useEffect(() => {
    if (experiment?.theme) {
      setTheme(experiment.theme);
    }
  }, [experiment?.theme, setTheme]);

  const onNext = () => {
    setHasShownConsent(true);
  };

  const getBlockHref = (slug: string) =>
    `/block/${slug}${
      participantIdUrl ? `?participant_id=${participantIdUrl}` : ""
    }`;

  if (loadingExperiment) {
    return <View name="loading" />;
  } else if (!loadingExperiment && !experiment)
    return <View name="error" message="Experiment not found" />;
  else if (!hasShownConsent && showConsent) {
    return (
      <View
        name="consent"
        participant={participant}
        experiment={experiment}
        onNext={onNext}
      />
    );
  } else if (!displayDashboard && nextBlock) {
    return <Redirect to={getBlockHref(nextBlock.slug)} />;
  }

  // TODO: why arent these routes in /App?
  return (
    <div className="aha__experiment">
      <Routes>
        <Route
          path={"/about"}
          element={
            <About
              content={experiment?.aboutContent}
              slug={experiment.slug}
              backButtonText={experiment.backButtonText}
            />
          }
        />
        <Route
          path={"*"}
          element={
            <Dashboard
              experiment={experiment}
              participantIdUrl={participantIdUrl}
              totalScore={totalScore}
            />
          }
        />
      </Routes>
      {experiment.theme?.footer && (
        <Footer
          disclaimer={experiment.disclaimer}
          logos={experiment.theme.footer.logos}
          privacy={experiment.privacy}
        />
      )}
    </div>
  );
}
