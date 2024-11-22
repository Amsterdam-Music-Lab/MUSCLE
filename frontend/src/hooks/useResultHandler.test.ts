import { act } from "react";
import { renderHook, } from "@testing-library/react";
import useResultHandler from "./useResultHandler";
import { vi, beforeEach, describe, it, expect, } from 'vitest';

import { scoreResult } from '@/API';
import Session from "@/types/Session";
import Participant from "@/types/Participant";
import { QuestionViews } from "@/types/Question";

vi.mock('@/API');

describe('useResultHandler', () => {

    const mockSession: Session = { id: 42 };
    const mockParticipant: Participant = { id: 13, hash: 'hash', csrf_token: 'token', participant_id_url: 'url', country: 'country' };


    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should call scoreResult with correct data', async () => {
        const { result } = renderHook(() =>
            useResultHandler({
                session: mockSession,
                participant: mockParticipant,
            })
        );

        const mockResult = {
            form: [{ id: 'q1', type: 'text', key: 'test_question', value: 'test', question: 'What is the average speed of a Swallow?', view: QuestionViews.BUTTON_ARRAY, choices: { 'slow': '1 km/h', 'fast': '42 km/h' } }],
            decision_time: 1000,
            config: { trialType: 'A' },
        };

        await act(async () => {
            await result.current(mockResult);
        });

        expect(scoreResult).toHaveBeenCalledWith({
            session: mockSession,
            participant: mockParticipant,
            result: mockResult,
        });
    });

    it('should not include section in data if not provided', async () => {
        const { result } = renderHook(() =>
            useResultHandler({
                session: mockSession,
                participant: mockParticipant,
            })
        );

        const mockResult = {
            result: { type: 'failure' },
        };

        await act(async () => {
            await result.current(mockResult);
        });

        expect(scoreResult).toHaveBeenCalledWith({
            session: mockSession,
            participant: mockParticipant,
            result: mockResult,
        });
        expect(scoreResult).not.toHaveBeenCalledWith(
            expect.objectContaining({ section: expect.anything() })
        );
    });


});
