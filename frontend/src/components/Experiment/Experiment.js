import React, { useState, useRef, useEffect, useCallback } from "react";
import { MEDIA_ROOT } from "../../config";
import {
    useExperiment,
    useParticipant,
    createResult,
    getNextRound,
} from "../../API";
import * as audio from "../../util/audio";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { withRouter } from "react-router-dom";

import CompositeView from '../CompositeView/CompositeView';
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import Explainer from "../Explainer/Explainer";
import Consent from "../Consent/Consent";
import Playlist from "../Playlist/Playlist";
import StartSession from "../StartSession/StartSession";
import SongSync from "../SongSync/SongSync";
import SongBool from "../SongBool/SongBool";
import Score from "../Score/Score";
import TwoAlternativeForced from "../TwoAlternativeForced/TwoAlternativeForced";
import TwoSong from "../TwoSong/TwoSong";
import ProfileQuestion from "../ProfileQuestion/ProfileQuestion";
import ResultQuestion from "../ResultQuestion/ResultQuestion";
import FinalScore from "../FinalScore/FinalScore";
import PracticeRound from "../PracticeRound/PracticeRound";
import Final from "../Final/Final";

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
    const resultBuffer = useRef([]);

    // API hooks
    const [experiment, loadingExperiment] = useExperiment(match.params.slug);
    const [participant, loadingParticipant] = useParticipant();

    const loadingText = experiment ? experiment.loading_text : '';
    const className = experiment ? experiment.class_name : '';

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
                loadState(experiment.first_round);
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
        loadState,
    ]);

    // Session result
    const onResult = async (result) => {
        // Add data to result buffer
        resultBuffer.current.push(result || {});

        // When time_pass_break is set true on the current state and result type
        // indicates that time has passed; skip any next rounds

        const timePassBreak =
            state &&
            state.time_pass_break &&
            result.result?.type === "time_passed";

        // Check if there is another round data available
        // if so, store the result data and call onNext
        if (state && state.next_round && !timePassBreak) {
            onNext();
            return;
        }

        // Merge result data with data from resultBuffer
        // NB: result data with same properties will be overwritten by later results
        const mergedResults = Object.assign(
            {},
            ...resultBuffer.current,
            result
        );

        // Create result data
        const data = {
            session,
            participant,
            result: mergedResults,
        };

        // Optionally add section to result data
        if (mergedResults.section) {
            data.section = mergedResults.section;
        }

        // Send data to API
        const action = await createResult(data);

        // Fallback: Call onNext, try to reload round
        if (!action) {
            onNext();
            return;
        }

        // Clear resultBuffer
        resultBuffer.current = [];

        // Check for preload_section_url in (nested) action
        const preloadUrl = getSectionUrl(action);

        if (preloadUrl) {
            // 100ms for fadeout
            setTimeout(() => {
                audio.load(MEDIA_ROOT + preloadUrl);
            }, 100);
        }

        // Init new state from action
        loadState(action);
    };

    // Load next round, stored in nextRound
    const onNext = async () => {
        if (state && state.next_round) {
            loadState(state.next_round);
        } else {
            console.log("No next-round data available");
            // Fallback in case a server response/async call went wrong
            // Try to get next_round data from server again
            const round = await getNextRound({
                session: session.current,
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
            onNext,
            onResult,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (view) {
            case "LOADING":
                return <Loading {...attrs} />;
            case "ERROR":
                return <div>Error: {state.error}</div>;
            case "EXPLAINER":
                return <Explainer {...attrs} />;
            case "CONSENT":
                return <Consent {...attrs} />;
            case "PLAYLIST":
                return <Playlist {...attrs} />;
            case "START_SESSION":
                return <StartSession {...attrs} />;
            case "SONG_SYNC":
                return <SongSync {...attrs} />;
            case "SONG_BOOL":
                return <SongBool {...attrs} />;
            case "SCORE":
                return <Score {...attrs} />;
            case "TWO_ALTERNATIVE_FORCED":
                return <TwoAlternativeForced {...attrs} />;
            case "TWO_SONG":
                return <TwoSong {...attrs} />;
            case "PRACTICE_ROUND":
                return <PracticeRound {...attrs} />
            case "COMPOSITE_VIEW":
                return <CompositeView {...attrs} />
            case "PROFILE_QUESTION":
                return <ProfileQuestion {...attrs} />;
            case "RESULT_QUESTION":
                return <ResultQuestion {...attrs} />;
            case "FINAL_SCORE":
                return (
                    <FinalScore
                        {...attrs}
                        onNext={() => {
                            setSession(null);
                            loadState(experiment.first_round);
                        }}
                    />
                );
            case "FINAL":
                return (
                    <Final
                        {...attrs}
                        onNext={() => {
                            setSession(null);
                            loadState(experiment.first_round);
                        }}
                    />
                );
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

// Get a section url from given (nested) action
const getSectionUrl = (action) => {
    if (!action) {
        return "";
    }

    if (action.section && action.section.url) {
        return action.section.url;
    }

    if (action.next_round) {
        return getSectionUrl(action.next_round);
    }

    return "";
};

export default withRouter(Experiment);
