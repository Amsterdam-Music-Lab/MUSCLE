import React from 'react';
import { vi } from 'vitest';
import { render } from '@testing-library/react';

import Playback from './Playback';

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

    let playbackArgs = {
        view: 'BUTTON',
        show_animation: false,
        instruction: 'Listen, just listen!',
        play_method: 'HTML',
        preload_message: 'Get ready',
        sections: [{id: 13, url: 'some/fancy/tune.mp3'}]
    };

    it('renders itself', () => {
        const { container } = render(
        <Playback 
            {... basicProps} playbackArgs={playbackArgs}
        />);
        expect(document.body.contains(container.querySelector('.aha__playback'))).to.be.true;
    });

})