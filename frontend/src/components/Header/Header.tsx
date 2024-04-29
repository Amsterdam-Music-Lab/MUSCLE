import React from "react";

interface HeaderProps {
    nextExperimentSlug: string;
    nextExperimentButtonText: string;
    collectionSlug: string;
    aboutButtonText: string;
}

export const Header: React.FC<HeaderProps> = ({ nextExperimentSlug, nextExperimentButtonText, collectionSlug, aboutButtonText }) => {
    return (
        <div className="hero">
            <div className="intro">
                <nav className="actions">
                    {nextExperimentSlug && <a className="btn btn-lg btn-primary" href={"/" + nextExperimentSlug}>{nextExperimentButtonText}</a>}
                    {aboutButtonText && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${collectionSlug}/about`}>{aboutButtonText}</Link>}
                </nav>
            </div>
        </div>
    );


}

export default Header;
