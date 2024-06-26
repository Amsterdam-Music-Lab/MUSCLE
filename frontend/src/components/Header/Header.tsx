import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "../Social/Social"
import HTML from '@/components/HTML/HTML';

interface HeaderProps {
    experimentCollectionTitle: string;
    experimentCollectionDescription: string;
    nextExperimentSlug: string | undefined;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    totalScore: Number;
}

interface Score {
    scoreClass: string;
    scoreLabel: string;
    noScoreLabel: string;
}

export const Header: React.FC<HeaderProps> = ({
    experimentCollectionTitle,
    experimentCollectionDescription,
    nextExperimentSlug,
    nextExperimentButtonText,
    collectionSlug,
    aboutButtonText,
    totalScore,
    score,
}) => {

    // TODO: Fix this permanently and localize in the backend
    // See also: https://github.com/Amsterdam-Music-Lab/MUSCLE/issues/1151
    // Get locale from browser (this is meant to be temporary until we have a proper solution for localization in the backend)
    const locale = navigator.language || 'en-US';
    const localeIsEnglish = locale.includes('en');

    // Get current URL minus the query string
    const currentUrl = window.location.href.split('?')[0];
    const hashtags = [experimentCollectionTitle ? experimentCollectionTitle.replace(/ /g, '').toLowerCase() : 'amsterdammusiclab'];

    const social = {
        apps: ['facebook', 'twitter'],
        message: localeIsEnglish ? `I scored ${totalScore} points` : `Ik heb ${totalScore} punten gescoord`,
        url: currentUrl,
        hashtags
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
                    {nextExperimentSlug && <a className="btn btn-lg btn-primary" href={`/${nextExperimentSlug}`}>{nextExperimentButtonText}</a>}
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
