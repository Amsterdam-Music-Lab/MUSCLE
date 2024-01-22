import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import UserFeedback from './UserFeedback';
import { postFeedback } from '../../API';

// Mock the API call
jest.mock('../../API', () => ({
  postFeedback: jest.fn(),
}));

describe('UserFeedback', () => {
  const mockExperimentSlug = 'test-slug';
  const mockParticipant = { id: 1 };
  const mockFeedbackInfo = {
    header: 'Your Feedback',
    button: 'Submit',
    contact_body: 'Contact us at test@example.com',
    thank_you: 'Thank you for your feedback!'
  };

  it('renders the feedback form', () => {
    const { getByText, getByRole } = render(
      <UserFeedback
        experimentSlug={mockExperimentSlug}
        participant={mockParticipant}
        feedbackInfo={mockFeedbackInfo}
      />
    );

    expect(getByText(mockFeedbackInfo.header)).toBeInTheDocument();
    expect(getByRole('textbox')).toBeInTheDocument();
    expect(getByText(mockFeedbackInfo.button)).toBeInTheDocument();
  });

  it('allows input to be entered', () => {
    const { getByRole } = render(
      <UserFeedback
        experimentSlug={mockExperimentSlug}
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
        experimentSlug={mockExperimentSlug}
        participant={mockParticipant}
        feedbackInfo={mockFeedbackInfo}
      />
    );

    fireEvent.change(getByRole('textbox'), { target: { value: 'Great experience!' } });
    fireEvent.click(getByText(mockFeedbackInfo.button));

    await waitFor(() => {
      expect(postFeedback).toHaveBeenCalledWith({
        experimentSlug: mockExperimentSlug,
        feedback: 'Great experience!',
        participant: mockParticipant
      });
      expect(queryByText(mockFeedbackInfo.header)).not.toBeInTheDocument();
      expect(getByText(mockFeedbackInfo.thank_you)).toBeInTheDocument();
    });
  });
});
