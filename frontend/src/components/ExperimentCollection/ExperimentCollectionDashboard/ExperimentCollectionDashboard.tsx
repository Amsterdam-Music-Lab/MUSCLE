import React, { useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";

import { API_ROOT } from "../../../config";
import Rank from "../../Rank/Rank";
import Social from "../../Social/Social"
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

    // Values to be sent from the backend
    const score = 165
    const no_score_label = 'Nog geen punten!'
    const score_class = 'gold'
    const score_label = 'Punten'
    const social = {
        'apps': ['facebook', 'twitter'],
        'message': "I scored 100 points",
        'url': 'wwww.amsterdammusiclab.nl',
        'hashtags': ["amsterdammusiclab", "citizenscience"]
    }

    const useAnimatedScore = (targetScore) => {
        const [score, setScore] = useState(0);
    
        const scoreValue = useRef(0);
    
        useEffect(() => {
            if (targetScore === 0) {
                return;
            }
    
            let id = -1;
    
            const nextStep = () => {
                // Score step
                const scoreStep = Math.max(
                    1,
                    Math.min(10, Math.ceil(Math.abs(scoreValue.current - targetScore) / 10))
                );
    
                // Scores are equal, stop
                if (targetScore === scoreValue.current) {
                    return;
                }
    
                // Add / subtract score
                scoreValue.current += Math.sign(targetScore - scoreValue.current) * scoreStep;
                setScore(scoreValue.current);
    
                id = setTimeout(nextStep, 50);
            };
            id = setTimeout(nextStep, 50);
    
            return () => {
                window.clearTimeout(id);
            };
        }, [targetScore]);
    
        return score;
    };

    const Score = ({ score, label, scoreClass }) => {
        const currentScore = useAnimatedScore(score);
    
        return (
            <div className="score">
                <Rank rank={{ class: scoreClass }} />
                <h3>
                    {currentScore ? currentScore + " " : ""}
                    {label}
                </h3>
            </div>
        );
    };

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
                {score && (
                    <div className="results">
                        <Score
                        score={score}
                        scoreClass={score_class}
                        label={score_label}
                        />
                        <Social
                            social={social}                        
                        />
                    </div>                
                )}
                {!score && (
                    <h3>{no_score_label}</h3>
                )}
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
