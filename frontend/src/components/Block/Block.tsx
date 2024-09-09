import { useState, useEffect, useCallback, useRef } from "react";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { useParams } from "react-router-dom";
import classNames from "classnames";

import useBoundStore from "@/util/stores";
import { getNextRound, useBlock } from "@/API";
import DefaultPage from "@/components/Page/DefaultPage";
import Explainer, { ExplainerProps } from "@/components/Explainer/Explainer";
import Final, { FinalProps } from "@/components/Final/Final";
import Loading, { LoadingProps } from "@/components/Loading/Loading";
import Playlist, { PlaylistProps } from "@/components/Playlist/Playlist";
import Score, { ScoreProps } from "@/components/Score/Score";
import Trial, { TrialProps } from "@/components/Trial/Trial";
import Info, { InfoProps } from "@/components/Info/Info";
import FloatingActionButton from "@/components/FloatingActionButton/FloatingActionButton";
import UserFeedback from "@/components/UserFeedback/UserFeedback";
import FontLoader from "@/components/FontLoader/FontLoader";
import useResultHandler from "@/hooks/useResultHandler";
import Session from "@/types/Session";
import { RedirectProps } from "../Redirect/Redirect";

interface SharedActionProps {
    title?: string;
    config?: object;
    style?: object;
}

type ActionProps = SharedActionProps &
    (
        | { view: "EXPLAINER" } & ExplainerProps
        | { view: "INFO" } & InfoProps
        | { view: "TRIAL_VIEW" } & TrialProps
        | { view: 'SCORE' } & ScoreProps
        | { view: 'FINAL' } & FinalProps
        | { view: 'PLAYLIST' } & PlaylistProps
        | { view: 'REDIRECT' } & RedirectProps
        | { view: "LOADING" } & LoadingProps
    )

// Block handles the main (experiment) block flow:
// - Loads the block and participant
// - Renders the view based on the state that is provided by the server
// - It handles sending results to the server
// - Implements participant_id as URL parameter, e.g. http://localhost:3000/bat?participant_id=johnsmith34
//   Empty URL parameter "participant_id" is the same as no URL parameter at all
const Block = () => {
    const { slug } = useParams();
    const startState = { view: "LOADING" } as ActionProps;
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
    const [state, setState] = useState<ActionProps | null>(startState);
    const [key, setKey] = useState<number>(Math.random());
    const playlist = useRef(null);

    // API hooks
    const [block, loadingBlock] = useBlock(slug);

    const loadingText = block ? block.loading_text : "";
    const className = block ? block.class_name : "";

    /** Set new state as spread of current state to force re-render */
    const updateState = useCallback((state: ActionProps) => {
        if (!state) return;

        setState({ ...state });
        setKey(Math.random());
    }, []);

    const updateActions = useCallback((currentActions: []) => {
        const newActions = currentActions;
        setActions(newActions);
        const newState = newActions.shift();
        updateState(newState);
    }, [updateState]);

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
                    image: block.image?.file,
                    url: window.location.href,
                    structuredData: {
                        "@type": "Experiment",
                    },
                });

                setBlock(block);

                if (block.session_id) {
                    setSession({ id: block.session_id });
                } else if (!block.session_id && session) {
                    setError('Session could not be created');
                }

                // Set theme
                if (block.theme) {
                    setTheme(block.theme);
                } else if (!block.theme && theme) {
                    setTheme(null);
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
            key,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (attrs.view) {
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
                return <Loading key={key} {...attrs} />;
            case "INFO":
                return <Info {...attrs} />;
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
