/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { AllPluginSpec } from "@/components/plugins";
import type { ProfileData } from "@/types/profile";
import { Route, Routes } from "react-router-dom";
import { EXPERIMENT_SLUG, routes } from "@/config";
import useBoundStore from "@/util/stores";
import { Redirect, InternalRedirect, Reload } from "@/components/utils";
import { Block, Experiment, View } from "../";
import { useParticipantScores } from "@/API";

interface AppRoutesProps {
  /**
   * Whether to show the landing page
   */
  showLanding?: boolean;

  /**
   * Plugins to show on the landing page
   */
  landingPlugins?: AllPluginSpec[];
}

/**
 * The routes used by the app. This is a separate component, partly so that
 * we can call useLocation to ensure smooth page transitions
 *
 * TODO this is no longer neeeded as ViewTransitions is further down the tree now (in View)
 */
export default function AppRoutes({
  showLanding = false,
  landingPlugins = [],
}: AppRoutesProps) {
  const error = useBoundStore((state) => state.error);
  const participant = useBoundStore((state) => state.participant);

  return error ? (
    <View name="error" title="An error occured" message={error} />
  ) : !participant ? (
    <View name="loading" />
  ) : (
    <Routes>
      {/* Home: either a landing page or redirect to the experiment */}
      <Route
        index
        element={
          <HomeController
            showLanding={showLanding}
            landingPlugins={landingPlugins}
          />
        }
      />

      {/* Request reload for given participant */}
      <Route
        path={routes.reloadParticipant(":id", ":hash")}
        element={<Reload />}
      />

      {/* Internal redirect */}
      <Route path={routes.internalRedirect()} element={<InternalRedirect />} />

      {/* Profile */}
      <Route path={routes.profile()} element={<ProfileController />} />

      {/* Store profile */}
      <Route
        path={routes.storeProfile()}
        element={<View name="storeProfile" />}
      />

      {/* Block */}
      <Route
        path={routes.block(":expSlug", ":blockSlug")}
        element={<Block />}
      />

      {/*
       * Experiment. Note that this matches any other path; further handling
       * is delegated to the Experiment controller.
       */}
      <Route path={routes.experiment(":expSlug/*")} element={<Experiment />} />
    </Routes>
  );
}

// Controllers that handle additional logic or data fetching

function HomeController({ showLanding, landingPlugins }) {
  const path = routes.experiment(EXPERIMENT_SLUG);
  return showLanding ? (
    <View name="landing" experimentPath={path} plugins={landingPlugins} />
  ) : (
    <Redirect to={path} />
  );
}

function ProfileController() {
  const setError = useBoundStore((state) => state.setError);
  const [data, loadingData] = useParticipantScores<ProfileData>();
  if (loadingData) return <View name="loading" />;
  if (!data) return setError("An error occured while loading your profile...");
  return (
    <View
      name="profile"
      scores={data.scores}
      title={data.messages.title}
      summary={data.messages.summary}
      content={data.messages.continue}
      points={data.messages.points}
    />
  );
}
