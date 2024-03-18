import { Link, Redirect } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import Loading  from "../Loading/Loading";
import { API_ROOT } from "../../config";

const ExperimentCollection = ({match}) => {
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);
    const dashboard = experimentCollection?.dashboard;
    const experiment = dashboard ? undefined : experimentCollection;;

    return (
        loadingExperimentCollection? (
            <div className="loader-container">
                <Loading />
            </div>
        ) : dashboard? (
            <div className="aha__collection">
                {/* Experiments */}
                <div data-testid="collection-dashboard" className="dashboard">
                    <ul>
                        {dashboard.map((exp) => (
                            <li key={exp.slug}>
                                <Link to={"/" + exp.slug}>
                                    <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                    <h3>{exp.name}</h3>
                                    <p>{exp.description}</p>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        ) : experiment && (
            <Redirect data-testid="collection-redirect" to={"/" + experiment.slug} />
        )
    )
}

const ImageOrPlaceholder = ({imagePath, alt}) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollection;