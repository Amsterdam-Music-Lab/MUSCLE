import React, { useRef } from "react";
import { createResult } from "../../API.js";
import { MEDIA_ROOT } from "../../config";
import { getSectionUrl } from "../../util/section";
import * as audio from '../../util/audio';
import SongSync from "../SongSync/SongSync";

// CustomTrial handles complex trial views
// - provide a generic onResult callback to the components
const CustomTrial = ({
    experiment,
    session,
    participant,
    loadState,
    playlist,
    loadingText,
    setPlaylist,
    setError,
    setSession,
    onNext,
    state,
}) => {
    const resultBuffer = useRef([]);

    // Session result
    const onResult = async (result, forceSubmit = false) => {
        // Add data to result buffer
        resultBuffer.current.push(result || {});

        // Check if there is another round data available
        // if so, store the result data and call onNext
        // can be forced by forceSubmit
        if (state && state.next_round && !forceSubmit) {
            onNext();
            return;
        }

        // Merge result data with data from resultBuffer
        // NB: result data with same properties will be overwritten by later results
        const mergedResults = Object.assign(
            {},
            ...resultBuffer.current,
            result
        );

        // Create result data
        const data = {
            session,
            participant,
            result: {form: mergedResults},
        };

        // Optionally add section to result data
        if (mergedResults.section) {
            data.section = mergedResults.section;
        }

        // Send data to API
        const action = await createResult(data);

        // Fallback: Call onNext, try to reload round
        if (!action) {
            onNext();
            return;
        }

        // Clear resultBuffer
        resultBuffer.current = [];

        // Check for preload_section_url in (nested) action
        const preloadUrl = getSectionUrl(action);

        if (preloadUrl) {
            setTimeout(() => {
                audio.load(MEDIA_ROOT + preloadUrl);
            }, 20);
        }

        // Init new state from action
        loadState(action);
    };

    // Render experiment state
    const render = (view) => {
        // Default attributes for every view
        const attrs = {
            onResult,
            experiment,
            session,
            participant,
            loadState,
            playlist,
            loadingText,
            setPlaylist,
            setError,
            setSession,
            onNext,
            ...state,
        };

        // Show view, based on the unique view ID:
        switch (view) {
            case "SONG_SYNC":
                return <SongSync {...attrs} />;           
            default:
                return (
                    <div className="text-white bg-danger">
                        Unknown view: {view}
                    </div>
                );
        }
    };

    // Fail safe
    if (!state) {
        return <div>Error: No valid state</div>;
    }

    let key = state.view;

    // Force view refresh for consecutive questions
    if (state.view === "QUESTION") {
        key = state.question.key;
    }

    return (
        <div className="aha__custom-trial" key={key}>
            {render(state.view)}
        </div>
    );
};

export default CustomTrial;
