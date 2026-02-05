import { act } from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import Score from './Score';
import { vi, describe, expect, it } from 'vitest';

vi.useFakeTimers();

const makeDefaultScoreProps = (overrides = {}) => ({
    last_song: 'Test Song',
    score: 10,
    score_message: 'Great job!',
    total_score: 50,
    texts: { score: 'Score' },
    button: {label: 'Next'},
    icon: 'fa-icon',
    feedback: 'Well done!',
    timer: null,
    onNext: vi.fn(),
    ...overrides,
});


describe('Score component', () => {

    it('renders correctly', () => {
        render(<Score {...makeDefaultScoreProps({icon: null})} />);
        expect(document.body.contains(screen.getByText('Great job!'))).toBe(true);
        expect(document.body.contains(screen.getByText('Test Song'))).toBe(true);
    });


    it('calls onNext after timer duration', () => {
        const onNext = vi.fn();
        render(<Score {...{ ...makeDefaultScoreProps({ timer: 5, onNext }) }} />);

        act(() => {
            vi.advanceTimersByTime(5000);
        });

        expect(onNext).toHaveBeenCalled();
    });

    it('conditionally renders elements', () => {
        const { rerender } = render(<Score {...{ ...makeDefaultScoreProps({ icon: null }) }} />);
        expect(document.body.contains(screen.queryByTestId('icon-element'))).not.toBeTruthy();

        rerender(<Score {...{ ...makeDefaultScoreProps({ last_song: null }) }} />);
        expect(document.body.contains(screen.queryByText('Test Song'))).not.toBeTruthy();
    });

    it('calls onNext when button is clicked and no timer', () => {
        const onNext = vi.fn();
        render(<Score {...{ ...makeDefaultScoreProps({ timer: null, onNext }) }} />);

        fireEvent.click(screen.getByText('Next'));
        expect(onNext).toHaveBeenCalled();
    });

});
