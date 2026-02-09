import { useRef } from "react";

import { useParticipantLink } from "../../API";
import Loading from "../Loading/Loading";
import Button from "../Button/Button";

interface ParticipantLinkProps {
    participantIDOnly?: boolean;
}

const ParticipantLink = ({ participantIDOnly = false }: ParticipantLinkProps) => {
    const [link, loadingLink] = useParticipantLink();
    const linkInput = useRef<HTMLInputElement>(null);

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

    const formatLink = (url: string) => {
        const formatted = participantIDOnly ? url.split('/')[6] : url;
        return formatted;
    }

    if (loadingLink) {
        return <Loading />;
    }

    if (!link) {
        return null;
    }

    return (
        <div className="aha__participant_link">
            <div className="copy">
                <input ref={linkInput} value={formatLink(link.url)} readOnly data-testid="participant-link" />
                <Button label={link.copy_message} onClick={copyLink} color="colorSecondary" data-testid="copy-button"/>
                    
            </div>
        </div>
    )
}

export default ParticipantLink;
