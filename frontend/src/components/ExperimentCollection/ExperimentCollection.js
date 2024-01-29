import React, { useState, useEffect, useCallback, useRef } from "react";

import { useExperimentCollection } from "../../API";
import { useParticipantStore } from "../../util/stores";
import Loading  from "../Loading/Loading";


const ExperimentCollection = ({match}) => {
    const urlQueryString = useRef(window.location.search); // location.search is a part of URL after (and incuding) "?"
    const participant = useParticipantStore(state => state.participant);
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);

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

export default ExperimentCollection;