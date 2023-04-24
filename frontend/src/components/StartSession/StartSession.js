import React, { useEffect } from "react";
import { createSession } from "../../API.js";
import Loading from "../Loading/Loading";

// StartSession is an experiment view that handles the creation of an experiment session
// - It only shows a loader screen while the session is created
// - This view is requird in every experiment as it created the session that is used for storing results
const StartSession = ({
    experiment,
    participant,
    playlist,
    setError,
    session,
    onNext,
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
            session.current = data.session;

            onNext();
            
        };
        init();
    }, [experiment, participant, playlist, session, setError, onNext]);

    return <Loading loadingText={experiment.loading_text} />;
};

export default StartSession;
