import { renderHook, act } from "@testing-library/react";
import useResultHandler from "./useResultHandler";
import { vi } from 'vitest';

import * as API from '../API';

vi.mock('../API');

describe('useResultHandler', () => {

    const mockOnNext = vi.fn();
    const initialState = { next_round: ['round2'] }; // Example initial state
    const mockSession = 'session-id';
    const mockParticipant = 'participant-id';

    it('buffers results correctly', async () => {
        const { result } = renderHook(() =>
            useResultHandler({ session: mockSession, participant: mockParticipant, onNext: mockOnNext, state: initialState })
        );

        await act(async () => {
            await result.current({ testResult: 'result1' }, false);
            await result.current({ testResult: 'result2' }, false);
        });

        expect(API.scoreResult).not.toHaveBeenCalled();

        await act(async () => {
            await result.current({ testResult: 'result3' }, true);
        });

        expect(API.scoreResult).toHaveBeenCalledWith({
            session: 'session-id',
            participant: 'participant-id',
            result: { testResult: 'result3' },
        });
    });

});
