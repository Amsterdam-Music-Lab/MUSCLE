import React, { useState, useEffect, useCallback } from "react";
import { useExperiment, useParticipant, getNextRound } from "../../API";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { withRouter } from "react-router-dom";
import { stateNextRound } from "../../util/nextRound";

import Consent from "../Consent/Consent";
import DefaultPage from "../Page/DefaultPage";
import Explainer from "../Explainer/Explainer";
import Final from "../Final/Final";
import Loading from "../Loading/Loading";
import Playlist from "../Playlist/Playlist";
import Score from "../Score/Score";
import SongSync from "../SongSync/SongSync";
import StartSession from "../StartSession/StartSession";
import Trial from "../Trial/Trial";
import useResultHandler from "../../hooks/useResultHandler";

// Experiment handles the main experiment flow:
// - Loads the experiment and participant
// - Renders the view based on the state that is provided by the server
// - It handles sending results to the server
const Experiment = ({ match }) => {
    const startState = { view: "LOADING" };

    // Current experiment state
    const [state, setState] = useState(startState);
    const [playlist, setPlaylist] = useState(null);
    const [session, setSession] = useState(null);

    // API hooks
    const [experiment, loadingExperiment] = useExperiment(match.params.slug);
    const [participant, loadingParticipant] = useParticipant();

    const loadingText = experiment ? experiment.loading_text : "";
    const className = experiment ? experiment.class_name : "";

    // Load state, set random key
    const loadState = useCallback((state) => {
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

    // Start first_round when experiment and partipant have been loaded
    useEffect(() => {
        // Check if done loading
        if (!loadingExperiment && !loadingParticipant) {
            // Loading succeeded
            if (experiment && participant) {
                loadState(stateNextRound(experiment));
            } else {
                // Loading error
                setError("Could not load experiment");
            }
        }
    }, [
        experiment,
        loadingExperiment,
        participant,
        loadingParticipant,
        setError,
        loadState
    ]);

    // Load next round, stored in nextRound
    const onNext = async () => {
        if (state.next_round && state.next_round.length) {
            loadState(stateNextRound(state));
        } else {
            console.error("No next-round data available");
            // Fallback in case a server response/async call went wrong
            // Try to get next_round data from server again
            const round = await getNextRound({
                session: session,
                participant,
            });
            if (round) {
                loadState(round);
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
            setSession,
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
            case "SONG_SYNC":
                return <SongSync {...attrs} />;

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
        <TransitionGroup className="aha__experiment">
            <CSSTransition
                key={key}
                timeout={{ enter: 300, exit: 300 }}
                classNames={"transition"}
            >
                <DefaultPage
                    title={state.title}
                    logoClickConfirm={
                        ["FINAL_SCORE", "ERROR"].includes(key)
                            ? null
                            : "Are you sure you want to stop this experiment?"
                    }
                    className={className}
                >
                    {render(state.view)}
                </DefaultPage>
            </CSSTransition>
        </TransitionGroup>
    );
};

export default withRouter(Experiment);
