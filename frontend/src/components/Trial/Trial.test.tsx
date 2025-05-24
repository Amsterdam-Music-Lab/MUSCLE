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
vi.mock("@/components/survey", () => ({
    Survey: vi.fn(({ submitResult }) => (
        <div data-testid="mock-feedback-form" onClick={() => { submitResult(); }}>Mock Feedback Form</div>
    )),
}));
vi.mock("@/components/utils", () => ({
    RenderHtml: ({ html }) => <div data-testid="mock-html">{html}</div>,
}));

const feedback_form = {
    form: [{
        key: 'test_question',
        view: QuestionViews.BUTTON_ARRAY,
        question: ['What is the average speed of a Swallow?'],
        choices: { 'slow': '1 km/h', 'fast': '42 km/h' },
        style: {}
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
            playback={{ view: 'AUTOPLAY' }}
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
            feedback_form={feedback_form}
            onNext={mockOnNext}
            onResult={mockOnResult}
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
        const formless_feedback_form = {
            ...feedback_form,
            form: undefined
        };
        render(<Trial
            config={defaultConfig}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedback_form={formless_feedback_form}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
        });
    });

    it("calls onResult and onNext when form is not defined and break_round_on is met", async () => {
        const formless_feedback_form = {
            ...feedback_form,
            form: undefined
        };
        const config = {
            ...defaultConfig,
            break_round_on: { NOT: ['fast'] }
        };
        render(<Trial
            config={config}
            onNext={mockOnNext}
            onResult={mockOnResult}
            feedback_form={formless_feedback_form}
        />);
        fireEvent.click(screen.getByTestId('mock-feedback-form'));
        await waitFor(() => {
            expect(mockOnResult).toHaveBeenCalled();
            expect(mockOnNext).toHaveBeenCalled();
        });
    });
});
