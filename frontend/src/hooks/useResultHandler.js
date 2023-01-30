import { useRef, useCallback } from "react";
import { createResult } from "../API.js";

// useResult provides a reusable function to handle experiment view data
// - collect results in a buffer
// - handles advancing to next round
// - finally submits the data to the API and loads the new state
const useResultHandler = ({ session, loadState, onNext, state }) => {
    const resultBuffer = useRef([]);

    const onResult = useCallback(
        async (result, forceSubmit = false) => {
            // Add data to result buffer
            resultBuffer.current.push(result || {});

            // Check if there is another round data available
            // can be forced by forceSubmit
            const hasNextRound = state && state.next_round && state.next_round.length;
            if (hasNextRound && !forceSubmit) {
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
                result: mergedResults,
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

            // Init new state from action
            loadState(action);
        },
        [session, loadState, onNext, state]
    );

    return onResult;
};

export default useResultHandler;
