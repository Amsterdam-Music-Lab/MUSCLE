import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import { useParticipantStore } from "../../util/stores";
import Loading  from "../Loading/Loading";


const ExperimentCollection = ({match}) => {
    const urlQueryString = useRef(window.location.search); // location.search is a part of URL after (and incuding) "?"
    const participant = useParticipantStore(state => state.participant);
    const experiment = useRef(null);
    const [dashboard, setDashboard] = useState(undefined);
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);

    useEffect(() => {
        if (!loadingExperimentCollection) {
            if (experimentCollection) {
                if (experimentCollection.dashboard) {
                    setDashboard(experimentCollection.dashboard);
                } else {
                    // redirect to experimentCollection.slug;
                }
            }
        }
    }, [experimentCollection, loadingExperimentCollection, setDashboard])

    return (
        !loadingExperimentCollection && dashboard ? (
        <div className="aha__collection">
            {/* <Logo homeUrl={`/${experiment.slug}`} /> */}
            {/* Experiments */}
            <div className="dashboard">
                <ul>
                    {dashboard.map((experiment) => (
                        <li
                            key={experiment.slug}
                            // style={{
                            //     borderBottom: `5px solid ${experiment.color}`,
                            // }}
                        >
                            <Link to={"/" + experiment.slug}>
                                <div
                                    className="image"
                                    // style={{
                                    //     backgroundImage: `url(${experiment.image})`,
                                    //     backgroundColor: experiment.color,
                                    // }}
                                ></div>
                                <h3>{experiment.name}</h3>
                                {/* <p>{experiment.description}</p> */}
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
            
        ) :
        (
            <div className="loader-container">
                <Loading />
            </div>
        )
    )
}

export default ExperimentCollection;