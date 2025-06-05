/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { useEffect, createContext, useContext, useState } from "react";
import type { AllPluginSpec } from "@/components/plugins";
import type { ProfileData } from "@/types/profile";
import {
  Route,
  Routes,
  useLocation,
  useParams,
  Outlet,
  Navigate,
} from "react-router-dom";
import { EXPERIMENT_SLUG, routes } from "@/config";
import useBoundStore from "@/util/stores";
import { Redirect, InternalRedirect, Reload } from "@/components/utils";
import { ViewTransition } from "@/components/layout";
import { Block, Experiment, View } from "../";
import { useBlock, useExperiment, useParticipantScores } from "@/API";
import useLogLifeCycle from "@/util/useLogLifeCycle";

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
      <Route path="profile" element={<ProfileController />}>
        <Route path="store" element={<View name="storeProfile" />} />
      </Route>

      {/* Store profile */}

      {/*
       * Experiment. Note that this matches any other path; further handling
       * is delegated to the Experiment controller.
       */}
      <Route path=":expSlug" element={<ExperimentController />}>
        <Route path="block/:blockSlug" element={<BlockController />} />
        <Route path="dashboard" element={<View name="dashboard" />} />
        <Route path="about" element={<View name="about" />} />
        <Route path="consent" element={<ConsentController />} />
        <Route path="noconsent" element={<View name="consentDenied" />} />
      </Route>
    </Routes>
  );
}
// Controllers that handle additional logic or data fetching

function useBlockData(blockSlug) {
  const [error, setError] = useState<string | null>(null);

  // Global state
  const session = useBoundStore((state) => state.session);
  const setSession = useBoundStore((state) => state.setSession);
  const setBlock = useBoundStore((state) => state.setBlock);
  const theme = useBoundStore((state) => state.theme);
  const setTheme = useBoundStore((state) => state.setTheme);
  const resetTheme = useBoundStore((state) => state.resetTheme);
  const setHeadData = useBoundStore((state) => state.setHeadData);
  const resetHeadData = useBoundStore((state) => state.resetHeadData);

  const [block, loading] = useBlock(blockSlug);

  useEffect(() => {
    if (loading) {
      // Nothing: still loading...
    } else if (!block) {
      setError("Could not load a block");
    } else if (!block.session_id && session) {
      setError("Session could not be created");
    } else {
      // Finished loading!
      setBlock(block);
      setSession({ id: block.session_id });
      setHeadData({
        title: block.name,
        description: block.description,
        image: block.image?.file ?? "",
        url: window.location.href,
        structuredData: { "@type": "Block" },
      });
    }

    return resetHeadData; // Clean up
  }, [block, loading, setError]);

  useEffect(() => {
    if (block?.theme) setTheme(block.theme);
    if (!block?.theme && theme) resetTheme();
  }, [block, theme, setTheme, resetTheme]);

  return [block, loading, session, error];
}

const BlockContext = createContext(null);
export const useBlockContext = () => useContext(BlockContext);

function BlockController() {
  useLogLifeCycle("BlockController");

  const { blockSlug } = useParams();
  const [block, loading, session, error] = useBlockData(blockSlug);
  const notFound = `Block "${blockSlug}" could not be found.`;
  if (loading) return <View name="loading" />;
  if (!block) return <View name="error" message={notFound} />;
  if (error) return <View name="error" message={error} />;

  return (
    <BlockContext.Provider value={{ block, session }}>
      <Block />
    </BlockContext.Provider>
  );
}

const ExperimentContext = createContext(null);
export const useExperimentContext = () => useContext(ExperimentContext);

export function ExperimentController() {
  useLogLifeCycle("ExperimentController");
  const { expSlug } = useParams();
  const hasShownConsent = useBoundStore((s) => s.hasShownConsent);
  const [experiment, loading] = useExperiment(expSlug!);
  const location = useLocation();
  const hasDashboard = experiment?.dashboard.length;
  const nextBlock = experiment?.nextBlock;

  // 1. Loading view while experiment data is fetched
  if (loading) return <View name="loading" />;

  // 2. Error view if no experiment data could be loaded
  const notFound = `Experiment "${expSlug}" could not be found.`;
  if (!experiment) return <View name="error" message={notFound} />;

  // 3. Redirect to consent if required (and we're not on that route)
  const isOnConsentRoute = location.pathname.includes("/consent");
  const consentRequired =
    false && !hasShownConsent && Boolean(experiment?.consent);
  if (!isOnConsentRoute && consentRequired) {
    return <Navigate to="consent" replace />;
  }

  // 4. Redirect to block if there is one (and we're not on that route)
  const isOnBlockRoute = location.pathname.includes("/block");
  if (!isOnBlockRoute && !hasDashboard && nextBlock) {
    console.log("Navigating to block!");
    return <Navigate to={`block/${nextBlock.slug}`} replace />;
  }
  console.log("rendering experiment route");
  // 5. Otherwise return child routes with experiment context
  return (
    <ExperimentContext.Provider value={experiment}>
      <Outlet />
    </ExperimentContext.Provider>
  );
}

function ConsentController() {
  const setHasShownConsent = useBoundStore((s) => s.setHasShownConsent);
  return <View name="consent" onNext={() => setHasShownConsent(true)} />;
}

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

// ———
