import React from "react";
import { Link } from "react-router-dom";

import ExperimentCollection from "@/types/ExperimentCollection";
import Header from "@/components/ExperimentCollection/Header/Header";
import Logo from "@/components/Logo/Logo";
import IBlock from "@/types/Block";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
    participantIdUrl: string | null;
    totalScore: number;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection, participantIdUrl, totalScore }) => {

    const { dashboard, description } = experimentCollection;
    const { nextExperimentButtonText, aboutButtonText } = experimentCollection.theme?.header || { nextExperimentButtonText: "", aboutButtonText: "" };

    const scoreDisplayConfig = experimentCollection.theme?.header?.score;
    const nextBlockSlug = experimentCollection.nextExperiment?.slug;
    const showHeader = experimentCollection.theme?.header;
    const socialMediaConfig = experimentCollection.socialMediaConfig;

    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <div className="aha__dashboard">
            <Logo logoClickConfirm={null} />
            {showHeader && (
                <Header
                    nextBlockSlug={nextBlockSlug}
                    collectionSlug={experimentCollection.slug}
                    totalScore={totalScore}
                    description={description}
                    scoreDisplayConfig={scoreDisplayConfig}
                    nextBlockButtonText={nextExperimentButtonText}
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

export default ExperimentCollectionDashboard;
