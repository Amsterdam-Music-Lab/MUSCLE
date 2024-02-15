import React from 'react';
import { render } from '@testing-library/react';

import Playback from './Playback';

jest.mock("../../util/stores");

describe('Playback', () => {

    const basicProps = {
        autoAdvance: false,
        responseTime: 42,
        onPreloadReady: jest.fn(),
        startedPlaying: jest.fn(),
        finishedPlaying: jest.fn(),
        submitResult: jest.fn(),
    }

    let playbackArgs = {
        view: 'BUTTON',
        show_animation: false,
        instruction: 'Listen, just listen!',
        play_method: 'HTML',
        ready_time: 1,
        preload_message: 'Get ready',
        sections: [{id: 13, url: 'some/fancy/tune.mp3'}]
    };

    it('renders itself', () => {
        const { container } = render(
        <Playback 
            {... basicProps} playbackArgs={playbackArgs}
        />);
        expect(container.querySelector('.aha__playback')).toBeInTheDocument();
    });

    it('shows Preload during ready_time', () => {
        const { container } = render(
        <Playback 
            {... basicProps} playbackArgs={playbackArgs}
        />);
        expect(container.querySelector('.aha__listen')).toBeInTheDocument();
    });

})