import { useState, useEffect, useCallback, useRef } from "react";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { useParams } from "react-router-dom";
import classNames from "classnames";

import useBoundStore from "@/util/stores";
import { getNextRound, useBlock } from "@/API";
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
import { Action } from "@/types/Action";
import { Round } from "@/types/Round";

// Block handles the main (experiment) block flow:
// - Loads the block and participant
// - Renders the view based on the state that is provided by the server
// - It handles sending results to the server
// - Implements participant_id as URL parameter, e.g. http://localhost:3000/bat?participant_id=johnsmith34
//   Empty URL parameter "participant_id" is the same as no URL parameter at all
const Block = () => {
    const { slug } = useParams();
    const startState = { view: "LOADING" } as Action;
    // Stores
    const setError = useBoundStore(state => state.setError);
    const participant = useBoundStore((state) => state.participant);
    const setSession = useBoundStore((state) => state.setSession);
    const session = useBoundStore((state) => state.session);
    const theme = useBoundStore((state) => state.theme);
    const setTheme = useBoundStore((state) => state.setTheme);
    const resetTheme = useBoundStore((state) => state.resetTheme);
    const setBlock = useBoundStore((state) => state.setBlock);
    const setCurrentAction = useBoundStore((state) => state.setCurrentAction);

    const setHeadData = useBoundStore((state) => state.setHeadData);
    const resetHeadData = useBoundStore((state) => state.resetHeadData);

    // Current block state
    const [actions, setActions] = useState<Round>([]);
    const [state, setState] = useState<Action | null>(startState);
    const [key, setKey] = useState<number>(Math.random());
    const playlist = useRef(null);

    // API hooks
    const [block, loadingBlock] = useBlock(slug!);

    const loadingText = block ? block.loading_text : "";
    const className = block ? block.class_name : "";

    /** Set new state as spread of current state to force re-render */
    const updateState = useCallback((state: Action) => {
        if (!state) return;

        setState({ ...state });
        setKey(Math.random());
    }, []);

    const updateActions = useCallback((currentActions: Round) => {
        const newActions = currentActions;
        setActions(newActions);
        const newState = newActions.shift();
        const currentAction = newState ? newState : null;
        setCurrentAction({ ...currentAction });
        updateState(newState);
    }, [updateState, setCurrentAction]);

    const continueToNextRound = async (activeSession: Session) => {
        // Try to get next_round data from server
        const round = await getNextRound({
            session: activeSession
        });
        if (round) {
            updateActions(round.next_round);
        } else {
            setError(
                "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
            );
            setCurrentAction(null);
            setState(null);
        }
    };

    // trigger next action from next_round array, or call session/next_round
    const onNext = async (doBreak = false) => {
        if (!doBreak && actions.length) {
            updateActions(actions);
        } else {
            continueToNextRound(session as Session);
        }
    };

    // Start first_round when block and partipant have been loaded
    useEffect(() => {
        // Check if done loading
        if (!loadingBlock && participant) {
            // Loading succeeded
            if (block) {
                // Set Helmet Head data
                setHeadData({
                    title: block.name,
                    description: block.description,
                    image: block.image?.file ?? "",
                    url: window.location.href,
                    structuredData: {
                        "@type": "Block",
                    },
                });

                setBlock(block);

                if (block.session_id) {
                    setSession({ id: block.session_id });
                } else if (!block.session_id && session) {
                    setError('Session could not be created');
                }

                continueToNextRound({ id: block.session_id });

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
    ]);

    useEffect(() => {
        if (block?.theme) {
            // Set theme if block has theme
            setTheme(block.theme);
        } else if (!block?.theme && theme) {
            // Reset theme if new block has no theme
            resetTheme();
        }
    }, [block, theme, setTheme, resetTheme]);

    const onResult = useResultHandler({
        session,
        participant,
    });

    // Render block state
    const render = () => {

        if (!state) {
            return (
                <div className="text-white bg-danger">
                    No valid state
                </div>
            );
        }

        // Default attributes for every view
        const attrs = {
            block: block!,
            participant: participant!,
            loadingText,
            onResult,
            onNext,
            playlist,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (attrs.view) {
            // Block views
            // -------------------------
            case "TRIAL_VIEW":
                return <Trial key={key} {...attrs} />;

            // Information & Scoring
            // -------------------------
            case "EXPLAINER":
                return <Explainer key={key} {...attrs} />;
            case "SCORE":
                return <Score key={key} {...attrs} />;
            case "FINAL":
                return <Final key={key} {...attrs} />;

            // Generic / helpers
            // -------------------------
            case "PLAYLIST":
                return <Playlist key={key} {...attrs} />;
            case "LOADING":
                return <Loading key={key} {...attrs} />;
            case "INFO":
                return <Info key={key} {...attrs} />;
            case "REDIRECT":
                window.location.replace(state.url);
                return null;

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

    const view = state?.view;

    return (<>
        <FontLoader fontUrl={theme?.heading_font_url} fontType="heading" />
        <FontLoader fontUrl={theme?.body_font_url} fontType="body" />
        <TransitionGroup
            className={classNames(
                "aha__block",
                !loadingBlock && block
                    ? "block-" + block.slug
                    : ""
            )}
            data-testid="block-wrapper"
        >
            <CSSTransition
                timeout={{ enter: 300, exit: 0 }}
                classNames={"transition"}
                unmountOnExit
            >
                {(!loadingBlock && block) || view === "ERROR" ? (
                    <DefaultPage
                        title={state.title}
                        className={className}
                    >
                        {render()}

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
                        <Loading loadingText={loadingText} />
                    </div>
                )}


            </CSSTransition>
        </TransitionGroup>
    </>

    );
};

export default Block;
