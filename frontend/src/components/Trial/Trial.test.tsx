import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { QuestionViews } from "@/types/Question";
import Trial from "./Trial";

vi.mock("../../util/stores");
vi.mock("../Playback/Playback", () => ({
    default: vi.fn(({ finishedPlaying, onPreloadReady }) => (
        <div data-testid="mock-playback" onClick={() => {
            finishedPlaying();
            onPreloadReady();
        }}>Mock Playback</div>
    )),
}));
vi.mock("../FeedbackForm/FeedbackForm", () => ({
    default: vi.fn(({ submitResult }) => (
        <div data-testid="mock-feedback-form" onClick={() => { submitResult(); }}>Mock Feedback Form</div>
    )),
}));
vi.mock("../HTML/HTML", () => ({
    default: vi.fn(({ body }) => <div data-testid="mock-html">{body}</div>),
}));

const feedbackForm = {
    form: [{
        key: 'test_question',
        view: QuestionViews.BUTTON_ARRAY,
        question: ['What is the average speed of a Swallow?'],
        choices: { 'slow': '1 km/h', 'fast': '42 km/h' },
        style: {}
    }],
    submitButton: {label: 'Submit'},
    skipButton: {label: 'Skip'},
};

const defaultConfig = {
    'listenFirst': false,
    'autoAdvance': false,
    'responseTime': 5000,
    'continueButton': undefined
};

describe('Trial', () => {
    const mockOnNext = vi.fn();
    const mockOnResult = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("renders itself", () => {
        render(<Trial
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={feedbackForm}
            {...defaultConfig}
        />);
        expect(screen.queryByRole('presentation')).toBeTruthy();
    });

    it("renders Playback component when playback prop is provided", () => {
        render(<Trial
            playback={{ somePlaybackProp: true }}
            feedbackForm={feedbackForm}
            {...defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        expect(screen.getByTestId('mock-playback')).toBeTruthy();
    });

    it("renders HTML component when html prop is provided", () => {
        const htmlBody = "Test HTML content";
        render(<Trial
            html={{ body: htmlBody }}
            feedbackForm={feedbackForm}
            {...defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        const htmlComponent = screen.getByTestId('mock-html');
        expect(htmlComponent).toBeTruthy();
        expect(htmlComponent.textContent).toBe(htmlBody);
    });

    it("renders FeedbackForm when feedback_form prop is provided", () => {
        render(<Trial
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={feedbackForm}
            {...defaultConfig}
        />);
        expect(screen.getByTestId('mock-feedback-form')).toBeTruthy();
    });

    it("shows continue button when continueButton is provided", () => {
        const config = { ...defaultConfig, show_continue_button: true, continue_label: 'Continue' };
        render(<Trial
            onNext={mockOnNext}
            onResult={mockOnResult}
            continueButton={{label: "Continue"}}
        />);
        expect(screen.getByText('Continue')).toBeTruthy();
    });

    it("calls onResult when FeedbackForm submits result", async () => {
        render(<Trial
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={feedbackForm}
            {...defaultConfig}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
        });
    });

    it("calls finishedPlaying when Playback component finishes", () => {
        const config = { ...defaultConfig, auto_advance: true };
        render(<Trial
            playback={{ view: 'AUTOPLAY' }}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={feedbackForm}
            {...defaultConfig}
        />);
        fireEvent.click(screen.getByTestId('mock-playback'));
        expect(screen.getByTestId('mock-feedback-form')).toBeTruthy();
    });

    it("auto-advances after specified timer when autoAdvance is true", async () => {
        render(<Trial
            playback={{ view: 'BUTTON' }}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={feedbackForm}
            autoAdvance={true}
            responseTime={0.2}
            />);
        fireEvent.click(screen.getByTestId('mock-playback'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
            expect(mockOnResult).toHaveBeenCalledWith(
                expect.objectContaining({
                    decision_time: expect.any(Number),
                    form: expect.arrayContaining([
                        expect.objectContaining({
                            key: 'test_question',
                            value: 'TIMEOUT'
                        })
                    ])
                })
            );
        });
    });

    it("calls onResult when form is not defined", async () => {
        const formlessFeedbackForm = {
            ...feedbackForm,
            form: undefined
        };
        render(<Trial
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={formlessFeedbackForm}
            {...defaultConfig}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
        });
    });

    it("calls onResult and onNext when form is not defined and breakRoundOn is met", async () => {
        const formlessFeedbackForm = {
            ...feedbackForm,
            form: undefined
        };
        render(<Trial
            {...defaultConfig}
            breakRoundOn={{ NOT: ['fast'] }}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedbackForm={formlessFeedbackForm}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
            expect(mockOnNext).toHaveBeenCalled();
        });
    });
});
