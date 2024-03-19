import { Link, Redirect } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import Loading  from "../Loading/Loading";
import { API_ROOT } from "../../config";

const ExperimentCollection = ({match}) => {
    /** ExperimentCollection is a Component which can show a dashboard of multiple experiments,
     * or redirect to the next experiment in the collection,
     * depending on the response from the backend, which can come in two "flavours": 
     * {
     *   slug: string,
     *   name: string,
     *   finished_session_count: number
     * }
     * {
     *  dashboard:
     *    [
     *      {
     *        slug: string
     *        name: string,
     *        sessions_finished: number
     *      }
     *    ]
     * }
     * */ 
    
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug); 

    return (
        loadingExperimentCollection? (
            <div className="loader-container">
                <Loading />
            </div>
        ) : experimentCollection.dashboard? (
            <div className="aha__collection">
                {/* Experiments */}
                <div role="menu" className="dashboard">
                    <ul>
                        {experimentCollection.dashboard.map((exp) => (
                            <li key={exp.slug} >
                                <Link to={"/" + exp.slug}>
                                    <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                    <h3>{exp.name}</h3>
                                    <div role="status" className="counter">{exp.finished_session_count}</div>
                                </Link>   
                            </li> 
                        ))}
                    </ul>
                </div>
            </div>
        ) : (
            <Redirect data-testid="collection-redirect" to={"/" + experimentCollection.slug} />
        )
    )
}

const ImageOrPlaceholder = ({imagePath, alt}) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollection;