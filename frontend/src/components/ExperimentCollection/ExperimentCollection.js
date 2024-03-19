import { Link, Redirect } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import Loading from "../Loading/Loading";
import { API_ROOT } from "../../config";

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
    const dashboard = experimentCollection?.dashboard || [];
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
            {/* Experiments */}
            <div role="menu" className="dashboard">
                <ul>
                    {dashboard.map((exp) => (
                        <li key={exp.slug}>
                            <Link to={"/" + exp.slug}>
                                <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                <h3>{exp.name}</h3>
                                <div role="status" className="counter">{exp.finished_session_count}</div>
                            </Link>
                        </li>
                    ))}
                    {dashboard.length === 0 && <p>No experiments found</p>}
                </ul>
            </div>
        </div>
    )
}

const ImageOrPlaceholder = ({ imagePath, alt }) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollection;