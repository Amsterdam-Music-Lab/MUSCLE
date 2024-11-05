import { useRef, useState } from "react";
import classNames from "classnames";

import { scoreIntermediateResult } from "../../API";
import useBoundStore from "@/util/stores";

import PlayCard from "./PlayCard";
import { Card } from "@/types/Section";
import Session from "@/types/Session";
import Participant from "@/types/Participant";

export const SCORE_FEEDBACK_DISPLAY = {
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
    scoreFeedbackDisplay?: string;
    submitResult: (result: any) => void;
    view: string;
}

const MatchingPairs = ({
    playSection,
    /** FIXME: technically these are Sections, but we're adding some extra properties to them in a hacky way,
    // which should be fixed in the future */
    sections,
    playerIndex,
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
    const [inBetweenTurns, setInBetweenTurns] = useState(false);
    const [score, setScore] = useState<number | null>(null);
    const [total, setTotal] = useState(bonusPoints);

    const columnCount = sections.length > 6 ? 4 : 3;

    const participant = useBoundStore(state => state.participant) as Participant;
    const session = useBoundStore(state => state.session) as Session;
    const setError = useBoundStore(state => state.setError);

    const registerUserClicks = (posX: number, posY: number) => {
        xPosition.current = posX;
        yPosition.current = posY;
    }

    let startOfTurn = performance.now();

    // Show (animated) feedback after second click on second card or finished playing
    const showFeedback = (score: number) => {

        const turnedCards = sections.filter(s => s.turned);

        // Check if this turn has finished
        if (turnedCards.length === 2) {
            // update total score & display current score
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
            turnedCards[0].matchClass = turnedCards[1].matchClass = fbclass;
            turnedCards[0].seen = turnedCards[1].seen = true;
            setInBetweenTurns(true);
            return;
        }
    }

    const checkMatchingPairs = async (index: number) => {
        const currentCard = sections[index];
        const turnedCards = sections.filter(s => s.turned);
        if (turnedCards.length < 2) {
            if (turnedCards.length === 1) {

                // This is the second card to be turned
                currentCard.turned = true;
                setSecondCard(currentCard);

                // set no mouse events for all but current
                sections.forEach(section => section.noevents = true);
                currentCard.noevents = true;
                currentCard.boardposition = index + 1;
                currentCard.timestamp = performance.now();

                const firstCardTimestamp = firstCard?.timestamp ?? 0;
                currentCard.response_interval_ms = Math.round(currentCard.timestamp - firstCardTimestamp);

                // check for match
                const first_card = firstCard;
                const second_card = currentCard;
                try {
                    const scoreResponse = await scoreIntermediateResult({ session, participant, result: { first_card, second_card } });
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
                // first click of the turn
                setFirstCard(currentCard);
                // turn first card, disable events
                currentCard.turned = true;
                currentCard.noevents = true;
                currentCard.boardposition = index + 1;
                currentCard.timestamp = performance.now();
                currentCard.start_of_turn = startOfTurn;
                // reset response interval in case this card has a value from a previous turn
                currentCard.response_interval_ms = '';
                // clear feedback text
                setFeedbackText('');
            }
        }
        return;
    };

    const finishTurn = () => {
        startOfTurn = performance.now();
        finishedPlaying();
        // remove matched cards from the board
        if (score === 10 || score === 20) {
            sections.find(s => s === firstCard)!.inactive = true;
            sections.find(s => s === secondCard)!.inactive = true;
        }
        setFirstCard(null);
        setSecondCard(null)
        setScore(null);
        // Turn all cards back and enable events
        sections.forEach(section => section.turned = false);
        sections.forEach(section => section.noevents = false);
        sections.forEach(section => section.matchClass = '');
        // Check if the board is empty
        if (sections.filter(s => s.inactive).length === sections.length) {
            // submit empty result, which will trigger a call to `next_round`
            submitResult({});
            setFeedbackText('');
        } else {
            setFeedbackText('Pick a card');
            setScore(null);
            setFeedbackClass('');
        }
        setInBetweenTurns(false);
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
                            onFinish={showFeedback}
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
