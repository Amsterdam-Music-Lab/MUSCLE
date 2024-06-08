import { useRef, useCallback } from "react";
import { scoreResult } from "@/API";

interface ResultData {
    session: unknown;
    participant: unknown;
    result: unknown;
    section?: unknown;
}

// useResult provides a reusable function to handle experiment view data
// - collect results in a buffer
// - handles advancing to next round
// - finally submits the data to the API and loads the new state
const useResultHandler = ({ session, participant, onNext, state }) => {
    const resultBuffer = useRef([]);

    const onResult = useCallback(
        async (
            result: unknown,
            forceSubmit = false,
            goToNextAction = true
        ) => {
            // Add data to result buffer
            resultBuffer.current.push(result || {});

            // Check if there is another round data available
            // can be forced by forceSubmit
            const hasNextRound = state && state.next_round && state.next_round.length;
            if (hasNextRound && !forceSubmit && goToNextAction) {
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
            const data: ResultData = {
                session,
                participant,
                result: mergedResults,
            };

            // Optionally add section to result data
            if (mergedResults.section) {
                data.section = mergedResults.section;
            }

            // Send data to API
            await scoreResult(data);

            // Clear resultBuffer
            resultBuffer.current = [];

            // Advance to next round
            if (goToNextAction) {
                onNext();
            }

        },
        [participant, session, onNext, state]
    );

    return onResult;
};

export default useResultHandler;
