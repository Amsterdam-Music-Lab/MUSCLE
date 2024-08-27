import { useState, useEffect, useCallback, useRef } from "react";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { useParams } from "react-router-dom";
import classNames from "classnames";

import useBoundStore from "@/util/stores";
import { getNextRound, useBlock } from "@/API";
import Consent from "@/components/Consent/Consent";
import DefaultPage from "@/components/Page/DefaultPage";
import Explainer from "@/components/Explainer/Explainer";
import Final from "@/components/Final/Final";
import Loading from "@/components/Loading/Loading";
import Playlist from "@/components/Playlist/Playlist";
import Score from "@/components/Score/Score";
import Trial, { IFeedbackForm } from "@/components/Trial/Trial";
import Info from "@/components/Info/Info";
import FloatingActionButton from "@/components/FloatingActionButton/FloatingActionButton";
import UserFeedback from "@/components/UserFeedback/UserFeedback";
import FontLoader from "@/components/FontLoader/FontLoader";
import useResultHandler from "@/hooks/useResultHandler";
import Session from "@/types/Session";
import { PlaybackArgs, PlaybackView } from "@/types/Playback";
import { FeedbackInfo, Step } from "@/types/Block";
import { TrialConfig } from "@/types/Trial";
import Social from "@/types/Social";

type BlockView = PlaybackView | "TRIAL_VIEW" | "EXPLAINER" | "SCORE" | "FINAL" | "PLAYLIST" | "LOADING" | "CONSENT" | "INFO" | "REDIRECT";

interface ActionProps {

    view: BlockView;
    title?: string;
    url?: string;
    next_round?: any[];

    // Some views require additional data
    button_label?: string;
    instruction?: string;
    timer?: number;
    steps: Step[];
    body?: string;
    html?: string;
    feedback_form?: IFeedbackForm;
    playback?: PlaybackArgs;
    config?: TrialConfig;

    // TODO: Think about how to properly handle the typing of different views

    // Score-related
    score?: number;
    score_message?: string;
    texts?: {
        score: string;
        next: string;
        listen_explainer: string;
    };
    feedback?: string;
    icon?: string;

    // Final related
    feedback_info?: FeedbackInfo;
    rank?: string;
    button?: {
        text: string;
        link: string;
    };
    final_text?: string | TrustedHTML;
    show_participant_link?: boolean;
    participant_id_only?: boolean;
    show_profile_link?: boolean;
    action_texts?: {
        all_experiments: string;
        profile: string;
        play_again: string;
    }
    points?: string;
    social?: Social;
    logo?: {
        image: string;
        link: string;
    };

    // Consent related
    text?: string;
    confirm?: string;
    deny?: string;
}


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
    const [key, setKey] = useState(null);
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
            setState(null);
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
    const render = (view: BlockView) => {
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
                return <Trial key={key} {...attrs} />;

            // Information & Scoring
            // -------------------------
            case "EXPLAINER":
                return <Explainer key={key} {...attrs}/>;
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
            case "CONSENT":
                return <Consent key={key} {...attrs} />;
            case "INFO":
                return <Info key={key} {...attrs} />;
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

    const view = state?.view;

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
