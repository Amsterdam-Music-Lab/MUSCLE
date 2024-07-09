import React from "react";
import { Link } from "react-router-dom";


import Social from "../../Social/Social"
import HTML from '@/components/HTML/HTML';
import { ScoreDisplayConfig } from "@/types/Theme";
import Rank from "@/components/Rank/Rank";
import { SocialMediaConfig } from "@/types/ExperimentCollection";

interface HeaderProps {
    description: string;
    nextBlockSlug: string | undefined;
    nextBlockButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    totalScore: number;
    scoreDisplayConfig?: ScoreDisplayConfig;
    socialMediaConfig?: SocialMediaConfig;
}

export const Header: React.FC<HeaderProps> = ({
    description,
    nextBlockSlug,
    nextBlockButtonText,
    aboutButtonText,
    collectionSlug,
    totalScore,
    scoreDisplayConfig,
    socialMediaConfig
}) => {

    // Get current URL minus the query string
    const currentUrl = window.location.href.split('?')[0];

    const social = {
        apps: socialMediaConfig?.channels || [],
        message: socialMediaConfig?.content || '',
        url: socialMediaConfig?.url || currentUrl,
        hashtags: socialMediaConfig?.tags || [],
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
                    <Rank
                        cup={{ className: scoreDisplayConfig.scoreClass, text: '' }}
                        score={{ score: totalScore, label: scoreDisplayConfig.scoreLabel }}
                    />
                    {socialMediaConfig?.channels?.length && (
                        <Social
                            social={social}
                        />
                    )}
                </div>
            )}
            {scoreDisplayConfig && totalScore === 0 && (
                <h3>{scoreDisplayConfig.noScoreLabel}</h3>
            )}
        </div>
    );
}



export default Header;
