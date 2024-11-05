import React from "react";
import { Link } from "react-router-dom";

import Experiment from "@/types/Experiment";
import Header from "@/components/Experiment/Header/Header";
import Logo from "@/components/Logo/Logo";
import IBlock from "@/types/Block";


interface ExperimentDashboardProps {
    experiment: Experiment;
    participantIdUrl: string | null;
    totalScore: number;
}

export const ExperimentDashboard: React.FC<ExperimentDashboardProps> = ({ experiment, participantIdUrl, totalScore }) => {

    const { dashboard, description } = experiment;
    const { nextBlockButtonText, aboutButtonText } = experiment.theme?.header || { nextBlockButtonText: "", aboutButtonText: "" };

    const scoreDisplayConfig = experiment.theme?.header?.score;
    const nextBlockSlug = experiment.nextBlock?.slug;
    const showHeader = experiment.theme?.header;
    const socialMediaConfig = experiment.socialMediaConfig;

    const getExperimentHref = (slug: string) => `/block/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <div className="aha__dashboard">
            <Logo />
            {showHeader && (
                <Header
                    nextBlockSlug={nextBlockSlug}
                    experimentSlug={experiment.slug}
                    totalScore={totalScore}
                    description={description}
                    scoreDisplayConfig={scoreDisplayConfig}
                    nextBlockButtonText={nextBlockButtonText}
                    aboutButtonText={aboutButtonText}
                    socialMediaConfig={socialMediaConfig}
                />
            )}
            {/* Experiments */}
            <div role="menu" className="dashboard toontjehoger">
                <ul>
                    {dashboard.map((exp: IBlock) => (
                        <li key={exp.slug}>
                            <Link to={getExperimentHref(exp.slug)} role="menuitem">
                                <ImageOrPlaceholder imagePath={exp.image?.file} alt={exp.image?.alt ?? exp.description} />
                                <h3>{exp.name}</h3>
                                <p>{exp.description}</p>
                            </Link>
                        </li>
                    ))}
                    {dashboard.length === 0 && <p>No experiments found</p>}
                </ul>
            </div>
        </div>
    );
}

const ImageOrPlaceholder = ({ imagePath, alt }: { imagePath?: string, alt: string }) => {
    const imgSrc = imagePath ?? null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentDashboard;
