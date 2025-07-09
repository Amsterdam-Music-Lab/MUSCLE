/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState, useEffect } from "react";
import useBoundStore from "@/util/stores";
import { useExperiment } from "@/API";
import useHeadDataFromExperiment from "@/hooks/useHeadDataFromExperiment";

import { Route, Routes, useParams } from "react-router-dom";
import { routes } from "@/config";
import { Block, View } from "@/components/application";
import { Redirect } from "@/components/utils";

/**
 * A component that controls an experiment. It loads the experiment data
 * and handles all routing related to the experiment: shows a consent form
 * (if consent has not been given, but is required) or a dashboard, or moves
 * on to the block view if possible.
 */
export default function Experiment() {
  const { expSlug } = useParams();
  const [experiment, loadingExperiment] = useExperiment(expSlug!);
  const [hasShownConsent, setHasShownConsent] = useState(false);
  const setTheme = useBoundStore((state) => state.setTheme);
  const setHeadData = useBoundStore((state) => state.setHeadData);
  const resetHeadData = useBoundStore((state) => state.resetHeadData);
  const participant = useBoundStore((state) => state.participant);

  useHeadDataFromExperiment(experiment, setHeadData, resetHeadData);

  // Update the global theme if the experiment has a theme set
  useEffect(() => {
    if (experiment?.theme) setTheme(experiment.theme);
  }, [experiment?.theme, setTheme]);

  // Loading...
  if (loadingExperiment) {
    return <View name="loading" />;
  }

  // Show an error if experiment is null, but not loading
  if (!loadingExperiment && !experiment) {
    return (
      <View
        name="error"
        message={`Experiment "${expSlug}" could not be found.`}
      />
    );
  }

  // Possibly redirect to the next block, if consent has been given,
  // there is no dashboard and a next block is specified.
  const consentRequired = !hasShownConsent && Boolean(experiment?.consent);
  const hasDashboard = experiment?.dashboard.length;
  if (!consentRequired && !hasDashboard && experiment?.nextBlock) {
    const params = { participant_id: participant?.participant_id_url };
    const path = routes.block(expSlug, experiment.nextBlock.slug, params);
    return <Redirect to={path} />;
  }

  // Return the experiment routes
  return (
    <Routes>
      {/*
       * Default: a consent form if that hasn't been signed yet,
       * otherwise show the experiment dashboard.
       * */}
      <Route
        index
        element={
          consentRequired ? (
            <View
              name="consent"
              experiment={experiment}
              onNext={() => setHasShownConsent(true)}
            />
          ) : (
            <View name="dashboard" experiment={experiment} />
          )
        }
      />

      {/* Block */}
      <Route path={routes.block(":exp", ":block")} element={<Block />} />

      {/* Information page about the experiment */}
      <Route
        path="/about"
        element={<View name="about" experiment={experiment} />}
      />

      {/* Information page about the experiment */}
      <Route
        path="/noconsent"
        element={<View name="consentDenied" experiment={experiment} />}
      />

      {/* Otherwise: invalid path */}
      <Route
        path="*"
        element={<View name="error" message="Page not found" />}
      />
    </Routes>
  );
}
