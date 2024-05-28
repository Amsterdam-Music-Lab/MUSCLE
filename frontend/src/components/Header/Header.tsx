import React, { useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "../Social/Social"

interface HeaderProps {
    nextExperimentSlug: string | undefined;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    showScore: boolean;
    totalScore: BigInteger;
    scoreClass: string;
    scoreLabel: string;
    noScoreLabel: string;
}

export const Header: React.FC<HeaderProps> = ({ nextExperimentSlug, nextExperimentButtonText, collectionSlug, aboutButtonText, showScore, totalScore, scoreClass, scoreLabel, noScoreLabel }) => {
    
    const social = {
        'apps': ['facebook', 'twitter'],
        'message': `I scored ${totalScore} points`,
        'url': 'wwww.amsterdammusiclab.nl',
        'hashtags': ["amsterdammusiclab", "citizenscience"]
    }

    const useAnimatedScore = (targetScore) => {
        const [score, setScore] = useState(0);

        const scoreValue = useRef(0);

        useEffect(() => {
            if (targetScore === 0) {
                return;
            }

            let id = -1;

            const nextStep = () => {
                // Score step
                const scoreStep = Math.max(
                    1,
                    Math.min(10, Math.ceil(Math.abs(scoreValue.current - targetScore) / 10))
                );

                // Scores are equal, stop
                if (targetScore === scoreValue.current) {
                    return;
                }

                // Add / subtract score
                scoreValue.current += Math.sign(targetScore - scoreValue.current) * scoreStep;
                setScore(scoreValue.current);

                id = setTimeout(nextStep, 50);
            };
            id = setTimeout(nextStep, 50);

            return () => {
                window.clearTimeout(id);
            };
        }, [targetScore]);

        return score;
    };

    const Score = ({ score, label, scoreClass }) => {
        const currentScore = useAnimatedScore(score);

        return (
            <div className="score">
                <Rank rank={{ class: scoreClass }} />
                <h3>
                    {currentScore ? currentScore + " " : ""}
                    {label}
                </h3>
            </div>
        );
    };
    
    return (
        <div className="hero aha__header">
            <div className="intro">
                <nav className="actions">
                    {nextExperimentSlug && <a className="btn btn-lg btn-primary" href={`/${nextExperimentSlug}`}>{nextExperimentButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
            {showScore, totalScore !== 0 && (
                <div className="results">
                    <Score
                    score={totalScore}
                    scoreClass={scoreClass}
                    label={scoreLabel}
                    />
                    <Social
                        social={social}                        
                    />
                </div>                
            )}
            {showScore, totalScore === 0 && (
                <h3>{noScoreLabel}</h3>
            )}
        </div>
    );
}

export default Header;
