import { Link, Redirect } from "react-router-dom";

import { useExperimentCollection } from "../../API";
import Loading  from "../Loading/Loading";

const ExperimentCollection = ({match}) => {
    const [experimentCollection, loadingExperimentCollection] = useExperimentCollection(match.params.slug);
    const dashboard = experimentCollection?.dashboard;
    const experiment = !dashboard && experimentCollection;

    return (
        loadingExperimentCollection? (
            <div className="loader-container">
                <Loading />
            </div>
        ) : dashboard? (
            <div className="aha__collection">
                {/* Experiments */}
                <div className="dashboard">
                    <ul>
                        {dashboard.map((exp) => (
                            <li key={exp.slug} >
                                <Link to={"/" + exp.slug}>
                                    <h3>{exp.name}</h3>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        ) : experiment && (
            <Redirect to={"/" + experiment.slug} />
        )
    )
}

export default ExperimentCollection;