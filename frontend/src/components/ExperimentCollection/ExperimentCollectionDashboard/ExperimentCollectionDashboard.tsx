import React from "react";
import { Link } from "react-router-dom";

import { API_ROOT } from "@/config";
import ExperimentCollection from "@/types/ExperimentCollection";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
    participantIdUrl: string | null;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection, participantIdUrl }) => {

    const dashboard = experimentCollection?.dashboard;

    // TODO: get next experiment and about link from experimentCollection
    const nextExperiment = experimentCollection.next_experiment; // TODO: get next_experiment from experimentCollection
    const aboutContent = experimentCollection.about_content;

    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <>
            <div className="hero">
                <div className="intro">
                    <p>{experimentCollection?.description}</p>
                    <nav className="actions">
                        {nextExperiment && <a className="btn btn-lg btn-primary" href={"/" + nextExperiment.slug}>Volgende experiment</a>}
                        {aboutContent && <Link className="btn btn-lg btn-outline-primary" to={`/collection/${experimentCollection.slug}/about`}>Over ons</Link>}
                    </nav>
                </div>
                <div className="results">

                </div>
            </div>
            {/* Experiments */}
            <div role="menu" className="dashboard">
                <ul>
                    {dashboard.map((exp) => (
                        <li key={exp.slug}>
                            <Link to={getExperimentHref(exp.slug)} role="menuitem">
                                <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                <h3>{exp.name}</h3>
                                <div className="status-bar">
                                    <span title={`Started ${exp.started_session_count} times`} role="status" className="counter">{exp.started_session_count}</span>
                                    <span title={`Started ${exp.finished_session_count} times`} role="status" className="counter">{exp.finished_session_count}</span>
                                </div>
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
