import { useEffect } from "react";
import { saveAs } from 'file-saver';

import { URLS } from "@/config";
import Button from "../Button/Button";
import Loading from "../Loading/Loading";
import { createConsent, useConsent } from "../../API";
import classNames from "classnames";
import Participant from "@/types/Participant";
import Experiment from "@/types/Experiment";

export interface ConsentProps {
    title: string;
    text: string;
    experiment: Experiment;
    participant: Pick<Participant, 'csrf_token'>;
    onNext: () => void;
    confirm: string;
    deny: string;
}

/** Consent is an experiment view that shows the consent text, and handles agreement/stop actions */
const Consent = ({ title, text, experiment, participant, onNext, confirm, deny }: ConsentProps) => {
    const [consent, loadingConsent] = useConsent(experiment.slug);
    const urlQueryString = window.location.search;

    // Listen for consent, and auto advance if already given
    useEffect(() => {
        if (consent || (new URLSearchParams(urlQueryString).get("participant_id"))) {
            onNext();
        }
    }, [consent, onNext, urlQueryString]);

    // Click on agree button
    const onAgree = async () => {
        // Store consent
        await createConsent({ experiment, participant });

        // Next!
        onNext();
    };

    const onDownload = async () => {
        const doc = new DOMParser().parseFromString(text, 'text/html');
        const txt = doc.body.textContent ? doc.body.textContent.split('  ').join('') : '';
        const blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
        saveAs(blob, 'consent.txt');
    }

    // Loader in case consent is being loaded
    // or it was already given
    if (loadingConsent || consent) {
        return <Loading />;
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
        <div className={classNames("aha__consent")}>
            <div className="aha__consent-header d-flex">
                <div className="flex-fill">
                    <h3>{title}</h3>
                </div>
                <div className="flex-end">
                    <button
                        className="btn btn-download fa-solid fa-download font-weight-bold"
                        data-testid="download-button"
                        onClick={onDownload}
                    >
                    </button>
                </div>
            </div>

            <div
                className="consent-text"
                data-testid="consent-text"
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
