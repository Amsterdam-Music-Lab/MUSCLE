import {
    BrowserRouter as Router,
    Route,
    Redirect,
    RouteComponentProps
} from "react-router-dom";
import { useExperimentCollection } from "../../API";
import Loading from "../Loading/Loading";
import ExperimentCollectionAbout from "./ExperimentCollectionAbout/ExperimentCollectionAbout";
import ExperimentCollectionDashboard from "./ExperimentCollectionDashboard/ExperimentCollectionDashboard";
import { URLS } from "../../config";
import IExperimentCollection from "@/types/ExperimentCollection";

interface RouteParams {
    slug: string
}

interface ExperimentCollectionProps extends RouteComponentProps<RouteParams> {
}

const ExperimentCollection = ({ match }: ExperimentCollectionProps) => {
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug) as [IExperimentCollection, boolean];
    const experimentToRedirectTo = experimentCollection?.redirect_to;

    if (loadingExperimentCollection) {
        return (
            <div className="loader-container">
                <Loading />
            </div>
        );
    }

    if (experimentToRedirectTo) {
        return <Redirect to={"/" + experimentToRedirectTo.slug} />;
    }

    return (
        <div className="aha__collection">
            <Router>
                <Route path={URLS.experimentCollectionAbout} component={() => <ExperimentCollectionAbout content={experimentCollection?.about_content} slug={experimentCollection.slug} />} />
                <Route path={URLS.experimentCollection} exact component={() => <ExperimentCollectionDashboard experimentCollection={experimentCollection} />} />
            </Router>
        </div>
    )
}

export default ExperimentCollection;