import React from "react";
import { Link } from "react-router-dom";


import Social from "../../Social/Social"
import HTML from '@/components/HTML/HTML';
import Score from "@/components/ScoreCounter/ScoreCounter";
import { ScoreDisplayConfig } from "@/types/Theme";
import Rank from "@/components/Rank/Rank";

interface HeaderProps {
    name: string;
    description: string;
    nextBlockSlug: string | undefined;
    nextBlockButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    totalScore: number;
    scoreDisplayConfig?: ScoreDisplayConfig;
}

export const Header: React.FC<HeaderProps> = ({
    name,
    description,
    nextBlockSlug,
    nextBlockButtonText,
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
    const hashtags = [name ? name.replace(/ /g, '') : 'amsterdammusiclab'];

    const social = {
        apps: ['facebook', 'twitter'],
        message,
        url: currentUrl,
        hashtags,
    }

    return (
        <div className="hero">
            <div className="intro">
                <HTML body={description} innerClassName="" />
                <nav className="actions">
                    {nextBlockSlug && <a className="btn btn-lg btn-primary" href={`/${nextBlockSlug}`}>{nextBlockButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
            {scoreDisplayConfig && totalScore !== 0 && (
                <div className="results">
                    <Rank rank={{ class: scoreDisplayConfig.scoreClass, text: '' }} />
                    <Score
                        score={totalScore}
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
