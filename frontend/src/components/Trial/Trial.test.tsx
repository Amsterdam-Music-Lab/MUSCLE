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
    default: vi.fn(({ onResult }) => (
        <div data-testid="mock-feedback-form" onClick={() => onResult({ type: 'feedback' })}>Mock Feedback Form</div>
    )),
}));
vi.mock("../HTML/HTML", () => ({
    default: vi.fn(({ body }) => <div data-testid="mock-html">{body}</div>),
}));

const feedback_form = {
    form: [{
        key: 'test_question',
        view: QuestionViews.BUTTON_ARRAY,
        question: ['What is the average speed of a Swallow?'],
        choices: { 'slow': '1 km/h', 'fast': '42 km/h' }
    }],
    submit_label: 'Submit',
    skip_label: 'Skip',
    is_skippable: false
};

const defaultConfig = {
    'listen_first': false,
    'auto_advance': false,
    'response_time': 5000,
    'show_continue_button': false
};

describe('Trial', () => {
    const mockOnNext = vi.fn();
    const mockOnResult = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("renders itself", () => {
        render(<Trial
            feedback_form={feedback_form}
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        expect(screen.queryByRole('presentation')).toBeTruthy();
    });

    it("sets the class of the trial element based on config style", () => {
        const config = { ...defaultConfig, style: 'boolean' };
        render(<Trial
            feedback_form={feedback_form}
            config={config}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        const presentation = screen.queryByRole('presentation');
        expect(presentation.classList.contains('boolean')).toBe(true);
    });

    it("renders Playback component when playback prop is provided", () => {
        render(<Trial
            playback={{ somePlaybackProp: true }}
            feedback_form={feedback_form}
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        expect(screen.getByTestId('mock-playback')).toBeTruthy();
    });

    it("renders HTML component when html prop is provided", () => {
        const htmlBody = "Test HTML content";
        render(<Trial
            html={{ body: htmlBody }}
            feedback_form={feedback_form}
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        const htmlComponent = screen.getByTestId('mock-html');
        expect(htmlComponent).toBeTruthy();
        expect(htmlComponent.textContent).toBe(htmlBody);
    });

    it("renders FeedbackForm when feedback_form prop is provided", () => {
        render(<Trial
            feedback_form={feedback_form}
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        expect(screen.getByTestId('mock-feedback-form')).toBeTruthy();
    });

    it("shows continue button when config.show_continue_button is true", () => {
        const config = { ...defaultConfig, show_continue_button: true, continue_label: 'Continue' };
        render(<Trial
            config={config}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        expect(screen.getByText('Continue')).toBeTruthy();
    });

    it("calls onResult when FeedbackForm submits result", async () => {
        render(<Trial
            feedback_form={feedback_form}
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
        });
    });

    it("calls finishedPlaying when Playback component finishes", () => {
        const config = { ...defaultConfig, auto_advance: true };
        render(<Trial
            playback={{ somePlaybackProp: true }}
            config={config}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedback_form={feedback_form}
        />);
        fireEvent.click(screen.getByTestId('mock-playback'));
        expect(screen.getByTestId('mock-feedback-form')).toBeTruthy();
    });

    it("auto-advances after specified timer when config.auto_advance_timer is set", async () => {
        const config = { ...defaultConfig, auto_advance: true, auto_advance_timer: 42 };
        render(<Trial
            playback={{ view: 'BUTTON' }}
            config={config}
            onNext={mockOnNext}
            onResult={mockOnResult}
            result_id={"123"}
        />);
        fireEvent.click(screen.getByTestId('mock-playback'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
            expect(mockOnResult).toHaveBeenCalledWith(
                expect.objectContaining({ result: { type: 'time_passed' }, result_id: "123" }),
            );
        });
    });
});
