import React, { useState, useEffect, useCallback, useRef } from "react";
import { useExperimentCollection, useParticipant } from "../../API";
import { Loading } from "../Loading/Loading";


const ExperimentCollection = ({match, location}) => {
    const urlQueryString = useRef(location.search); // location.search is a part of URL after (and incuding) "?"
    const [participant, loadingParticipant] = useParticipant(urlQueryString.current);
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug, participant);

    return (
        !loadingExperimentCollection? (
            <div>ExperimentCollection</div>
        ) :
        (
            <div className="loader-container">
                <Loading />
            </div>
        )
    )
}