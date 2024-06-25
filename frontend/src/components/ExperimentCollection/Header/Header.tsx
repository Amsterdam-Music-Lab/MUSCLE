import React from "react";
import { Link } from "react-router-dom";


import Social from "../../Social/Social"
import HTML from '@/components/HTML/HTML';
import Score from "../Score/Score";
import { ScoreDisplayConfig } from "@/types/Theme";

interface HeaderProps {
    description: string;
    nextBlockSlug: string | undefined;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    totalScore: number;
    scoreDisplayConfig?: ScoreDisplayConfig;
}

export const Header: React.FC<HeaderProps> = ({
    description,
    nextBlockSlug,
    nextExperimentButtonText,
    aboutButtonText,
    collectionSlug,
    totalScore,
    scoreDisplayConfig,
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

    return (
        <div className="hero aha__header">
            <div className="intro">
                <HTML body={description} innerClassName="" />
                <nav className="actions">
                    {nextBlockSlug && <a className="btn btn-lg btn-primary" href={`/${nextBlockSlug}`}>{nextExperimentButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
            {scoreDisplayConfig && totalScore !== 0 && (
                <div className="results">
                    <Score
                        score={totalScore}
                        rank={{ class: scoreDisplayConfig.scoreClass, text: '' }}
                        label={scoreDisplayConfig.scoreLabel}
                    />
                    <Social
                        social={social}
                    />
                </div>
            )}
            {scoreDisplayConfig && totalScore === 0 && (
                <h3>{scoreDisplayConfig.noScoreLabel}</h3>
            )}
        </div>
    );
}



export default Header;
