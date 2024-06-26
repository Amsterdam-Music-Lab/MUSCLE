import React from "react";
import { Link } from "react-router-dom";

import ExperimentCollection from "@/types/ExperimentCollection";
import Header from "@/components/Header/Header";
import Logo from "@/components/Logo/Logo";
import IExperiment from "@/types/Experiment";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
    participantIdUrl: string | null;
    totalScore: number;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection, participantIdUrl, totalScore }) => {

    const dashboard = experimentCollection.dashboard;
    const nextExperimentSlug = experimentCollection.nextExperiment?.slug;

    const headerProps = experimentCollection.theme?.header ? {
        nextExperimentSlug,
        collectionSlug: experimentCollection.slug,
        ...experimentCollection.theme.header,
        totalScore,
        experimentCollectionTitle: experimentCollection.name,
        experimentCollectionDescription: experimentCollection.description

    } : undefined;

    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <div className="aha__dashboard">
            <Logo logoClickConfirm={null} />
            {headerProps && (
                <Header {...headerProps}></Header>
            )}
            {/* Experiments */}
            <div role="menu" className="dashboard toontjehoger">
                <ul>
                    {dashboard.map((exp: IExperiment) => (
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

const ImageOrPlaceholder = ({ imagePath, alt }: { imagePath: string, alt: string }) => {
    const imgSrc = imagePath ?? null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollectionDashboard;
