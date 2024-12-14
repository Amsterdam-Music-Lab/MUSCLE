import React from "react";
import { Link } from "react-router-dom";


import Social from "../../Social/Social"
import HTML from '@/components/HTML/HTML';
import { ScoreDisplayConfig } from "@/types/Theme";
import Rank from "@/components/Rank/Rank";
import { SocialMediaConfig } from "@/types/Experiment";

interface HeaderProps {
    description: string;
    nextBlockSlug: string | undefined;
    nextBlockButtonText: string;
    experimentSlug: string;
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
    experimentSlug,
    totalScore,
    scoreDisplayConfig,
    socialMediaConfig
}) => {

    return (
        <div className="hero">
            <div className="intro">
                <HTML body={description} innerClassName="" />
                <nav className="actions">
                    {nextBlockSlug && <a className="btn btn-lg btn-primary" href={`/block/${nextBlockSlug}`}>{nextBlockButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/${experimentSlug}/about`}>{aboutButtonText}</Link>}
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
                            social={socialMediaConfig}
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
