import { useEffect } from "react";
import {
    BrowserRouter as Router,
    Route,
    Routes,
} from "react-router-dom";
import axios from "axios";

import { API_BASE_URL, EXPERIMENT_SLUG, URLS } from "@/config";
import { URLS as API_URLS } from "../../API";
import useBoundStore from "../../util/stores";
import Block from "../Block/Block";
import Experiment from "../Experiment/Experiment";
import ExperimentAbout from "../Experiment/ExperimentAbout/ExperimentAbout";
import LoaderContainer from "../LoaderContainer/LoaderContainer";
import ConditionalRender from "../ConditionalRender/ConditionalRender";
import Profile from "../Profile/Profile";
import Reload from "../Reload/Reload";
import StoreProfile from "../StoreProfile/StoreProfile";
import useDisableRightClickOnTouchDevices from "../../hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { InternalRedirect } from "../InternalRedirect/InternalRedirect";
import Helmet from "@/components/Helmet/Helmet";
import Redirect from "@/components/Redirect/Redirect";

// App is the root component of our application
const App = () => {
    const error = useBoundStore(state => state.error);
    const setError = useBoundStore(state => state.setError);
    const participant = useBoundStore((state) => state.participant);
    const setParticipant = useBoundStore((state) => state.setParticipant);
    const setParticipantLoading = useBoundStore((state) => state.setParticipantLoading);
    const queryParams = window.location.search;

    useDisableRightClickOnTouchDevices();
    useDisableIOSPinchZoomOnTouchDevices();

    useEffect(() => {
        const urlParams = new URLSearchParams(queryParams);
        const participantId = urlParams.get('participant_id');
        let participantQueryParams = '';
        if (participantId) {
            participantQueryParams = `?participant_id=${participantId}`;
        }
        try {
            axios.get(API_BASE_URL + API_URLS.participant.current + participantQueryParams).then(response => {
                setParticipant(response.data);
            });
        } catch (err) {
            console.error(err);
            setError('Could not load participant', err);
        } finally {
            setParticipantLoading(false);
        }
    }, [setError, queryParams, setParticipant])

    if (error) {
        return <p className="aha__error">Error: {error}</p>;
    }

    return (
        <>
            <Helmet />
            <Router className="aha__app">
                <ConditionalRender condition={!!participant} fallback={<LoaderContainer />}>
                    <Routes>
                        {/* Request reload for given participant */}
                        <Route path={URLS.reloadParticipant} element={<Reload />} />

                        {/* Default experiment */}
                        <Route
                            path="/"
                            element={<Redirect to={URLS.experiment.replace(":slug", EXPERIMENT_SLUG)} />}
                        />

                        {/* Profile */}
                        <Route path={URLS.profile} element={<Profile />} />

                        {/* Internal redirect */}
                        <Route path={URLS.internalRedirect} element={<InternalRedirect />} />

                        {/* Block */}
                        <Route path={URLS.block} element={<Block />} />

                        {/* Experiment */}
                        <Route path={URLS.experiment} element={<Experiment />} />

                        {/* ExperimentAbout */}
                        <Route path={URLS.experiment} element={<ExperimentAbout />} />

                        {/* Store profile */}
                        <Route
                            path={URLS.storeProfile}
                            element={StoreProfile}
                        />
                    </Routes>
                </ConditionalRender>
            </Router >
        </>
    );
};

export default App;
