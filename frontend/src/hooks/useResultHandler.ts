import { useRef, useCallback } from "react";
import { scoreResult } from "@/API";
import Session from "@/types/Session";
import Participant from "@/types/Participant";
import Question from "@/types/Question";
import { TrialConfig } from "@/types/Trial";

interface ResultData {
    session: Session;
    participant: Participant;
    result: unknown;
    section?: unknown;
}

interface UseResultHandlerParams {
    session: Session;
    participant: Participant;
    onNext: () => void;
    state: any;
}

interface OnResultParams {

    // If feedback form is provided
    form?: Question[];
    decision_time?: number;
    config?: TrialConfig

    // If no feedback form is provided
    result?: {
        type: string;
    }
    result_id?: string;
}

/**
 * useResult provides a reusable function to handle block view data
 * - collect results in a buffer
 * - handles advancing to next round
 * - finally submits the data to the API and loads the new state
 */
const useResultHandler = ({ session, participant }: UseResultHandlerParams) => {
    const resultBuffer = useRef([]);

    const onResult = useCallback(
        async (
            result: OnResultParams,
        ) => {
            // Add data to result buffer
            resultBuffer.current.push(result || {});

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
        },
        [participant, session]
    );

    return onResult;
};

export type OnResultType = ReturnType<typeof useResultHandler>;

export default useResultHandler;
