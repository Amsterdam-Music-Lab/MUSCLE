import React, { useEffect } from "react";
import { createSession } from "../../API.js";
import Loading from "../Loading/Loading";
import { stateNextRound } from "../../util/nextRound";

// StartSession is an experiment view that handles the creation of an experiment session
// - It only shows a loader screen while the session is created
// - This view is requird in every experiment as it created the session that is used for storing results
const StartSession = ({
    experiment,
    participant,
    playlist,
    setError,
    setSession,
    loadState,    
}) => {
    // Create a new session, and set state to next_round
    useEffect(() => {
        const init = async () => {
            const data = await createSession({
                experiment,
                participant,
                playlist,
            });

            if (!data) {
                setError("Could not create a session");
                return;
            }

            // Store session
            setSession(data.session);

            // Start next round
            loadState(stateNextRound(data));

        };
        init();
    }, [experiment, participant, playlist, setError, setSession, loadState]);

    return <Loading loadingText={experiment.loading_text} />;
};

export default StartSession;
