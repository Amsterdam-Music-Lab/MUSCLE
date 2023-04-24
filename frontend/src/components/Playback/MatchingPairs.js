import React, {useRef} from "react";

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

    const resultBuffer = useRef([]);

    const startTime = useRef(Date.now());

    const setScoreMessage = (score) => {
        switch(score) {
            case -1: return '-1 Misremembered!'
            case 0: return '0';
            case 1: return '+1 Lucky match!';
            case 2: return '+2 Good job!';
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

    const checkMatchingPairs = (index) => {
        const currentCard = sections[index];
        const turnedCards = sections.filter(s => s.turned);
        if (turnedCards.length == 1) {
            // we have two turned cards
            currentCard.turned = true;
            // check for match
            const lastCard = lastPlayerIndex.current >=0 ? sections[lastPlayerIndex.current] : undefined;
            if (lastCard && lastCard.id === currentCard.id) {
                // match
                lastCard.inactive = true;
                currentCard.inactive = true;
                setPlayerIndex(-1);
                if (currentCard.seen && lastCard.seen) {
                    score.current = 2;
                    lastCard.memory = true;
                    currentCard.memory = true;
                } else {
                    score.current = 1;
                    lastCard.lucky = true;
                    currentCard.lucky = true;
                }
            } else {
                if (lastCard.seen && currentCard.seen) { score.current = -1; }
                else { score.current = 0; }
                lastCard.nomatch = true;
                currentCard.nomatch = true;
                setTimeout(() => {
                    lastCard.nomatch = false;
                    currentCard.nomatch = false;
                  }, 700);
                
            };
        } else {
            // turn all cards back, turn current card
            lastPlayerIndex.current = -1;
            sections.forEach(section => section.turned = false);
            currentCard.turned = true;
            score.current = undefined;
        }

        resultBuffer.current.push({
            selectedSection: currentCard.id,
            xPosition: xPosition.current,
            yPosition: yPosition.current,
            score: score.current,
            timestamp: formatTime(Date.now() - startTime.current)
        });
        
        currentCard.seen = true;

        if (sections.filter(s => s.inactive).length === sections.length) {
            // all cards have been turned
            setTimeout(() => {
                submitResult({moves: resultBuffer.current});
              }, finishDelay);
            
        }
        
        return;
    };

    const calculateRunningScore = () => {
        const allScores = resultBuffer.current.filter(
            r => r.score !== undefined ).map( r => r.score );
        if (!allScores.length) return 100;
        const initial = 0;
        const score = allScores.reduce( 
            (accumulator, s)  => accumulator + s, initial )
        return 100 + score; //Math.round(score / resultBuffer.current.length * 100)
    }
    
    return (
        <div className="aha__matching-pairs container">
            <h5 className="matching-pairs__score">Score: {calculateRunningScore()}</h5>
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
                onFinish={finishedPlaying}
                stopAudioAfter={stopAudioAfter}
                />
            )
            )}
            </div>
            <div className="matching-pairs__feedback">{setScoreMessage(score.current)}</div>
        </div>  
    )
}

export default MatchingPairs;