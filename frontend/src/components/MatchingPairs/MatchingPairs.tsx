import { useRef, useState } from "react";
import classNames from "classnames";

import { scoreIntermediateResult } from "@/API";
import useBoundStore from "@/util/stores";
import { getAudioLatency } from "@/util/time";

import PlayCard from "./PlayCard";
import { Card } from "@/types/Section";
import Session from "@/types/Session";
import Participant from "@/types/Participant";
import { ScoreFeedbackDisplay } from "@/types/Playback";

export const SCORE_FEEDBACK_DISPLAY: { [key: string]: ScoreFeedbackDisplay } = {
    SMALL_BOTTOM_RIGHT: 'small-bottom-right',
    LARGE_TOP: 'large-top',
    HIDDEN: 'hidden',
}

interface MatchingPairsProps {
    playSection: (section: Card) => void;
    sections: Card[];
    showAnimation: boolean;
    finishedPlaying: () => void;
    scoreFeedbackDisplay?: ScoreFeedbackDisplay;
    submitResult: (result: any) => void;
    view: string;
}

const MatchingPairs = ({
    playSection,
    sections: initialSections, // renamed to make it clear these are initial values
    showAnimation,
    finishedPlaying,
    scoreFeedbackDisplay = SCORE_FEEDBACK_DISPLAY.LARGE_TOP,
    submitResult,
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
                };
            }
            return section;
        }));
    };

    const checkMatchingPairs = async (index: number) => {

        const turnedCards = sections.filter(s => s.turned);
        const section = sections[index];

        const updatedCurrentCard = {
            ...section,
            turned: true,
            noevents: true,
            boardposition: index + 1,
            timestamp: performance.now(),
            audio_latency_ms: getAudioLatency()
        }

        if (turnedCards.length < 2) {
            if (turnedCards.length === 1) {
                setSecondCard(updatedCurrentCard);
                setSections(prev => prev.map((section, i) => {
                    if (i === index) {
                        return { ...updatedCurrentCard, seen: true}
                    }
                    return { ...section, noevents: true };
                }));

                try {
                    const scoreResponse = await scoreIntermediateResult({
                        session,
                        participant,
                        result: { "start_of_turn": startOfTurn, first_card: firstCard, second_card: updatedCurrentCard },
                    });
                    if (!scoreResponse) {
                        throw new Error('We cannot currently proceed with the game. Try again later');
                    }
                    setScore(scoreResponse.score);
                    showFeedback(scoreResponse.score);
                } catch {
                    setError('We cannot currently proceed with the game. Try again later');
                    return;
                }
            } else {
                setFirstCard(updatedCurrentCard);
                setSections(prev => prev.map((section, i) => {
                    if (i === index) {
                        return {...updatedCurrentCard, seen: true};
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
                    {sections.map((section, index) => (
                        <PlayCard
                            key={index}
                            onClick={() => {
                                playSection(section);
                                checkMatchingPairs(index);
                            }}
                            registerUserClicks={registerUserClicks}
                            section={section}
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
