import {
    BrowserRouter as Router,
    Route,
    Redirect
} from "react-router-dom";
import { useExperimentCollection } from "../../API";
import Loading from "../Loading/Loading";
import ExperimentCollectionAbout from "./ExperimentCollectionAbout/ExperimentCollectionAbout";
import ExperimentCollectionDashboard from "./ExperimentCollectionDashboard/ExperimentCollectionDashboard";
import { URLS } from "../../config";

const ExperimentCollection = ({ match }) => {
    /** ExperimentCollection is a Component which can show a dashboard of multiple experiments,
 * or redirect to the next experiment in the collection,
 * depending on the response from the backend, which has the following structure: 
 * {
 *   slug: string,
 *   name: string,
 *   description: string,
 *   dashboard: [
 *     {
 *       slug: string,
 *       name: string,
 *       finished_session_count: number
 *     }
 *   ],
 *   redirect_to: {
 *     slug: string,
 *     name: string,
 *     finished_session_count: number
 *   }
 * }
 * */
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);
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
                <Route path={URLS.experimentCollectionAbout} component={() => <ExperimentCollectionAbout content={'## Hey!\n\n **lolz**'} />} />
                <Route path={URLS.experimentCollection} exact component={() => <ExperimentCollectionDashboard experimentCollection={experimentCollection} />} />
            </Router>
        </div>
    )
}

export default ExperimentCollection;