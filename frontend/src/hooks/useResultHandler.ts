import { useCallback } from "react";
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
}

interface OnResultParams {

    // If feedback form is provided
    form: Question[];
    decision_time?: number;
    config?: TrialConfig
}

/**
 * useResult provides a reusable function to handle block view data
 * - handles advancing to next round
 * - finally submits the data to the API and loads the new state
 */
const useResultHandler = ({ session, participant }: UseResultHandlerParams) => {

    const onResult = useCallback(
        async (
            result: OnResultParams,
        ) => {

            // Merge result data with data from resultBuffer
            // NB: result data with same properties will be overwritten by later results
            const mergedResults = result;

            // Create result data
            const data: ResultData = {
                session,
                participant,
                result: mergedResults,
            };

            // Send data to API
            await scoreResult(data);
        },
        [participant, session]
    );

    return onResult;
};

export type OnResultType = ReturnType<typeof useResultHandler>;

export default useResultHandler;
