import { useRef, useState } from "react";
import classNames from "classnames";

import { scoreIntermediateResult } from "@/API";
import useBoundStore from "@/util/stores";

import PlayCard from "./PlayCard";
import { Card } from "@/types/Section";
import Session from "@/types/Session";
import Participant from "@/types/Participant";
import Overlay from "../Overlay/Overlay";
import { ScoreFeedbackDisplay } from "@/types/Playback";

export const SCORE_FEEDBACK_DISPLAY: { [key: string]: ScoreFeedbackDisplay } = {
    SMALL_BOTTOM_RIGHT: 'small-bottom-right',
    LARGE_TOP: 'large-top',
    HIDDEN: 'hidden',
}

interface MatchingPairsProps {
    playSection: (index: number) => void;
    sections: Card[];
    playerIndex: number;
    showAnimation: boolean;
    finishedPlaying: () => void;
    scoreFeedbackDisplay?: ScoreFeedbackDisplay;
    submitResult: (result: any) => void;
    tutorial?: { [key: string]: string };
    view: string;
}

type ScoreType = 'lucky_match' | 'memory_match' | 'no_match' | 'misremembered';

const MatchingPairs = ({
    playSection,
    sections: initialSections, // renamed to make it clear these are initial values
    playerIndex,
    showAnimation,
    finishedPlaying,
    scoreFeedbackDisplay = SCORE_FEEDBACK_DISPLAY.LARGE_TOP,
    submitResult,
    tutorial,
    view
}: MatchingPairsProps) => {
    const block = useBoundStore(state => state.block);
    const bonusPoints = block?.bonus_points || 0;
    const xPosition = useRef(-1);
    const yPosition = useRef(-1);
    const [firstCard, setFirstCard] = useState<Card | null>(null);
    const [secondCard, setSecondCard] = useState<Card | null>(null);
    const [feedbackText, setFeedbackText] = useState('Pick a card');
    const [feedbackClass, setFeedbackClass] = useState('');
    const [score, setScore] = useState<number | null>(null);
    const [total, setTotal] = useState(bonusPoints);
    const [startOfTurn, setStartOfTurn] = useState(performance.now());
    const [overlayWasShown, setOverlayWasShown] = useState(false);

    // New state to track card states
    const [sections, setSections] = useState(() => initialSections.map(section => ({
        ...section,
        turned: false,
        noevents: false,
        inactive: false,
        seen: false,
        matchClass: '',
        boardposition: undefined as number | undefined,
        timestamp: undefined as number | undefined
    })));

    // Check if the user is in between turns to show the hidden overlay
    const inBetweenTurns = Boolean(score && (firstCard && secondCard) || sections.filter(s => s.turned).length === 2);

    const [tutorialOverlayState, setTutorialOverlayState] = useState({
        isOpen: false,
        title: '',
        content: '',
        completed: [] as ScoreType[],
    });

    const columnCount = sections.length > 6 ? 4 : 3;

    const participant = useBoundStore(state => state.participant) as Participant;
    const session = useBoundStore(state => state.session) as Session;
    const setError = useBoundStore(state => state.setError);

    const registerUserClicks = (posX: number, posY: number) => {
        xPosition.current = posX;
        yPosition.current = posY;
    };

    const showFeedback = (score: number) => {

        setTotal(total + score);

        let fbclass: string = '';
        switch (score) {
            case 10:
                fbclass = 'fblucky';
                setFeedbackText('Lucky match');
                break;
            case 20:
                fbclass = 'fbmemory';
                setFeedbackText('Good job!');
                break;
            case 0:
                fbclass = 'fbnomatch';
                setFeedbackText('No match');
                break;
            case -10:
                fbclass = 'fbmisremembered';
                setFeedbackText('Misremembered');
                break;
            default:
                setFeedbackClass('');
                setFeedbackText('');
        }
        setFeedbackClass(fbclass);

        setSections(prev => prev.map(section => {
            if (section.turned) {
                return {
                    ...section,
                    matchClass: fbclass,
                    seen: true
                };
            }
            return section;
        }));
    };

    const showOverlay = (score: number) => {

        let scoreType: ScoreType = 'no_match';

        switch (score) {
            case 10:
                scoreType = 'lucky_match';
                break;
            case 20:
                scoreType = 'memory_match';
                break;
            case 0:
                scoreType = 'no_match';
                break;
            case -10:
                scoreType = 'misremembered';
                break;
        }

        // check if the scoreType has already been shown
        if (tutorialOverlayState.completed.includes(scoreType)) {
            return false;
        }

        // check if the scoreType is in the tutorial object
        if (!tutorial || !tutorial[scoreType]) {
            return false;
        }

        // show the overlay
        setTutorialOverlayState({
            isOpen: true,
            title: '',
            content: tutorial[scoreType],
            completed: [...tutorialOverlayState.completed, scoreType],
        });

        return true;
    }

    const getAudioLatency = () => {
        if (window.sessionStorage.getItem('audioLatency') !== null) {
            return window.sessionStorage.getItem('audioLatency');
        } else {
            return NaN;
        }
    }

    const checkMatchingPairs = async (index: number) => {
        const currentCard = sections[index];
        const turnedCards = sections.filter(s => s.turned);

        let updatedCurrentCard;

        if (turnedCards.length < 2) {
            if (turnedCards.length === 1) {
                setSections(prev => prev.map((section, i) => {
                    if (i === index) {
                        updatedCurrentCard = {
                            ...section,
                            turned: true,
                            noevents: true,
                            boardposition: index + 1,
                            timestamp: performance.now(),
                            audio_latency_ms: getAudioLatency()
                        };
                        return updatedCurrentCard;
                    }
                    return { ...section, noevents: true };
                }));

                setSecondCard(updatedCurrentCard);

                try {
                    const scoreResponse = await scoreIntermediateResult({
                        session,
                        participant,
                        result: { "start_of_turn": startOfTurn, first_card: firstCard, second_card: updatedCurrentCard, overlay_was_shown: overlayWasShown, },
                    });
                    if (!scoreResponse) {
                        throw new Error('We cannot currently proceed with the game. Try again later');
                    }
                    setScore(scoreResponse.score);
                    showFeedback(scoreResponse.score);
                    const isShowingOverlay = showOverlay(scoreResponse.score);
                    setOverlayWasShown(isShowingOverlay);
                } catch {
                    setError('We cannot currently proceed with the game. Try again later');
                    return;
                }
            } else {
                const section = sections[index];
                updatedCurrentCard = {
                    ...section,
                    turned: true,
                    noevents: true,
                    boardposition: index + 1,
                    timestamp: performance.now(),
                    audio_latency_ms: getAudioLatency()
                };
                setFirstCard(updatedCurrentCard);
                setSections(prev => prev.map((section, i) => {
                    if (i === index) {
                        return updatedCurrentCard;
                    }
                    return section;
                }));
                setFeedbackText('');
            }
        }
    };

    const finishTurn = () => {
        setStartOfTurn(performance.now());
        finishedPlaying();

        const updatedSections = sections.map(section => {
            if (score === 10 || score === 20) {
                if (section.id === firstCard?.id || section.id === secondCard?.id) {
                    section.inactive = true;
                }
            }
            return {
                ...section,
                turned: false,
                noevents: false,
                matchClass: ''
            };
        });

        setSections(updatedSections);

        setFirstCard(null);
        setSecondCard(null);
        setScore(null);

        // Check if the board is empty
        if (updatedSections.filter(s => s.inactive).length === sections.length) {
            submitResult({});
            setFeedbackText('');
        } else {
            setFeedbackText('Pick a card');
            setScore(null);
            setFeedbackClass('');
        }
    }

    return (
        <div className="aha__matching-pairs">
            <div>
                {scoreFeedbackDisplay !== SCORE_FEEDBACK_DISPLAY.HIDDEN &&
                    <ScoreFeedback
                        score={score}
                        total={total}
                        feedbackClass={feedbackClass}
                        feedbackText={feedbackText}
                        scoreFeedbackDisplay={scoreFeedbackDisplay}
                    />}

                <div className={classNames("playing-board", columnCount === 3 && "playing-board--three-columns")}>
                    {sections.map((_section, index) => (
                        <PlayCard
                            key={index}
                            onClick={() => {
                                playSection(index);
                                checkMatchingPairs(index);
                            }}
                            registerUserClicks={registerUserClicks}
                            playing={playerIndex === index}
                            section={sections[index]}
                            showAnimation={showAnimation}
                            view={view}
                        />
                    )
                    )}
                </div>
                <div
                    className="matching-pairs__overlay"
                    onClick={finishTurn}
                    style={{ display: inBetweenTurns ? 'block' : 'none' }}
                    data-testid="overlay"
                ></div>
            </div>
            <Overlay
                isOpen={tutorialOverlayState.isOpen}
                title={tutorialOverlayState.title}
                content={tutorialOverlayState.content}
                onClose={() => {
                    finishTurn();
                    setTutorialOverlayState({ ...tutorialOverlayState, isOpen: false });
                }}
            />
        </div>

    )
}

interface ScoreFeedbackProps {
    scoreFeedbackDisplay?: string;
    score: number | null;
    feedbackText: string;
    feedbackClass: string;
    total: number;
}

const ScoreFeedback = ({
    scoreFeedbackDisplay = SCORE_FEEDBACK_DISPLAY.LARGE_TOP,
    score,
    feedbackText,
    feedbackClass,
    total,
}: ScoreFeedbackProps) => {
    return (
        <div className={
            classNames(
                "matching-pairs__score-feedback row justify-content-between",
                { "matching-pairs__score-feedback--small-bottom-right": scoreFeedbackDisplay === SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT },
            )}
        >
            <div className="col-6 align-self-start">
                <div className={classNames("matching-pairs__feedback", feedbackClass)}>
                    {score} <br /> {feedbackText}
                </div>
            </div>
            <div className="col-6 align-self-end">
                <div data-testid="score" className="matching-pairs__score">Score: <br />{total}</div>
            </div>
        </div>
    )
}

export default MatchingPairs;
