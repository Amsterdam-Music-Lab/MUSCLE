import { describe, expect, it, vi } from 'vitest';
import { render } from '@testing-library/react';

import Playback from './Playback';
import { PlaybackAction } from '@/types/Playback';

vi.mock("../../util/stores");

describe('Playback', () => {

    const basicProps = {
        autoAdvance: false,
        responseTime: 42,
        onPreloadReady: vi.fn(),
        startedPlaying: vi.fn(),
        finishedPlaying: vi.fn(),
        submitResult: vi.fn(),
    }

    let playbackAction: PlaybackAction = {
        view: 'BUTTON',
        showAnimation: false,
        mute: false,
        instruction: 'Listen, just listen!',
        preloadMessage: 'Get ready',
        sections: [{ link: 'some/fancy/tune.mp3', label: '', playMethod: 'HTML', playFrom: 0}],
    };

    it('renders itself', () => {
        const { container } = render(
            <Playback
                {...{...basicProps, ...playbackAction}}
            />);
        expect(document.body.contains(container.querySelector('.aha__playback'))).toBe(true);
    });

})
