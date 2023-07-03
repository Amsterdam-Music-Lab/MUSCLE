import React, {useRef, useState} from "react";
import classNames from "classnames";

import PlayCard from "../PlayButton/PlayCard";

const MatchingPairs = ({
    playSection,
    sections,
    playerIndex,
    finishedPlaying,
    stopAudioAfter,
    submitResult,
}) => {
    const finishDelay = 1500;
    const xPosition = useRef(-1);
    const yPosition = useRef(-1);
    const score = useRef(undefined);
    const firstCard = useRef(-1);
    const secondCard = useRef(-1);
    const [total, setTotal] = useState(100);
    const [message, setMessage] = useState('Pick a card')

    const resultBuffer = useRef([]);

    const startTime = useRef(Date.now());
    
    const setScoreMessage = (score) => {
        switch (score) {       
            case -10: return '-10 <br />Misremembered';
            case 0: return '0 <br />No match';
            case 10: return '+10 <br />Lucky match';
            case 20: return '+20 <br />Good job!';
            default: return '';
        }
    }

    const registerUserClicks = (posX, posY) => {
        xPosition.current = posX;
        yPosition.current = posY;
    }

    const formatTime = (time) => {
        return time/1000;
    }

    // Show (animated) feedback after second click on second card or finished playing
    const showFeedback = () => {        
                
        const turnedCards = sections.filter(s => s.turned);
        // Check if this turn has finished
        if (turnedCards.length === 2) {                        
            // update total score & display current score
            setTotal(total+score.current);
            setMessage(setScoreMessage(score.current));           
            // show end of turn animations
            switch (score.current) {                                       
                case 10:
                    turnedCards[0].lucky = true;
                    turnedCards[1].lucky = true;                                        
                    break;
                case 20:
                    turnedCards[0].memory = true;
                    turnedCards[1].memory = true;                                        
                    break;
                default:
                    turnedCards[0].nomatch = true;
                    turnedCards[1].nomatch = true;
                    // reset nomatch cards for coming turns
                    setTimeout(() => {
                        turnedCards[0].nomatch = false;
                        turnedCards[1].nomatch = false;                        
                      }, finishDelay);
                    break;  
            }   

            // add third click event to finish the turn
            document.getElementById('root').addEventListener('click', finishTurn);
            return;
        }
    }

    const checkMatchingPairs = (index) => {        
        const currentCard = sections[index];
        const turnedCards = sections.filter(s => s.turned);
        if (turnedCards.length < 2) {
            if (turnedCards.length === 1) {
                // We have two turned cards
                currentCard.turned = true;
                secondCard.current = index;                
                // set no mouse events for all but current
                sections.forEach(section => section.noevents = true);                
                currentCard.noevents = true;
                // check for match
                const lastCard = sections[firstCard.current];                
                if (lastCard.group === currentCard.group) {
                    // match                                        
                    if (currentCard.seen) {
                        score.current = 20;                        
                    } else {
                        score.current = 10;                        
                    }
                } else {                    
                    if (currentCard.seen) { score.current = -10; }
                    else { score.current = 0; }
                };
                currentCard.seen = true;
                lastCard.seen = true;
                showFeedback();
            } else {
                // first click of the turn
                firstCard.current = index;
                // turn first card, disable events
                currentCard.turned = true;
                currentCard.noevents = true;
                // clear message
                setMessage('');
            }              
            resultBuffer.current.push({            
                selectedSection: currentCard.id,
                cardIndex: index,
                score: score.current,
                timestamp: formatTime(Date.now() - startTime.current)
            });
        }
        return;
    };

    const finishTurn = () => {
        finishedPlaying();
        // remove matched cards from the board
        if (score.current === 10 || score.current === 20) {            
            sections[firstCard.current].inactive = true;
            sections[secondCard.current].inactive = true;            
        }
        firstCard.current = -1;
        secondCard.current = -1;
        // remove third click event
        document.getElementById('root').removeEventListener('click', finishTurn);
        score.current = undefined;
        // Turn all cards back and enable events
        sections.forEach(section => section.turned = false);
        sections.forEach(section => section.noevents = false);        
        // Check if the board is empty
        if (sections.filter(s => s.inactive).length === sections.length) {
            // all cards have been turned
            setTimeout(() => {
                submitResult({score: total, moves: resultBuffer.current});
              }, finishDelay);            
        }               
    }

    return (
        <div className="aha__matching-pairs container">
            <div className="row justify-content-around">
                <div className="col-6 align-self-start">
                    <div dangerouslySetInnerHTML={{ __html: message }}
                         className={classNames("matching-pairs__feedback", {fbnomatch: score.current === 0}, {fblucky: score.current === 10}, {fbmemory: score.current === 20}, {fbmisremembered: score.current === -10})}
                        
                    />
                </div>
                <div className="col-6 align-self-end">
                    <div className="matching-pairs__score">Score: <br />{total}</div>        
                </div>
            </div>

            <div className="playing-board d-flex justify-content-center">
                {Object.keys(sections).map((index) => (
                    <PlayCard 
                        key={index}
                        onClick={()=> {
                            playSection(index);
                            checkMatchingPairs(index);
                        }}
                        registerUserClicks={registerUserClicks}
                        playing={playerIndex === index}
                        section={sections[index]}
                        onFinish={showFeedback}
                        stopAudioAfter={stopAudioAfter}                    
                    />
                )
                )}
            </div>
        </div>  
    )
}

export default MatchingPairs;