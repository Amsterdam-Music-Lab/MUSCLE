import React, { useState } from "react";
import {
    Route,
    Redirect,
    RouteComponentProps,
    Switch
} from "react-router-dom";

import useBoundStore from "../../util/stores";
import { useExperimentCollection } from "@/API";
import Consent from "../Consent/Consent";
import Footer from "../Footer/Footer";
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import ExperimentCollectionAbout from "./ExperimentCollectionAbout/ExperimentCollectionAbout";
import ExperimentCollectionDashboard from "./ExperimentCollectionDashboard/ExperimentCollectionDashboard";
import { URLS } from "@/config";
import IExperimentCollection from "@/types/ExperimentCollection";
import IParticipant from "@/types/Participant";

interface RouteParams {
    slug: string
}

interface ExperimentCollectionProps extends RouteComponentProps<RouteParams> {
    participant: IParticipant
}

const ExperimentCollection = ({ match }: ExperimentCollectionProps) => {
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug) as [IExperimentCollection, boolean];
    const [hasShownConsent, setHasShownConsent] = useState(false);
    const participant = useBoundStore((state) => state.participant);
    const setTheme = useBoundStore((state) => state.setTheme);
    const participantIdUrl = participant?.participant_id_url;
    const nextExperiment = experimentCollection?.nextExperiment;
    const displayDashboard = experimentCollection?.dashboard.length;
    const showConsent = experimentCollection?.consent;
    const totalScore = experimentCollection?.totalScore;
    const score = experimentCollection?.score;

    if (experimentCollection?.theme) {
        setTheme(experimentCollection.theme);
    }

    const onNext = () => {
        setHasShownConsent(true);
    }

    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    if (loadingExperimentCollection) {
        return (
            <div className="loader-container">
                <Loading />
            </div>
        );
    }

    if (!loadingExperimentCollection && !experimentCollection) {
        return <p className="aha__error">Experiment not found</p>;
    }

    if (!hasShownConsent && showConsent) {
        const attrs = {
            participant,
            onNext,
            experiment: experimentCollection,
            ...experimentCollection.consent,
        }
        return (
            <DefaultPage className='aha__consent-wrapper' title={experimentCollection.name}>
                <Consent {...attrs}/>
            </DefaultPage>
        )
    }

    if (!displayDashboard && nextExperiment) {
        return <Redirect to={getExperimentHref(nextExperiment.slug)} />
    }

    return (
        <div className="aha__collection">
            <Switch>
                <Route path={URLS.experimentCollectionAbout} component={() => <ExperimentCollectionAbout content={experimentCollection?.aboutContent} slug={experimentCollection.slug} />} />
                <Route path={URLS.experimentCollection} exact component={() => <ExperimentCollectionDashboard experimentCollection={experimentCollection} participantIdUrl={participantIdUrl} totalScore={totalScore} score={score} />} />
            </Switch>
            {experimentCollection.theme?.footer && (
                <Footer
                    disclaimer={experimentCollection.theme.footer.disclaimer}
                    logos={experimentCollection.theme.footer.logos}
                    privacy={experimentCollection.theme.footer.privacy}
                />
            )}
        </div>
    )
}

export default ExperimentCollection;