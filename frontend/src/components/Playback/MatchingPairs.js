import React, {useRef, useState} from "react";
import classNames from "classnames";

import PlayCard from "../PlayButton/PlayCard";

const MatchingPairs = ({
    playSection,
    sections,
    playerIndex,
    setPlayerIndex,
    lastPlayerIndex,
    finishedPlaying,
    stopAudioAfter,
    submitResult
}) => {
    const finishDelay = 1500;
    const xPosition = useRef(-1);
    const yPosition = useRef(-1);
    const score = useRef(undefined);
    const firstCard = useRef(-1);
    const [total, setTotal] = useState(100);
    const [message, setMessage] = useState('')
    
    // Used to update the component without a click to apply changed classes
    const [feedback, setFeedback] = useState(false)

    const resultBuffer = useRef([]);

    const startTime = useRef(Date.now());
    
    const setScoreMessage = (score) => {
        switch (score) {       
            case -1: return '-1 <br />Misremembered';
            case 0: return '0 <br />No match';
            case 1: return '+1 <br />Lucky match';
            case 2: return '+2 <br />Good job!';
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
        finishedPlaying();        
        const turnedCards = sections.filter(s => s.turned);
        // Check if this turn has finished
        if (turnedCards.length == 2) {                        
            // update total score & display current score
            setTotal(calculateRunningScore());
            setMessage(setScoreMessage(score.current));
            // Turn all cards back and enable events after animations have finished
            setTimeout(() => {
                score.current = undefined;
                sections.forEach(section => section.turned = false);
                sections.forEach(section => section.noevents = false);
                firstCard.current = -1;
                setMessage('<br />Give it another try');
                setFeedback(false);                
            }, finishDelay);
            // show end of turn animations
            switch (score.current) {                                       
                case 1:
                    turnedCards[0].lucky = true;
                    turnedCards[1].lucky = true;
                    turnedCards[0].inactive = true;
                    turnedCards[1].inactive = true;                    
                    break;
                case 2:
                    turnedCards[0].memory = true;
                    turnedCards[1].memory = true;                    
                    turnedCards[0].inactive = true;
                    turnedCards[1].inactive = true;                    
                    break;
                default:
                    turnedCards[0].nomatch = true;
                    turnedCards[1].nomatch = true;
                    // reset nomatch cards for coming turns
                    setTimeout(() => {
                        turnedCards[0].nomatch = false;
                        turnedCards[1].nomatch = false;                        
                      }, 700);
                    break;  
            }   
            // Update the component to show animations 
            setFeedback(true);
            // Check if the board is empty
            if (sections.filter(s => s.inactive).length === sections.length) {
                // all cards have been turned
                setTimeout(() => {
                    submitResult({moves: resultBuffer.current});
                  }, finishDelay);            
            }        
            return;
        }
    }

    const checkMatchingPairs = (index) => {        
        const currentCard = sections[index];
        const turnedCards = sections.filter(s => s.turned);
        if (turnedCards.length < 2) {
            if (turnedCards.length == 1) {
                // We have two turned cards
                currentCard.turned = true;                
                // set no mouse events for all but current
                sections.forEach(section => section.noevents = true);                
                currentCard.noevents = false;
                // check for match
                const lastCard = sections[firstCard.current];                
                if (lastCard.id === currentCard.id) {
                    // match                                        
                    if (currentCard.seen && lastCard.seen) {
                        score.current = 2;                        
                    } else {
                        score.current = 1;                        
                    }
                } else {                    
                    if (lastCard.seen && currentCard.seen) { score.current = -1; }
                    else { score.current = 0; }
                };
                currentCard.seen = true;
                lastCard.seen = true;                
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
                xPosition: xPosition.current,
                yPosition: yPosition.current,
                score: score.current,
                timestamp: formatTime(Date.now() - startTime.current)
            });
            
        } else {
            // second click on second card
            showFeedback();            
        }
    };

    const calculateRunningScore = () => {        
        const allScores = resultBuffer.current.filter(
            r => r.score !== undefined).map(r => r.score);            
        if (!allScores.length) return 100;
        const initial = 0;
        const score = allScores.reduce( 
            (accumulator, s)  => accumulator + s, initial )
        return 100 + score; //Math.round(score / resultBuffer.current.length * 100)
    }
    
    return (
        <div className="aha__matching-pairs container">
            <div className="row">
                <div className="col-6">
                    <div dangerouslySetInnerHTML={{ __html: message }}
                         className={classNames("matching-pairs__feedback", {fbnomatch: score.current == 0}, {fblucky: score.current == 1}, {fbmemory: score.current == 2}, {fbmisremembered: score.current == -1})}
                        
                    />
                </div>
                <div className="col-6">
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