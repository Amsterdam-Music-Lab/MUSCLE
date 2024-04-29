import React, { useRef, useState } from "react";
import classNames from "classnames";

import { scoreIntermediateResult } from "../../API";
import useBoundStore from "@/util/stores";

import PlayCard from "./PlayCard";

export const SCORE_FEEDBACK_DISPLAY = {
    SMALL_BOTTOM_RIGHT: 'small-bottom-right',
    LARGE_TOP: 'large-top',
    HIDDEN: 'hidden',
}

const MatchingPairs = ({
    playSection,
    sections,
    playerIndex,
    showAnimation,
    finishedPlaying,
    scoreFeedbackDisplay = SCORE_FEEDBACK_DISPLAY.LARGE_TOP,
    submitResult,
    view
}) => {

    const xPosition = useRef(-1);
    const yPosition = useRef(-1);    
    const [firstCard, setFirstCard] = useState(null);
    const [secondCard, setSecondCard] = useState(null);
    const [feedbackText, setFeedbackText] = useState('Pick a card');
    const [feedbackClass, setFeedbackClass] = useState('');
    const [inBetweenTurns, setInBetweenTurns] = useState(false);
    const [score, setScore] = useState(null);
    const [total, setTotal] = useState(100);

    const columnCount = sections.length > 6 ? 4 : 3;

    const participant = useBoundStore(state => state.participant);
    const session = useBoundStore(state => state.session);
    const setError = useBoundStore(state => state.setError);

    const registerUserClicks = (posX, posY) => {
        xPosition.current = posX;
        yPosition.current = posY;
    }

    // Show (animated) feedback after second click on second card or finished playing
    const showFeedback = (score) => {

        const turnedCards = sections.filter(s => s.turned);

        // Check if this turn has finished
        if (turnedCards.length === 2) {
            // update total score & display current score
            setTotal(total + score);
            let fbclass;
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
            turnedCards[1].seen = turnedCards[1].seen = true;
            setInBetweenTurns(true);
            return;
        }
    }

    const checkMatchingPairs = async (index) => {
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
                currentCard.boardposition = parseInt(index) + 1;
                currentCard.timestamp = performance.now();                
                currentCard.response_interval_ms = Math.round(currentCard.timestamp - firstCard.timestamp);                
                // check for match
                const first_card = firstCard;
                const second_card = currentCard;
                try {
                    const scoreResponse = await scoreIntermediateResult({ session, participant, result: { first_card, second_card } });
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
                currentCard.seen = true;
                currentCard.boardposition = parseInt(index) + 1;
                currentCard.timestamp = performance.now();                
                // clear feedback text
                setFeedbackText('');
            }
        }
        return;
    };

    const finishTurn = () => {
        finishedPlaying();
        // remove matched cards from the board
        if (score === 10 || score === 20) {
            sections.find(s => s === firstCard).inactive = true;
            sections.find(s => s === secondCard).inactive = true;
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
            setScore('');
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
                    {Object.keys(sections).map((index) => (
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

const ScoreFeedback = ({
    scoreFeedbackDisplay = SCORE_FEEDBACK_DISPLAY.LARGE_TOP,
    score,
    feedbackText,
    feedbackClass,
    total,
}) => {
    return (
        <div className={
            classNames(
                "matching-pairs__score-feedback row justify-content-between",
                { "matching-pairs__score-feedback--small-bottom-right": scoreFeedbackDisplay === SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT },
            )}
        >
            <div className="col-6 align-self-start">
                <div className={classNames("matching-pairs__feedback", feedbackClass)}>
                    {score} <br/> {feedbackText}
                </div>
            </div>
            <div className="col-6 align-self-end">
                <div data-testid="score" className="matching-pairs__score">Score: <br />{total}</div>
            </div>
        </div>
    )
}

export default MatchingPairs;

