import React, { useRef } from "react";

import { useParticipantScores, useParticipantLink } from "../../API";
import Loading from "../Loading/Loading";

const ParticipantLink = () => {
    const [data, loadingData] = useParticipantScores();
    const [link, loadingLink] = useParticipantLink();
    const linkInput = useRef();

    const copyLink = () => {
        if (!linkInput.current) {
            return;
        }

        // Select text
        linkInput.current.select();

        // For mobile
        linkInput.current.setSelectionRange(0, 99999);

        // Copy
        navigator.clipboard.writeText(linkInput.current);
    };
    switch (true) {
        case loadingData || loadingLink:
            return <Loading />;
        default:
            return (
                <div className="aha__participant_link">
                    <div className="copy">
                        <input ref={linkInput} value={link.url} readonly />
                        <button onClick={copyLink} onKeyPress={copyLink}>
                            COPY
                        </button>
                    </div>
                </div>
            )
    }
}

export default ParticipantLink;


