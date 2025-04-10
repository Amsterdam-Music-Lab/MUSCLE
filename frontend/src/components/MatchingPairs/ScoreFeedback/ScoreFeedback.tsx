import { useRef, useState } from "react";
import classNames from "classnames";

import { scoreIntermediateResult } from "@/API";
import useBoundStore from "@/util/stores";

import Session from "@/types/Session";
import Participant from "@/types/Participant";
import Overlay from "../Overlay/Overlay";
import { ScoreFeedbackDisplay } from "@/types/Playback";

import { Timeline, getTimeline } from "@/components/game";
import PlayingBoard from "@/components/MatchingPairs/PlayingBoard";
import TuneTwins from "@/components/MCGTheme/logos/TuneTwins"
import Score from "@/components/MCGTheme/Score";

// TODO
import {SCORE_FEEDBACK_DISPLAY} from "../MatchingPairs2/MatchingPairs2"


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
                "matching-pairs__score-feedback", "d-flex", "flex-column", "justify-content-center",
                { "matching-pairs__score-feedback--small-bottom-right": scoreFeedbackDisplay === SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT },
            )}
        >
            
            <div className="label pb-2 d-none d-md-inline-block">Total score</div>
            <div data-testid="score" className={`matching-pairs__score ${total == 0 ? 'zero' : (total > 0 ? 'positive' : 'negative')}`}>
                <span className="value">
                    <span className="sign">{ total >= 0 ? "" : "-"}</span>
                    {Math.abs(total)}
                </span>
                <span className="points">points</span>
            </div>
            
            <div className={classNames("matching-pairs__feedback", "pt-2", feedbackClass)} style={{minHeight: "4em"}}>
                <span className="text">{feedbackText}</span>{' '}
                {feedbackClass !== "" && <span className="font-weight-bold">{ 
                    score === 0 ? "You got 0 points." : (score > 0 
                        ? `+${score} points` 
                        : `${score} points`
                    )
                }</span>}
                
            </div>
            
            
        </div>
    )
}


export default ScoreFeedback