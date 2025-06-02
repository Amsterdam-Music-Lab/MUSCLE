/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import axios from "axios";

import { API_BASE_URL, EXPERIMENT_SLUG, URLS } from "@/config";
import { URLS as API_URLS } from "@/API";
import useBoundStore from "@/util/stores";
import useDisableRightClickOnTouchDevices from "@/hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { Redirect, InternalRedirect, Reload } from "@/components/utils";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { Block, Experiment, View } from "../";
import Helmet from "./Helmet";

// TODO ideally load or populate this from the backend
import frontendConfig from "@/config/frontend";
import { BaseLayout } from "@/components/layout/BaseLayout";

// App is the root component of our application
export default function App() {
  const error = useBoundStore((state) => state.error);
  const setError = useBoundStore((state) => state.setError);
  const participant = useBoundStore((state) => state.participant);
  const setParticipant = useBoundStore((state) => state.setParticipant);
  const setParticipantLoading = useBoundStore(
    (state) => state.setParticipantLoading
  );
  const queryParams = window.location.search;

  useDisableRightClickOnTouchDevices();
  useDisableIOSPinchZoomOnTouchDevices();

  useEffect(() => {
    const urlParams = new URLSearchParams(queryParams);
    const participantId = urlParams.get("participant_id");
    let participantQueryParams = "";
    if (participantId) {
      participantQueryParams = `?participant_id=${participantId}`;
    }
    try {
      axios
        .get(
          API_BASE_URL + API_URLS.participant.current + participantQueryParams
        )
        .then((response) => {
          setParticipant(response.data);
        });
    } catch (err) {
      console.error(err);
      setError("Could not load participant", err);
    } finally {
      setParticipantLoading(false);
    }
  }, [setError, queryParams, setParticipant, setParticipantLoading]);

  if (error) {
    return <View name="error" title="An error occured" message={error} />;
  }

  return (
    <ThemeProvider>
      <Helmet />
      <BaseLayout>
        <Router>
          {!!participant ? (
            <Routes>
              {/* Request reload for given participant */}
              <Route path={URLS.reloadParticipant} element={<Reload />} />

              {/* Default experiment */}
              <Route
                path="/"
                element={
                  frontendConfig.showLanding ? (
                    <View
                      name="landing"
                      experimentUrl={URLS.experiment.replace(
                        ":slug",
                        EXPERIMENT_SLUG
                      )}
                      plugins={frontendConfig.landing.plugins}
                    />
                  ) : (
                    <Redirect
                      to={URLS.experiment.replace(":slug", EXPERIMENT_SLUG)}
                    />
                  )
                }
              />

              {/* Profile */}
              <Route path={URLS.profile} element={<View name="profile" />} />

              {/* Internal redirect */}
              <Route
                path={URLS.internalRedirect}
                element={<InternalRedirect />}
              />

              {/* Block */}
              <Route path={URLS.block} element={<Block />} />

              {/* Experiment */}
              <Route path={URLS.experiment} element={<Experiment />} />

              {/* Store profile */}
              <Route
                path={URLS.storeProfile}
                element={<View name="storeProfile" />}
              />
            </Routes>
          ) : (
            <View name="loading" />
          )}
        </Router>
      </BaseLayout>
    </ThemeProvider>
  );
}
