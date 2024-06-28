import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "../Social/Social"
import HTML from '@/components/HTML/HTML';

interface HeaderProps {
    experimentCollectionTitle: string;
    experimentCollectionDescription: string;
    nextBlockSlug: string | undefined;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    totalScore: number;
}

interface Score {
    scoreClass: string;
    scoreLabel: string;
    noScoreLabel: string;
}

export const Header: React.FC<HeaderProps> = ({
    experimentCollectionTitle,
    experimentCollectionDescription,
    nextBlockSlug,
    nextExperimentButtonText,
    collectionSlug,
    aboutButtonText,
    totalScore,
    score,
}) => {

    // TODO: Fix this permanently and localize in and fetch content from the backend
    // See also: https://github.com/Amsterdam-Music-Lab/MUSCLE/issues/1151
    // Get current URL minus the query string
    const currentUrl = window.location.href.split('?')[0];
    const message = totalScore > 0 ? `Ha! Ik ben muzikaler dan ik dacht - heb maar liefst ${totalScore} punten! Speel mee met #ToontjeHoger` : "Ha! Speel mee met #ToontjeHoger en laat je verrassen: je bent muzikaler dat je denkt!";
    const hashtags = [experimentCollectionTitle ? experimentCollectionTitle.replace(/ /g, '') : 'amsterdammusiclab'];

    const social = {
        apps: ['facebook', 'twitter'],
        message,
        url: currentUrl,
        hashtags,
    }

    const useAnimatedScore = (targetScore: number) => {
        const [score, setScore] = useState(0);

        useEffect(() => {
            if (targetScore === 0) {
                setScore(0);
                return;
            }

            let animationFrameId: number;

            const nextStep = () => {
                setScore((prevScore) => {
                    const difference = targetScore - prevScore;
                    const scoreStep = Math.max(1, Math.min(10, Math.ceil(Math.abs(difference) / 10)));

                    if (difference === 0) {
                        cancelAnimationFrame(animationFrameId);
                        return prevScore;
                    }

                    const newScore = prevScore + Math.sign(difference) * scoreStep;
                    animationFrameId = requestAnimationFrame(nextStep);
                    return newScore;
                });
            };

            // Start the animation
            animationFrameId = requestAnimationFrame(nextStep);

            // Cleanup function to cancel the animation frame
            return () => {
                cancelAnimationFrame(animationFrameId);
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
                <HTML body={experimentCollectionDescription} innerClassName="" />
                <nav className="actions">
                    {nextBlockSlug && <a className="btn btn-lg btn-primary" href={`/${nextBlockSlug}`}>{nextExperimentButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
            {score && totalScore !== 0 && (
                <div className="results">
                    <Score
                        score={totalScore}
                        scoreClass={score.scoreClass}
                        label={score.scoreLabel}
                    />
                    <Social
                        social={social}
                    />
                </div>
            )}
            {score && totalScore === 0 && (
                <h3>{score.noScoreLabel}</h3>
            )}
        </div>
    );
}



export default Header;
