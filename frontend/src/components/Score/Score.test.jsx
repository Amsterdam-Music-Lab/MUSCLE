import React, { act } from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import Score from './Score';
import makeDefaultScoreProps from '../../util/testUtils/makeDefaultScoreProps';
import { vi } from 'vitest';

vi.useFakeTimers();

describe('Score component', () => {

    it('renders correctly', () => {
        const props = {
            last_song: 'Test Song',
            score: 10,
            score_message: 'Great job!',
            total_score: 50,
            texts: { score: 'Score', next: 'Next' },
            icon: null,
            feedback: 'Well done!',
            timer: null,
            onNext: vi.fn(),
        };

        render(<Score {...props} />);
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
        expect(document.body.contains(screen.queryByTestId('icon-element'))).to.not.be.true;

        rerender(<Score {...{ ...makeDefaultScoreProps({ last_song: null }) }} />);
        expect(document.body.contains(screen.queryByText('Test Song'))).to.not.be.true;
    });

    it('calls onNext when button is clicked and no timer', () => {
        const onNext = vi.fn();
        render(<Score {...{ ...makeDefaultScoreProps({ timer: null, onNext }) }} />);

        fireEvent.click(screen.getByText('Next'));
        expect(onNext).toHaveBeenCalled();
    });

});
