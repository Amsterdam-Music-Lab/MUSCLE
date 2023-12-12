import React from 'react';
import { render } from '@testing-library/react';
import MatchingPairs from './MatchingPairs';

jest.mock("../PlayButton/PlayCard", () => (props) => (
    <div data-testid="play-card" {...props} />
));

describe('MatchingPairs Component', () => {

    const baseProps = {
        playSection: jest.fn(),
        playerIndex: 0,
        finishedPlaying: jest.fn(),
        stopAudioAfter: jest.fn(),
        submitResult: jest.fn(),
    };

    it('displays two columns when sections length is less than or equal to 6', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--two-columns')).toBeInTheDocument();
    });

    it('displays four columns when sections length is greater than 6', () => {
        const sections = new Array(7).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--two-columns')).not.toBeInTheDocument();
    });
});
