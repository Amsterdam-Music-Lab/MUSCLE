import { Suspense, lazy, useState } from "react";
import {
    Route,
    Routes,
    useParams
} from "react-router-dom";

import DefaultPage from "@/components/Page/DefaultPage";
import Loading from "@/components/Loading/Loading";
import Redirect from "@/components/Redirect/Redirect";
const Consent = lazy(() => import("@/components/Consent/Consent"));
const Footer = lazy(() => import("@/components/Footer/Footer"));
const ExperimentAbout = lazy(() => import("@/components/Experiment/ExperimentAbout/ExperimentAbout"));
const ExperimentDashboard = lazy(() => import("@/components/Experiment/ExperimentDashboard/ExperimentDashboard"));
import IExperiment from "@/types/Experiment";
import useHeadDataFromExperiment from "@/hooks/useHeadDataFromExperiment";
import useBoundStore from "@/util/stores";
import { getBlockHref, useExperiment } from "@/API";

const Experiment = () => {
    const { identifier } = useParams();

    const [experiment, loadingExperiment] = useExperiment(identifier!) as [IExperiment, boolean];
    const [hasShownConsent, setHasShownConsent] = useState(false);
    const participant = useBoundStore((state) => state.participant);
    const setTheme = useBoundStore((state) => state.setTheme);
    const setHeadData = useBoundStore((state) => state.setHeadData);
    const resetHeadData = useBoundStore((state) => state.resetHeadData);
    const participantIdUrl = participant?.participant_id_url;
    const nextBlock = experiment?.nextBlock;
    const displayDashboard = experiment?.dashboard.length;
    const showConsent = experiment?.consent;
    const totalScore = experiment?.accumulatedScore;

    useHeadDataFromExperiment(experiment, setHeadData, resetHeadData);

    if (experiment?.theme) {
        setTheme(experiment.theme);
    }

    const onNext = () => {
        setHasShownConsent(true);
    }

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
            experiment,
            ...experiment.consent,
        }
        return (
            <DefaultPage className='aha__consent-wrapper' title={experiment.name}>
                <Suspense fallback={<Loading />}>
                    <Consent {...attrs} />
                </Suspense>
            </DefaultPage>
        )
    }

    if (!displayDashboard && nextBlock) {
        return <Redirect to={getBlockHref(experiment.identifier, nextBlock.identifier, participantIdUrl)} />
    }

    return (
        <div className="aha__experiment">
            <Routes>
                <Route
                    path={'/about'}
                    element={<ExperimentAbout {...experiment} />}
                />
                <Route
                    path={'*'}
                    element={<ExperimentDashboard experiment={experiment} participantIdUrl={participantIdUrl} totalScore={totalScore} />}
                />
            </Routes>
            {experiment.theme?.footer && (
                <Suspense fallback={<Loading />}>
                    <Footer
                        disclaimer={experiment.disclaimer}
                        logos={experiment.theme.footer.logos}
                        privacy={experiment.privacy}
                    />
                </Suspense>
            )}
        </div>
    )
}

export default Experiment;
