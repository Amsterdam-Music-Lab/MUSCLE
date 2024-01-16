import React, { useState, useEffect, useCallback, useRef } from "react";
import { useExperiment, getNextRound } from "../../API";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { withRouter } from "react-router-dom";
import classNames from "classnames";

import { useParticipantStore, useSessionStore } from "../../util/stores";
import { createSession } from "../../API.js";
import Consent from "../Consent/Consent";
import DefaultPage from "../Page/DefaultPage";
import ToontjeHoger from "../ToontjeHoger/ToontjeHoger";
import Explainer from "../Explainer/Explainer";
import Final from "../Final/Final";
import Loading from "../Loading/Loading";
import Playlist from "../Playlist/Playlist";
import Score from "../Score/Score";
import StartSession from "../StartSession/StartSession";
import Trial from "../Trial/Trial";
import useResultHandler from "../../hooks/useResultHandler";
import Info from "../Info/Info";
import FloatingActionButton from "components/FloatingActionButton/FloatingActionButton";
import UserFeedback from "components/UserFeedback/UserFeedback";


// Experiment handles the main experiment flow:
// - Loads the experiment and participant
// - Renders the view based on the state that is provided by the server
// - It handles sending results to the server
// - Implements participant_id as URL parameter, e.g. http://localhost:3000/bat?participant_id=johnsmith34
//   Empty URL parameter "participant_id" is the same as no URL parameter at all
const Experiment = ({ match }) => {
    const startState = { view: "LOADING" };
    const participant = useParticipantStore((state) => state.participant);
    const setSessionStore = useSessionStore((state) => state.setSession);

    // Current experiment state
    const [state, setState] = useState(startState);
    const [playlist, setPlaylist] = useState(null);
    const [actions, setActions] = useState([]);
    const [session, setSession] = useState(null);

    // API hooks
    const [experiment, loadingExperiment] = useExperiment(match.params.slug);

    const loadingText = experiment ? experiment.loading_text : "";
    const className = experiment ? experiment.class_name : "";

    // Load state, set random key
    const loadState = useCallback((state) => {
        if (!state) return;
        state.key = Math.random();
        setState(state);
    }, []);

    // Create error view
    const setError = useCallback(
        (error) => {
            loadState({ view: "ERROR", error });
        },
        [loadState]
    );

    const updateActions = useCallback((currentActions) => {
        let newActions = currentActions;
        const newState = newActions.shift();
        loadState(newState);
        setActions(newActions);
    }, [loadState, setActions]);

    useEffect(() => {
        if (!experiment || !participant || !playlist) {
            return;
        }
        try { 
            createSession({
                experiment,
                participant,
                playlist,
            }).then(data => {
                setSession(data.session);
                setSessionStore(data.session);
            });
        } catch (err) {
            setError(`Could not create a session: ${err}`)
        }
    }, [experiment, participant, playlist, setError, setSessionStore])

    // Start first_round when experiment and partipant have been loaded
    useEffect(() => {
        // Check if done loading
        if (!loadingExperiment && participant) {
            // Loading succeeded
            if (experiment) {
                updateActions(experiment.next_round);
            } else {
                // Loading error
                setError("Could not load experiment");
            }
        }
    }, [
        experiment,
        loadingExperiment,
        participant,
        setError,
        updateActions
    ]);

    // trigger next action from next_round array, or call session/next_round
    const onNext = async (doBreak) => {
        if (!doBreak && actions.length) {
            updateActions(actions);
        } else {
            // Try to get next_round data from server
            const round = await getNextRound({
                session: session
            });
            if (round) {
                updateActions(round.next_round);
            } else {
                setError(
                    "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
                );
            }
        }
    };

    const onResult = useResultHandler({
        session,
        participant,
        loadState,
        onNext,
        state,
    });

    // Render experiment state
    const render = (view) => {
        // Default attributes for every view
        const attrs = {
            experiment,
            session,
            participant,
            loadState,
            playlist,
            loadingText,
            setPlaylist,
            setError,
            onResult,
            onNext,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (view) {
            // Experiment views
            // -------------------------
            case "TRIAL_VIEW":
                return <Trial {...attrs} />;

            // Information & Scoring
            // -------------------------
            case "EXPLAINER":
                return <Explainer {...attrs} />;
            case "SCORE":
                return <Score {...attrs} />;
            case "FINAL":
                return <Final {...attrs} />;

            // Generic / helpers
            // -------------------------
            case "PLAYLIST":
                return <Playlist {...attrs} />;
            case "START_SESSION":
                return <StartSession {...attrs} />;
            case "LOADING":
                return <Loading {...attrs} />;
            case "ERROR":
                return <div>Error: {state.error}</div>;
            case "CONSENT":
                return <Consent {...attrs} />;
            case "INFO":
                return <Info {...attrs} />;
            case "REDIRECT":
                return window.location.replace(state.url);

            // Specials
            // -------------------------
            case "TOONTJEHOGER":
                return <ToontjeHoger {...attrs} />;

            default:
                return (
                    <div className="text-white bg-danger">
                        Unknown view: {view}
                    </div>
                );
        }
    };

    // Fail safe
    if (!state) {
        return <div>Error: No valid state</div>;
    }

    let key = state.view;

    // Force view refresh for consecutive questions
    if (state.view === "QUESTION") {
        key = state.question.key;
    }
    return (
        <TransitionGroup
            className={classNames(
                "aha__experiment",
                !loadingExperiment && experiment
                    ? "experiment-" + experiment.slug
                    : ""
            )}
        >
            <CSSTransition
                key={key}
                timeout={{ enter: 300, exit: 0 }}
                classNames={"transition"}
                unmountOnExit
            >
                {(!loadingExperiment && experiment) || key === "ERROR" ? (
                    <DefaultPage
                        title={state.title}
                        logoClickConfirm={
                            ["FINAL", "ERROR", "TOONTJEHOGER"].includes(key) ||
                                // Info pages at end of experiment
                                (key === "INFO" &&
                                    (!state.next_round || !state.next_round.length))
                                ? null
                                : "Are you sure you want to stop this experiment?"
                        }
                        className={className}
                    >
                        {render(state.view)}

                        {experiment?.feedback_info?.show_float_button && (
                            <FloatingActionButton>
                                <UserFeedback
                                    experimentSlug={experiment.slug}
                                    participant={participant}
                                    feedbackInfo={experiment.feedback_info}
                                    inline={false} />
                            </FloatingActionButton>
                        )}
                    </DefaultPage>
                ) : (
                    <div className="loader-container">
                        <Loading />
                    </div>
                )}


            </CSSTransition>
        </TransitionGroup>
    );
};

export default withRouter(Experiment);
