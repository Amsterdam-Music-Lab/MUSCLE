import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PlayButton from './PlayButton';

describe('PlayButton Component', () => {

    const mockSection = {
        link: '/some/url.mp3',
        label: 'player label',
        color: '#000000',
        playing: false
    }

    it('renders correctly', () => {
        const { container } = render(<PlayButton section={mockSection} />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton).toBeTruthy();
        expect(container.querySelector('.playbutton-spacer')).toBeTruthy();
    });

    it('applies correct classes when not playing', () => {
        const { container } = render(<PlayButton section={mockSection} />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton.classList.contains('border-outside')).toBe(true);
        expect(playButton.classList.contains('btn')).toBe(true);
        expect(playButton.classList.contains('stop')).toBe(false);
        expect(playButton.classList.contains('disabled')).toBe(false);
    });

    it('applies correct classes when playing', () => {
        const { container } = render(<PlayButton section={mockSection} isPlaying={true} />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton.classList.contains('stop')).toBe(true);
        expect(playButton.classList.contains('disabled')).toBe(true);
    });

    it('applies custom className', () => {
        const { container } = render(<PlayButton section={mockSection} className="custom-class" />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton.classList.contains('custom-class')).toBe(true);
    });

    it('calls playSection when clicked and not disabled', () => {
        const mockPlaySection = vi.fn();

        render(<PlayButton section={mockSection} playSection={mockPlaySection} playIndex={2} />);
        const playButton = screen.getByRole('button');
        fireEvent.click(playButton);
        expect(mockPlaySection).toHaveBeenCalledWith(2);
    });

    it('does not call playSection when clicked and disabled', () => {
        const mockPlaySection = vi.fn();

        render(<PlayButton section={mockSection} playSection={mockPlaySection} disabled={true} />);
        const playButton = screen.getByRole('button');
        fireEvent.click(playButton);
        expect(mockPlaySection).not.toHaveBeenCalled();
    });

    it('calls playSection on keyDown', async () => {
        const mockPlaySection = vi.fn();

        render(<PlayButton section={mockSection} playSection={mockPlaySection} playIndex={2} />);
        const playButton = screen.getByRole('button');
        playButton.focus();
        await fireEvent.keyDown(playButton, { key: 'Enter', code: 'Enter', charCode: 13 });
        expect(mockPlaySection).toHaveBeenCalledWith(2);
    });

    it('applies disabled class when disabled prop is true', () => {
        const { container } = render(<PlayButton section={mockSection} disabled={true} />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton.classList.contains('disabled')).toBe(true);
    });

    it('has correct tabIndex', () => {
        const { container } = render(<PlayButton section={mockSection} />);
        const playButton = container.querySelector('.aha__play-button');
        expect(playButton.getAttribute('tabIndex')).toBe('0');
    });
});
