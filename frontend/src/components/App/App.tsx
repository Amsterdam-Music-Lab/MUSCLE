import { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import axios from "axios";

import { API_BASE_URL, EXPERIMENT_SLUG, URLS } from "@/config";
import { URLS as API_URLS } from "@/API";
import useBoundStore from "@/util/stores";
import Experiment from "@/components/Experiment/Experiment";
import StoreProfile from "@/components/StoreProfile/StoreProfile";
import useDisableRightClickOnTouchDevices from "@/hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { Redirect, InternalRedirect, Reload, ConditionalRender } from "@/components/utils";

import { ThemeProvider } from "@/theme/ThemeProvider";
import { Loading, Landing, Profile } from "@/components/views";
import { Block, Background, Helmet } from "@/components/application";

// TODO ideally load or populate this from the backend
import frontendConfig from "@/config/frontend";

// App is the root component of our application
const App = () => {
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
    return <p className="aha__error">Error: {error}</p>;
  }

  return (
    <ThemeProvider>
      <Helmet />
      <Router className="aha__app">
        <ConditionalRender
          condition={!!participant}
          fallback={<Loading />}
        >
          <Routes>
            {/* Request reload for given participant */}
            <Route path={URLS.reloadParticipant} element={<Reload />} />

            {/* Default experiment */}
            <Route
              path="/"
              element={
                frontendConfig.showLanding ? (
                  <Landing
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
            <Route path={URLS.profile} element={<Profile />} />

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
            <Route path={URLS.storeProfile} element={StoreProfile} />
          </Routes>
        </ConditionalRender>
      </Router>

      <Background />
    </ThemeProvider>
  );
};

export default App;
