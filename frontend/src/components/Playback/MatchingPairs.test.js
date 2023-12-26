import React from 'react';
import { render } from '@testing-library/react';
import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from './MatchingPairs';

vi.mock("../../util/stores", () => ({
    __esModule: true,
    default: jest.fn(),
    useBoundStore: jest.fn()
}));

vi.mock("@/components/PlayButton/PlayCard", () => ({
    default: props => <div data-testid="play-card" {...props} />
}));

describe('MatchingPairs Component', () => {

    const baseProps = {
        playSection: vi.fn(),
        playerIndex: 0,
        finishedPlaying: vi.fn(),
        onFinish: vi.fn(),
        stopAudioAfter: 4.0,
        submitResult: vi.fn(),
        showAnimation: false
    };

    it('displays three columns when sections length is less than or equal to 6', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);

        expect(document.body.contains(container.querySelector('.playing-board--three-columns'))).to.be.true;
    });

    it('displays four columns when sections length is greater than 6', () => {
        const sections = new Array(7).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);

        expect(document.body.contains(container.querySelector('.playing-board--three-columns'))).to.not.be.true;
    });

    it('displays score feedback when scoreFeedbackDisplay is not HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).toBeInTheDocument();
    });

    it('does not display score feedback when scoreFeedbackDisplay is HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.HIDDEN} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).not.toBeInTheDocument();
    });

    it('displays score feedback on the top when scoreFeedbackDisplay is LARGE_TOP', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).not.toBeInTheDocument();
    });

    it('displays score feedback on the bottom right when scoreFeedbackDisplay is SMALL_BOTTOM_RIGHT', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).toBeInTheDocument();
    });
});
