import React, { useState, useEffect, useCallback, useRef } from "react";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { useParams } from "react-router-dom";
import classNames from "classnames";

import useBoundStore from "@/util/stores";
import { createSession, getNextRound, useBlock } from "@/API";
import Consent from "@/components/Consent/Consent";
import DefaultPage from "@/components/Page/DefaultPage";
import Explainer from "@/components/Explainer/Explainer";
import Final from "@/components/Final/Final";
import Loading from "@/components/Loading/Loading";
import Playlist from "@/components/Playlist/Playlist";
import Score from "@/components/Score/Score";
import Trial from "@/components/Trial/Trial";
import Info from "@/components/Info/Info";
import FloatingActionButton from "@/components/FloatingActionButton/FloatingActionButton";
import UserFeedback from "@/components/UserFeedback/UserFeedback";
import FontLoader from "@/components/FontLoader/FontLoader";
import useResultHandler from "@/hooks/useResultHandler";
import Session from "@/types/Session";

// Block handles the main (experiment) block flow:
// - Loads the block and participant
// - Renders the view based on the state that is provided by the server
// - It handles sending results to the server
// - Implements participant_id as URL parameter, e.g. http://localhost:3000/bat?participant_id=johnsmith34
//   Empty URL parameter "participant_id" is the same as no URL parameter at all
const Block = () => {
    const { slug } = useParams();
    const startState = { view: "LOADING" };
    // Stores
    const setError = useBoundStore(state => state.setError);
    const participant = useBoundStore((state) => state.participant);
    const setSession = useBoundStore((state) => state.setSession);
    const session = useBoundStore((state) => state.session);
    const theme = useBoundStore((state) => state.theme);
    const setTheme = useBoundStore((state) => state.setTheme);
    const setBlock = useBoundStore((state) => state.setBlock);

    const setHeadData = useBoundStore((state) => state.setHeadData);
    const resetHeadData = useBoundStore((state) => state.resetHeadData);

    // Current block state
    const [actions, setActions] = useState([]);
    const [state, setState] = useState(startState);
    const playlist = useRef(null);

    // API hooks
    const [block, loadingBlock] = useBlock(slug);

    const loadingText = block ? block.loading_text : "";
    const className = block ? block.class_name : "";

    // set random key before setting state
    // this will assure that `state` will be recognized as an updated object
    const updateState = useCallback((state) => {
        if (!state) return;
        state.key = Math.random();
        setState(state);
    }, []);

    const updateActions = useCallback((currentActions) => {
        const newActions = currentActions;
        setActions(newActions);
        const newState = newActions.shift();
        updateState(newState);
    }, [updateState]);

    /**
     * @deprecated
     */
    const checkSession = async (): Promise<Session | void> => {
        if (session) {
            return session;
        }

        if (block?.session_id) {
            const newSession = { id: block.session_id };
            setSession(newSession);
            return newSession;
        }
    };

    const continueToNextRound = async () => {
        const thisSession = await checkSession();
        // Try to get next_round data from server
        const round = await getNextRound({
            session: thisSession
        });
        if (round) {
            updateActions(round.next_round);
        } else {
            setError(
                "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
            );
            setState(undefined);
        }
    };

    // trigger next action from next_round array, or call session/next_round
    const onNext = async (doBreak = false) => {
        if (!doBreak && actions.length) {
            updateActions(actions);
        } else {
            continueToNextRound();
        }
    };

    // Start first_round when block and partipant have been loaded
    useEffect(() => {
        // Check if done loading
        if (!loadingBlock && participant) {
            // Loading succeeded
            if (block) {
                setSession(null);
                // Set Helmet Head data
                setHeadData({
                    title: block.name,
                    description: block.description,
                    image: block.image?.file,
                    url: window.location.href,
                    structuredData: {
                        "@type": "Experiment",
                    },
                });

                setBlock(block);

                if (block.session_id) {
                    setSession({ id: block.session_id });
                }

                // Set theme
                if (block.theme) {
                    setTheme(block.theme);
                } else if (!block.theme && theme) {
                    setTheme(null);
                }

                if (block.next_round.length) {
                    updateActions([...block.next_round]);
                } else {
                    setError("The first_round array from the ruleset is empty")
                }
            } else {
                // Loading error
                setError("Could not load block");
            }
        }

        // Cleanup
        return () => {
            resetHeadData();
        };
    }, [
        block,
        loadingBlock,
        participant,
        setError,
        updateActions,
        theme,
        setTheme,
    ]);

    const onResult = useResultHandler({
        session,
        participant,
        onNext,
        state,
    });

    // Render block state
    const render = (view) => {
        // Default attributes for every view
        const attrs = {
            block,
            participant,
            loadingText,
            onResult,
            onNext,
            playlist,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (view) {
            // Block views
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
            case "LOADING":
                return <Loading {...attrs} />;
            case "CONSENT":
                return <Consent {...attrs} />;
            case "INFO":
                return <Info {...attrs} />;
            case "REDIRECT":
                return window.location.replace(state.url);

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
        setError('No valid state');
    }

    const view = state.view;

    return (<>
        <FontLoader fontUrl={theme?.heading_font_url} fontType="heading" />
        <FontLoader fontUrl={theme?.body_font_url} fontType="body" />
        <TransitionGroup
            className={classNames(
                "aha__block",
                !loadingBlock && block
                    ? "experiment-" + block.slug
                    : ""
            )}
            data-testid="experiment-wrapper"
        >
            <CSSTransition
                key={view}
                timeout={{ enter: 300, exit: 0 }}
                classNames={"transition"}
                unmountOnExit
            >
                {(!loadingBlock && block) || view === "ERROR" ? (
                    <DefaultPage
                        title={state.title}
                        logoClickConfirm={
                            ["FINAL", "ERROR"].includes(view) ||
                                // Info pages at end of block
                                (view === "INFO" &&
                                    (!state.next_round || !state.next_round.length))
                                ? null
                                : "Are you sure you want to stop this experiment?"
                        }
                        className={className}
                    >
                        {render(view)}

                        {block?.feedback_info?.show_float_button && (
                            <FloatingActionButton>
                                <UserFeedback
                                    blockSlug={block.slug}
                                    participant={participant}
                                    feedbackInfo={block.feedback_info}
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
    </>

    );
};

export default Block;
