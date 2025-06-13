/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect } from "react";
import { BrowserRouter, createBrowserRouter } from "react-router-dom";
import axios from "axios";

import { API_BASE_URL } from "@/config";
import { URLS } from "@/API";
import useBoundStore from "@/util/stores";
import useDisableRightClickOnTouchDevices from "@/hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { BaseLayout } from "@/components/layout/BaseLayout";
import AppRoutes from "./AppRoutes";
import Helmet from "./Helmet";

// TODO ideally load or populate this from the backend
import frontendConfig from "@/config/frontend";

/**
 * The root component of the application
 *
 * Note that this component also sets the participant_id as URL parameter,
 * e.g. http://localhost:3000/bat?participant_id=johnsmith34
 * Empty URL parameter "participant_id" is the same as no URL parameter at all
 */
export default function App() {
  const setError = useBoundStore((state) => state.setError);
  const setParticipant = useBoundStore((state) => state.setParticipant);
  const setParticipantLoading = useBoundStore((s) => s.setParticipantLoading);

  // Disable gestures on touch devices
  useDisableRightClickOnTouchDevices();
  useDisableIOSPinchZoomOnTouchDevices();

  // Load the participant using the participant_id query param
  const queryParams = window.location.search;
  useEffect(() => {
    try {
      const urlParams = new URLSearchParams(queryParams);
      const participantId = urlParams.get("participant_id");
      let url = `${API_BASE_URL}${URLS.participant.current}`;
      if (participantId) url = `${url}?participant_id=${participantId}`;
      axios.get(url).then((response) => setParticipant(response.data));
    } catch (err) {
      console.error(err);
      setError("Could not load participant", err);
    } finally {
      setParticipantLoading(false);
    }
  }, [setError, queryParams, setParticipant, setParticipantLoading]);

  return (
    <ThemeProvider>
      <Helmet />
      <BaseLayout>
        <BrowserRouter>
          {/* The routes are in a separate component so that we can use
          useLocation to get smooth page transitions */}
          <AppRoutes
            showLanding={frontendConfig.showLanding}
            landingPlugins={frontendConfig?.landing?.plugins}
          />
        </BrowserRouter>
      </BaseLayout>
    </ThemeProvider>
  );
}
