import React, { useState } from "react";
import {
    Route,
    Redirect,
    RouteComponentProps,
    Switch
} from "react-router-dom";

import useBoundStore from "../../util/stores";
import { useExperiment } from "@/API";
import Consent from "../Consent/Consent";
import Footer from "../Footer/Footer";
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import ExperimentAbout from "./ExperimentAbout/ExperimentAbout";
import ExperimentDashboard from "./ExperimentDashboard/ExperimentDashboard";
import { URLS } from "@/config";
import IExperiment from "@/types/Experiment";
import IParticipant from "@/types/Participant";

interface RouteParams {
    slug: string
}

interface ExperimentProps extends RouteComponentProps<RouteParams> {
    participant: IParticipant
}

const Experiment = ({ match }: ExperimentProps) => {
    const [experiment, loadingExperiment] = useExperiment(match.params.slug) as [IExperiment, boolean];
    const [hasShownConsent, setHasShownConsent] = useState(false);
    const participant = useBoundStore((state) => state.participant);
    const setTheme = useBoundStore((state) => state.setTheme);
    const participantIdUrl = participant?.participant_id_url;
    const nextBlock = experiment?.nextBlock;
    const displayDashboard = experiment?.dashboard.length;
    const showConsent = experiment?.consent;
    const totalScore = experiment?.totalScore;

    if (experiment?.theme) {
        setTheme(experiment.theme);
    }

    const onNext = () => {
        setHasShownConsent(true);
    }

    const getBlockHref = (slug: string) => `/block/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    if (loadingExperiment) {
        return (
            <div className="loader-container">
                <Loading />
            </div>
        );
    }

    if (!loadingExperiment && !experiment) {
        return <p className="aha__error">Experiment not found</p>;
    }

    if (!hasShownConsent && showConsent) {
        const attrs = {
            participant,
            onNext,
            block: experiment,
            ...experiment.consent,
        }
        return (
            <DefaultPage className='aha__consent-wrapper' title={experiment.name}>
                <Consent {...attrs} />
            </DefaultPage>
        )
    }

    if (!displayDashboard && nextBlock) {
        return <Redirect to={getBlockHref(nextBlock.slug)} />
    }

    return (
        <div className="aha__experiment">
            <Switch>
                <Route path={URLS.experimentAbout} component={() => <ExperimentAbout content={experiment?.aboutContent} slug={experiment.slug} />} />
                <Route path={URLS.experiment} exact component={() => <ExperimentDashboard experiment={experiment} participantIdUrl={participantIdUrl} totalScore={totalScore} />} />
            </Switch>
            {experiment.theme?.footer && (
                <Footer
                    disclaimer={experiment.theme.footer.disclaimer}
                    logos={experiment.theme.footer.logos}
                    privacy={experiment.theme.footer.privacy}
                />
            )}
        </div>
    )
}

export default Experiment;
