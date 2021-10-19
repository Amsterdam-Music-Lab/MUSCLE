import React, { useEffect } from "react";
import { URLS } from "../../config";
import Button from "../Button/Button";
import Loading from "../Loading/Loading";
import * as API from "../../API";

// Consent is an experiment view that shows the consent text, and handles agreement/stop actions
const Consent = ({ title, text, experiment, participant, onNext, confirm, deny }) => {
    const [consent, loadingConsent] = API.useConsent(experiment.slug);

    // Listen for consent, and auto advance if already given
    useEffect(() => {
        if (consent) {
            onNext();
        }
    }, [consent, onNext]);

    // Click on agree button
    const onAgree = async () => {
        // Store consent
        await API.createConsent({ experiment, participant });

        // Next!
        onNext();
    };

    // Loader in case consent is being loaded
    // or it was already given
    if (loadingConsent || consent) {
        return <Loading loadingText={experiment.loading_text} />;
    }

    // Calculate height for consent text to prevent overlapping browser chrome
    const height =
        (document &&
            document.documentElement &&
            document.documentElement.clientHeight) ||
        window.innerHeight;

    const width =
        (document &&
            document.documentElement &&
            document.documentElement.clientWidth) ||
        window.innerWidth;

    const correction = width > 720 ? 300 : 250;

    // Show consent
    return (
        <div className="aha__consent">
            <h3>{title}</h3>

            <div
                className="consent-text"
                style={{ height: height - correction }}
                dangerouslySetInnerHTML={{ __html: text }}
            />

            <div className="buttons d-flex justify-content-between">
                <a href={URLS.AMLHome} className="btn btn-negative btn-lg">
                    {deny}
                </a>

                <Button
                    className="btn-positive"
                    onClick={onAgree}
                    title={confirm}
                />
            </div>
        </div>
    );
};

export default Consent;
