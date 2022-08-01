import React, { useRef } from "react";

import { useParticipantLink } from "../../API";
import Loading from "../Loading/Loading";

const ParticipantLink = ({participantIDOnly}) => {
    const [link, loadingLink] = useParticipantLink();
    const linkInput = useRef();

    const copyLink = () => {
        if (!linkInput.current) {
            return;
        }

        // mark text in input box
        linkInput.current.select();

        // For mobile
        linkInput.current.setSelectionRange(0, 99999);
        // Copy
        navigator.clipboard.writeText(linkInput.current.value);
    };

    const formatLink = (url) => {
        const formatted = participantIDOnly===true ? url.split('/')[6] : url;
        return formatted;
    }

    switch (true) {
        case loadingLink:
            return <Loading />;
        default:
            return (
                <div className="aha__participant_link">
                    <div className="copy">
                        <input ref={linkInput} value={formatLink(link.url)} readOnly />
                        <button onClick={copyLink} onKeyPress={copyLink}>
                            {link.copy_message}
                        </button>
                    </div>
                </div>
            )
    }
}

export default ParticipantLink;


