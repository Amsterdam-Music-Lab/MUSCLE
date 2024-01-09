import {useEffect, React} from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import axios from "axios";
import {create } from "zustand";
import { EXPERIMENT_SLUG, API_BASE_URL, URLS } from "../../config";
import { URLS as ApiUrls } from "../../API";
import Experiment from "../Experiment/Experiment";
import Profile from "../Profile/Profile";
import Reload from "../Reload/Reload";
import StoreProfile from "../StoreProfile/StoreProfile.js";

export const useParticipantStore = create((set) => ({
    participant: null,
    setParticipant: (participant) => set((state) => ({participant}))
}));

// App is the root component of our application
const App = () => {
    const setParticipant = useParticipantStore((state) => state.setParticipant);
    const queryParams = window.location.search;
    
    useEffect(() => {
        const getParticipant = async () => {
            const participantResponse = await axios.get(API_BASE_URL + ApiUrls.participant.current + queryParams);
            setParticipant(participantResponse.data);
        }
        getParticipant();
    }, [])

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
