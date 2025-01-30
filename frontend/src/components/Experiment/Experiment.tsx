import { useState } from "react";
import {
    Route,
    Routes,
    useParams
} from "react-router-dom";

import useBoundStore from "../../util/stores";
import { useExperiment } from "@/API";
import Consent from "../Consent/Consent";
import Footer from "../Footer/Footer";
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import ExperimentAbout from "./ExperimentAbout/ExperimentAbout";
import ExperimentDashboard from "./ExperimentDashboard/ExperimentDashboard";
import IExperiment from "@/types/Experiment";
import Redirect from "@/components/Redirect/Redirect";
import useHeadDataFromExperiment from "@/hooks/useHeadDataFromExperiment";

const Experiment = () => {
    const { slug } = useParams();

    const [experiment, loadingExperiment] = useExperiment(slug!) as [IExperiment, boolean];
    const [hasShownConsent, setHasShownConsent] = useState(false);
    const participant = useBoundStore((state) => state.participant);
    const setTheme = useBoundStore((state) => state.setTheme);
    const setHeadData = useBoundStore((state) => state.setHeadData);
    const resetHeadData = useBoundStore((state) => state.resetHeadData);
    const participantIdUrl = participant?.participant_id_url;
    const nextBlock = experiment?.nextBlock;
    const displayDashboard = experiment?.dashboard.length;
    const showConsent = experiment?.consent;
    const totalScore = experiment?.totalScore;

    useHeadDataFromExperiment(experiment, setHeadData, resetHeadData);

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
            experiment,
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
            <Routes>
                <Route
                    path={'/about'}
                    element={<ExperimentAbout content={experiment?.aboutContent} slug={experiment.slug} backButtonText={experiment.backButtonText} />}
                />
                <Route
                    path={'*'}
                    element={<ExperimentDashboard experiment={experiment} participantIdUrl={participantIdUrl} totalScore={totalScore} />}
                />
            </Routes>
            {experiment.theme?.footer && (
                <Footer
                    disclaimer={experiment.disclaimer}
                    logos={experiment.theme.footer.logos}
                    privacy={experiment.privacy}
                />
            )}
        </div>
    )
}

export default Experiment;
