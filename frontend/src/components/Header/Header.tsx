import React from "react";
import { Link } from "react-router-dom";

interface HeaderProps {
    nextExperimentSlug: string | undefined;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
    showScore: boolean;
}

export const Header: React.FC<HeaderProps> = ({ nextExperimentSlug, nextExperimentButtonText, collectionSlug, aboutButtonText, showScore }) => {
    return (
        <div className="hero aha__header">
            <div className="intro">
                <nav className="actions">
                    {nextExperimentSlug && <a className="btn btn-lg btn-primary" href={`/${nextExperimentSlug}`}>{nextExperimentButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
        </div>
    );
}

export default Header;
