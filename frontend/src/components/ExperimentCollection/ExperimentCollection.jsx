import React, { useEffect, useState, useRef } from "react";
import { Link, Redirect } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import Loading from "../Loading/Loading";
import { API_ROOT } from "../../config";
import Rank from "../Rank/Rank";
import Social from "../Social/Social"

const ExperimentCollection = ({ match }) => {
        /** ExperimentCollection is a Component which can show a dashboard of multiple experiments,
     * or redirect to the next experiment in the collection,
     * depending on the response from the backend, which has the following structure: 
     * {
     *   slug: string,
     *   name: string,
     *   description: string,
     *   dashboard: [
     *     {
     *       slug: string,
     *       name: string,
     *       finished_session_count: number
     *     }
     *   ],
     *   redirect_to: {
     *     slug: string,
     *     name: string,
     *     finished_session_count: number
     *   }
     * }
     * */ 
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);
    const dashboard = experimentCollection?.dashboard || [];
    const experimentToRedirectTo = experimentCollection?.redirect_to;

    // TODO: get next experiment and about link from experimentCollection
    const nextExperiment = null; // TODO: get next experiment from experimentCollection
    const aboutLink = null; // TODO: get about link from experimentCollection

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
       

    if (loadingExperimentCollection) {
        return (
            <div className="loader-container">
                <Loading />
            </div>
        );
    }

    if (experimentToRedirectTo) {
        return <Redirect to={"/" + experimentToRedirectTo.slug} />;
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
        <div className="aha__collection">
            <div className="hero">
                <div className="intro">
                    <p>{experimentCollection?.description}</p>
                    <div className="actions">
                        {nextExperiment && <a className="btn btn-lg btn-primary" href={"/" + nextExperiment.slug}>Volgende experiment</a>}
                        {aboutLink && <a className="btn btn-lg btn-outline-primary" href="/toontjehoger/about">Over ons</a>}
                    </div>
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
                            <Link to={"/" + exp.slug}>
                                <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                <h3>{exp.name}</h3>
                                <div role="status" className="counter">{exp.finished_session_count}</div>
                            </Link>
                        </li>
                    ))}
                    {dashboard.length === 0 && <p>No experiments found</p>}
                </ul>
            </div>
        </div>
    )
}

const ImageOrPlaceholder = ({ imagePath, alt }) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollection;