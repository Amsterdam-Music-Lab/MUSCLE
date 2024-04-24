import React from "react";
import { Link } from "react-router-dom";

import { API_ROOT } from "@/config";
import ExperimentCollection from "@/types/ExperimentCollection";
import DefaultPage from "@/components/Page/DefaultPage";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection }) => {

    const dashboard = experimentCollection?.dashboard;

    return (
        <DefaultPage>
            {/* Experiments */}
            <div role="menu" className="dashboard">
                <ul>
                    {dashboard.map((exp) => (
                        <li key={exp.slug}>
                            <Link to={"/" + exp.slug}>
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
        </DefaultPage>
    );
}

const ImageOrPlaceholder = ({ imagePath, alt }: { imagePath: string, alt: string }) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollectionDashboard;
