import {useEffect, React} from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import axios from "axios";

import { API_BASE_URL, EXPERIMENT_SLUG, URLS } from "../../config";
import { URLS as API_URLS } from "../../API";
import useBoundStore from "../../util/stores";
import Experiment from "../Experiment/Experiment";
import Profile from "../Profile/Profile";
import Reload from "../Reload/Reload";
import StoreProfile from "../StoreProfile/StoreProfile.js";


// App is the root component of our application
const App = () => {
    const error = useBoundStore(state => state.error);
    const setError = useBoundStore(state => state.setError);
    const setParticipant = useBoundStore((state) => state.setParticipant);
    const queryParams = window.location.search;
    
    useEffect(() => {
        const urlParams = new URLSearchParams(queryParams);
        if (!urlParams.has("participant_id")) {
            return;
        }
        try {
            axios.get(API_BASE_URL + API_URLS.participant.current + queryParams).then(response => {
                setParticipant(response.data);
            });
        } catch (err) {
            console.error(err);
            setError('Could not load participant');
        }
    }, [setError, queryParams, setParticipant])

    if (error) {
        return <p className="aha__error">Error: {error}</p>;
    }

    return (
        <Router className="aha__app">
            <Switch>
                {/* Request reload for given participant */}
                <Route path={URLS.reloadParticipant}>
                    <Reload/>
                </Route>

                {/* Default experiment */}
                <Route path="/" exact>
                    <Redirect
                        to={URLS.experiment.replace(":slug", EXPERIMENT_SLUG)}
                    />
                </Route>
                
                {/* Profile */}
                <Route path={URLS.profile} exact>
                    <Profile slug={EXPERIMENT_SLUG} />
                </Route>

                {/* Experiment */}
                <Route path={URLS.experiment} component={Experiment} />

                <Route path={URLS.session} />

                {/* Store profile */}
                <Route
                    path={URLS.storeProfile}
                    exact
                    component={StoreProfile}
                />


            </Switch>
        </Router>
    );
};

export default App;
