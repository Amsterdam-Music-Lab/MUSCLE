import { vi, describe, it, expect, } from 'vitest';
import { render, fireEvent, waitFor } from '@testing-library/react';
import UserFeedback from './UserFeedback';
import { postFeedback } from '../../API';

// Mock the API call
vi.mock('../../API', () => ({
    postFeedback: vi.fn(),
}));

describe('UserFeedback', () => {
    const mockBlockSlug = 'test-slug';
    const mockParticipant = { id: 1 };
    const mockFeedbackInfo = {
        header: 'Your Feedback',
        button: 'Submit',
        contact_body: 'Contact us at test@example.com',
        thank_you: 'Thank you for your feedback!',
        show_float_button: true,
    };

    it('renders the feedback form', () => {
        const { getByText, getByRole } = render(
            <UserFeedback
                blockSlug={mockBlockSlug}
                participant={mockParticipant}
                feedbackInfo={mockFeedbackInfo}
            />
        );

        expect(getByText(mockFeedbackInfo.header)).toBeTruthy();
        expect(getByRole('textbox')).toBeTruthy();
        expect(getByText(mockFeedbackInfo.button)).toBeTruthy();
    });

    it('allows input to be entered', () => {
        const { getByRole } = render(
            <UserFeedback
                blockSlug={mockBlockSlug}
                participant={mockParticipant}
                feedbackInfo={mockFeedbackInfo}
            />
        );

        const input = getByRole('textbox');
        fireEvent.change(input, { target: { value: 'Great experience!' } });

        expect(input.value).toBe('Great experience!');
    });

    it('submits feedback and shows thank you message', async () => {
        postFeedback.mockResolvedValueOnce({}); // Mocking resolved promise

        const { getByText, getByRole, queryByText } = render(
            <UserFeedback
                blockSlug={mockBlockSlug}
                participant={mockParticipant}
                feedbackInfo={mockFeedbackInfo}
            />
        );

        fireEvent.change(getByRole('textbox'), { target: { value: 'Great experience!' } });
        fireEvent.click(getByText(mockFeedbackInfo.button));

        await waitFor(() => {
            expect(postFeedback).toHaveBeenCalledWith({
                blockSlug: mockBlockSlug,
                feedback: 'Great experience!',
                participant: mockParticipant
            });
            expect(queryByText(mockFeedbackInfo.header)).toBeNull();
            expect(getByText(mockFeedbackInfo.thank_you)).toBeTruthy();
        });
    });
});
