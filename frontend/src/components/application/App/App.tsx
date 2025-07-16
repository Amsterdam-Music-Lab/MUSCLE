/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import axios from "axios";

import { API_BASE_URL } from "@/config";
import { URLS } from "@/API";
import { useState } from "react";
import useBoundStore from "@/util/stores";
import useDisableRightClickOnTouchDevices from "@/hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { BaseLayout } from "@/components/layout/BaseLayout";
import AppRoutes from "./AppRoutes";
import Helmet from "./Helmet";

// i18n
import { i18n } from "@lingui/core";
import { I18nProvider } from "@lingui/react";
// import { messages as messagesEn } from "@/locales/en/messages";
// import { messages as messagesNl } from "@/locales/nl/messages";
// import { i18n } from "@lingui/core";

import { dynamicActivate, detectLocale } from "@/i18n";

// i18n.load("en", messagesEn);
// i18n.load("nl", messagesNl);
// i18n.activate("nl");

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
  const [locale, setLocale] = useState(detectLocale());

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

  useEffect(() => {
    console.log("Activating locale:", locale);
    dynamicActivate(locale);
  }, [locale]);

  return (
    <I18nProvider i18n={i18n}>
      <ThemeProvider>
        <Helmet>
          <link rel="icon" type="image/png" href="/favicon.ico" />
          <link rel="apple-touch-icon" href="/favicon.ico" />
        </Helmet>
        <BaseLayout>
          <Router>
            {/* The routes are in a separate component so that we can use
          useLocation to get smooth page transitions */}
            <AppRoutes />
          </Router>
        </BaseLayout>
      </ThemeProvider>
    </I18nProvider>
  );
}
