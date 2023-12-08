import React from 'react';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Score from './Score';
import makeDefaultScoreProps from '../../util/testUtils/makeDefaultScoreProps';

jest.useFakeTimers();

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
            onNext: jest.fn(),
        };

        render(<Score {...props} />);
        expect(screen.getByText('Great job!')).toBeInTheDocument();
        expect(screen.getByText('Test Song')).toBeInTheDocument();
    });


    it('calls onNext after timer duration', () => {
        const onNext = jest.fn();
        render(<Score {...{ ...makeDefaultScoreProps({ timer: 5, onNext }) }} />);

        act(() => {
            jest.advanceTimersByTime(5000);
        });

        expect(onNext).toHaveBeenCalled();
    });

    it('conditionally renders elements', () => {
        const { rerender } = render(<Score {...{ ...makeDefaultScoreProps({ icon: null }) }} />);
        expect(screen.queryByTestId('icon-element')).not.toBeInTheDocument();

        rerender(<Score {...{ ...makeDefaultScoreProps({ last_song: null }) }} />);
        expect(screen.queryByText('Test Song')).not.toBeInTheDocument();
    });

    it('calls onNext when button is clicked and no timer', () => {
        const onNext = jest.fn();
        render(<Score {...{ ...makeDefaultScoreProps({ timer: null, onNext }) }} />);

        fireEvent.click(screen.getByText('Next'));
        expect(onNext).toHaveBeenCalled();
    });

});
