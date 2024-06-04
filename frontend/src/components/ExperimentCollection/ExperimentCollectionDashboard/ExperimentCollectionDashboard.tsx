import React from "react";
import { Link } from "react-router-dom";

import { API_ROOT } from "@/config";
import ExperimentCollection from "@/types/ExperimentCollection";
import AppBar from "@/components/AppBar/AppBar";
import Header from "@/components/Header/Header";
import IExperiment from "@/types/Experiment";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
    participantIdUrl: string | null;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection, participantIdUrl }) => {

    const dashboard = experimentCollection.dashboard;
    const nextExperimentSlug = experimentCollection.nextExperiment?.slug;
    const headerProps = experimentCollection.theme?.header? {
        nextExperimentSlug,
        collectionSlug: experimentCollection.slug,
        ... experimentCollection.theme.header
    } : undefined;

    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <>
        <AppBar title={experimentCollection.name} logoClickConfirm="placeholder text" />
        {headerProps && (
            <Header { ...headerProps }></Header>
        )}
            {/* Experiments */}
            <div role="menu" className="dashboard toontjehoger">
                <ul>
                    {dashboard.map((exp: IExperiment) => (
                        <li key={exp.slug}>
                            <Link to={getExperimentHref(exp.slug)} role="menuitem">
                                <ImageOrPlaceholder imagePath={exp.image.file} alt={exp.description} />
                                <h3>{exp.name}</h3>
                                <p>{exp.description}</p>
                            </Link>
                        </li>
                    ))}
                    {dashboard.length === 0 && <p>No experiments found</p>}
                </ul>
            </div>
        </>
    );
}

const ImageOrPlaceholder = ({ imagePath, alt }: { imagePath: string, alt: string }) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollectionDashboard;
