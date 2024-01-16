import React, { useEffect } from "react";

import { useParticipantStore } from "../../util/stores";
import { createSession } from "../../API.js";
import Loading from "../Loading/Loading";


// StartSession is an experiment view that handles the creation of an experiment session
// - It only shows a loader screen while the session is created
// - This view is requird in every experiment as it created the session that is used for storing results
const StartSession = ({
    experiment,
    playlist,
    setError,
    onNext,
    session,
}) => {
    const participant = useParticipantStore((state) => state.participant);

    // Create a new session, and set state to next_round
    useEffect(() => {
        const init = async () => {
            try { 
                const data = await createSession({
                    experiment,
                    participant,
                    playlist,
                });
                // Store session
                session.current = data.session;
                onNext();
            } catch (err) {
                setError(`Could not create a session: ${err}`)
            }
        };
        init();
    }, [experiment, participant, playlist, session, setError, onNext]);

    return <Loading loadingText={experiment.loading_text} />;
};

export default StartSession;
