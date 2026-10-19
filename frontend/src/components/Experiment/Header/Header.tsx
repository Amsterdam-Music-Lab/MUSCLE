import React from "react";
import { Link } from "react-router-dom";

import HTML from '@/components/HTML/HTML';
import ScoreCounter, { ScoreCounterProps } from "@/components/ScoreCounter/ScoreCounter";
import Social from "@/components/Social/Social"
import Trophy, { TrophyProps } from "@/components/Trophy/Trophy";
import { SocialMediaConfig } from "@/types/Experiment";
import { ScoreDisplayConfig } from "@/types/Theme";
import { styleButton, styleButtonOutline } from "@/util/stylingHelpers";

interface HeaderProps {
    description: string;
    nextBlockIdentifier: string | undefined;
    nextBlockButtonText: string;
    experimentIdentifier: string;
    aboutButtonText: string;
    totalScore: number;
    scoreDisplayConfig?: ScoreDisplayConfig;
    socialMediaConfig?: SocialMediaConfig;
    buttonColor: string;
}

export const Header: React.FC<HeaderProps> = ({
    description,
    nextBlockIdentifier,
    nextBlockButtonText,
    aboutButtonText,
    experimentIdentifier,
    totalScore,
    scoreDisplayConfig,
    socialMediaConfig,
    buttonColor
}) => {

    return (
        <div className="hero">
            <div className="intro">
                <HTML body={description} innerClassName="" />
                <nav className="actions">
                    {nextBlockIdentifier && <a className="btn btn-lg" css={styleButton(buttonColor)} href={`/block/${nextBlockIdentifier}`}>{nextBlockButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg" css={styleButtonOutline(buttonColor)} to={`/${experimentIdentifier}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
            {scoreDisplayConfig && totalScore !== 0 && (
                <div className="results">
                    <div data-testid="header-trophy" className="aha__header-trophy">
                        <Trophy className={trophy.className} label={trophy.label} />
                        <ScoreCounter score={scores.accumulative.value} label={scores.accumulative.label} />
                    </div >
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
