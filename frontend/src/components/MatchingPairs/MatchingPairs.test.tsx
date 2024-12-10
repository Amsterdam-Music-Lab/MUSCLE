import { vi, describe, beforeEach, afterEach, test, expect } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import * as API from '../../API';

import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from './MatchingPairs';

let mock: MockAdapter;

vi.mock("@/components/PlayButton/PlayCard", () => ({
    default: (props: any) => <div data-testid="play-card" {...props} />
}));

const initialState = {
    participant: 1,
    session: 1,
    setError: vi.fn(),
    block: { bonus_points: 42 },
    currentAction: () => ({ view: 'TRIAL_VIEW' }),
};

vi.mock("../../util/stores", () => ({
    __esModule: true,
    default: (fn: any) => {

        return fn(initialState);
    },
    useBoundStore: vi.fn()
}));

describe('MatchingPairs Component', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        mock = new MockAdapter(axios);
        mock.onPost().reply(200, { score: 10 });
    });

    afterEach(() => {
        mock.restore()
    })

    let mockSections = [
        { id: 1, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false },
        { id: 2, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false },
        { id: 3, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false },
        { id: 4, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false },
    ];

    const baseProps = {
        playSection: vi.fn(),
        playerIndex: 0,
        finishedPlaying: vi.fn(),
        onFinish: vi.fn(),
        stopAudioAfter: 4.0,
        showAnimation: false,
        tutorial: {
            lucky_match: 'Lucky match tutorial content',
            memory_match: 'Memory match tutorial content',
            no_match: 'No match tutorial content',
            misremembered: 'Misremembered tutorial content',
        }
    };

    test('renders correctly', () => {
        const { getByText } = render(<MatchingPairs sections={mockSections} setPlayerIndex={vi.fn()} />);
        expect(getByText('Pick a card')).not.toBeNull();
    });

    test('flips a card when clicked', async () => {
        render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={vi.fn()} />);
        const cards = screen.getAllByRole('button');

        fireEvent.click(cards[0]);

        await waitFor(() => expect(cards[0].classList.contains('turned')).toBe(true));
    });

    test('updates score after a match', async () => {
        mock.onPost().replyOnce(200, { score: 10 });
        const { getByText } = render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={vi.fn()} />);
        const cards = screen.getAllByRole('button');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);

        await waitFor(() => expect(getByText('Score: 52')).not.toBeNull());
    });

    test('has a blocking overlay in-between turns', async () => {
        mock.onPost().replyOnce(200, { score: 0 });
        render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={vi.fn()} />);
        const cards = screen.getAllByRole('button');

        await waitFor(() => expect(screen.getByTestId('overlay').style.display).toBe('none'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await new Promise(r => setTimeout(r, 1));
        expect(screen.getByTestId('overlay').style.display).toBe('block')
    });

    test('calls scoreIntermediateResult after each turn', async () => {
        mock.onPost().reply(200, { score: 10 });
        const spy = vi.spyOn(API, 'scoreIntermediateResult');
        render(<MatchingPairs {...baseProps} sections={mockSections} tutorial={undefined} setPlayerIndex={vi.fn()} />);
        const cards = screen.getAllByTestId('play-card');

        mock.onPost().reply(200, { score: 10 });
        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        await new Promise(r => setTimeout(r, 1));


        fireEvent.click(screen.getByTestId('overlay'));
        await new Promise(r => setTimeout(r, 1));

        await waitFor(() => screen.getByText('Pick a card'));
        expect(spy).toHaveBeenCalled();

        // cleanup spy
        spy.mockRestore();
    })

    test('ends the game when all pairs are matched', async () => {

        const expectedFirstScore = initialState.block.bonus_points + 10;
        const expectedSecondScore = expectedFirstScore + 20;

        mock.onPost().reply(200, { score: 10 });
        const submitResult = vi.fn();
        render(
            <MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={vi.fn()} submitResult={submitResult} />
        );
        const cards = screen.getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        await new Promise(r => setTimeout(r, 1));
        fireEvent.click(screen.getByTestId('overlay'));
        await new Promise(r => setTimeout(r, 1));

        waitFor(() => {
            expect(screen.getByTestId('score').textContent).toBe(`Score: ${expectedFirstScore}`);
            expect(cards[0].classList.contains('disabled')).toBe(true);
            expect(cards[2].classList.contains('disabled')).toBe(true);
        });

        mock.onPost().reply(200, { score: 20 });
        fireEvent.click(cards[1]);
        fireEvent.click(cards[3]);
        await new Promise(r => setTimeout(r, 1));
        fireEvent.click(screen.getByTestId('overlay'));
        await new Promise(r => setTimeout(r, 1));
        waitFor(() => {
            expect(screen.getByTestId('score').textContent).toBe(`Score: ${expectedSecondScore}`);
            expect(cards[1].classList.contains('disabled')).toBe(true);
            expect(cards[3].classList.contains('disabled')).toBe(true);
            expect(submitResult).toHaveBeenCalled();
        });
    });

    test('displays three columns when sections length is less than or equal to 6', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--three-columns')).not.toBeNull();
    });

    test('displays four columns when sections length is greater than 6', () => {
        const sections = new Array(7).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--three-columns')).toBeNull();
    });

    test('displays score feedback when scoreFeedbackDisplay is not HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).not.toBeNull();
    });

    test('does not display score feedback when scoreFeedbackDisplay is HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.HIDDEN} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).toBeNull();
    });

    test('displays score feedback on the top when scoreFeedbackDisplay is LARGE_TOP', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).toBeNull();
    });

    test('displays score feedback on the bottom right when scoreFeedbackDisplay is SMALL_BOTTOM_RIGHT', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).not.toBeNull();
    });

    describe('Tutorial Overlay Integration', () => {
        const tutorialContent = {
            lucky_match: 'Lucky match tutorial content',
            memory_match: 'Memory match tutorial content',
            no_match: 'No match tutorial content',
            misremembered: 'Misremembered tutorial content'
        };



        test('shows tutorial overlay on first lucky match', async () => {
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    tutorial={tutorialContent}
                    setPlayerIndex={vi.fn()}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // Make a lucky match
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            await waitFor(() => {
                expect(screen.getByText('Lucky match tutorial content')).toBeTruthy();
            });
        });

        test('does not show tutorial overlay for same score type twice', async () => {
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    tutorial={tutorialContent}
                    setPlayerIndex={vi.fn()}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // First lucky match
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            await waitFor(() => {
                expect(screen.getByText('Lucky match tutorial content')).toBeTruthy();
            });

            // Close the overlay
            const overlay = screen.getByRole('presentation');
            expect(overlay).toBeTruthy();
            const closeButton = overlay.querySelector('button');
            expect(closeButton).toBeTruthy();
            fireEvent.click(closeButton as Element);

            // Second lucky match
            fireEvent.click(cards[1]);
            fireEvent.click(cards[3]);

            // Wait a bit to ensure overlay doesn't appear
            await new Promise(r => setTimeout(r, 100));
            waitFor(() =>
                expect(screen.queryByText('Lucky match tutorial content')).toBeNull()
            );
        });

        test('closes tutorial overlay and finishes turn when clicking "Got it"', async () => {
            const finishedPlaying = vi.fn();
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    tutorial={tutorialContent}
                    setPlayerIndex={vi.fn()}
                    finishedPlaying={finishedPlaying}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // Make a match
            mock.onPost().reply(200, { score: 10 });
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            await waitFor(() => {
                expect(screen.getByText('Lucky match tutorial content')).toBeTruthy();
            });

            // Close the overlay
            const overlay = screen.getByRole('presentation');
            expect(overlay).toBeTruthy();
            const closeButton = overlay.querySelector('button');
            expect(closeButton).toBeTruthy();
            fireEvent.click(closeButton as Element);

            waitFor(() => {
                expect(screen.queryByText('Lucky match tutorial content')).toBeNull();
                expect(finishedPlaying).toHaveBeenCalled();
                expect(screen.getByText('Pick a card')).toBeTruthy();
            });
        });

        test('closes tutorial overlay when pressing Escape key', async () => {
            const finishedPlaying = vi.fn();
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    tutorial={tutorialContent}
                    setPlayerIndex={vi.fn()}
                    finishedPlaying={finishedPlaying}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // Make a match
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            await waitFor(() => {
                expect(screen.getByText('Lucky match tutorial content')).toBeTruthy();
            });

            // Press Escape
            fireEvent.keyDown(document, { key: 'Escape' });

            waitFor(() => {
                expect(screen.queryByText('Lucky match tutorial content')).toBeNull();
                expect(finishedPlaying).toHaveBeenCalled();
            });
        });

        test('does not show tutorial overlay when tutorial prop is not provided', async () => {
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    setPlayerIndex={vi.fn()}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // Make a match
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            // Wait a bit to ensure overlay doesn't appear
            await new Promise(r => setTimeout(r, 100));
            waitFor(() =>
                expect(screen.queryByText('Lucky match tutorial content')).toBeNull()
            );
        });

        test('shows different tutorial content for different match types', async () => {
            render(
                <MatchingPairs
                    {...baseProps}
                    sections={mockSections}
                    tutorial={tutorialContent}
                    setPlayerIndex={vi.fn()}
                />
            );
            const cards = screen.getAllByTestId('play-card');

            // First make a lucky match
            fireEvent.click(cards[0]);
            fireEvent.click(cards[2]);

            await waitFor(() => {
                expect(screen.getByText('Lucky match tutorial content')).toBeTruthy();
            });

            // Close the overlay
            const overlay = screen.getByRole('presentation');
            expect(overlay).toBeTruthy();
            const closeButton = overlay.querySelector('button');
            expect(closeButton).toBeTruthy();
            fireEvent.click(closeButton as Element);

            // Then make a memory match
            mock.onPost().replyOnce(200, { score: 20 });
            fireEvent.click(cards[1]);
            fireEvent.click(cards[3]);

            waitFor(() => {
                expect(screen.getByText('Memory match tutorial content')).toBeTruthy();
            });
        });
    });
});
