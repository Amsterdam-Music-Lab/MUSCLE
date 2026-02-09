import { render, screen, fireEvent } from '@testing-library/react';
import { describe, test, expect, beforeEach, vi } from 'vitest';
import MultiPlayer from './MultiPlayer';
import PlaybackSection from "@/types/Section";

const initialState = {
    theme: {colorNeutral1: '#ffb14c', colorNeutral2: '#0cc7f1', colorNeutral3: '#2b2bee'}
};

vi.mock("../../util/stores", () => ({
    __esModule: true,
    default: (fn: any) => {

        return fn(initialState);
    },
    useBoundStore: vi.fn()
}));

describe('MultiPlayer Component', () => {
    const mockPlaySection = vi.fn();
    const mockSections: PlaybackSection[] = [
        { link: '123451', label: 'Label 1', color: 'colorNeutral1' },
        { link: '123452', label: 'Label 2', color: 'colorNeutral2' },
        { link: '123453', label: 'Label 3',  color: 'colorNeutral3' },
    ];

    const defaultProps = {
        playSection: mockPlaySection,
        sections: mockSections,
        playing: 0,
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    test('renders correct number of PlayButton components', () => {
        render(<MultiPlayer {...defaultProps} />);
        const players = screen.queryAllByRole('button');
        expect(players.length).toBe(mockSections.length);
    });

    test('applies correct class names', () => {
        const { container } = render(<MultiPlayer {...defaultProps} />);

        if (!container.firstChild) {
            throw new Error('No container.firstChild');
        }

        const classList = container.firstChild.classList;
        expect(classList.contains('aha__multiplayer')).toBe(true);
        expect(classList.contains('d-flex')).toBe(true);
        expect(classList.contains('justify-content-around')).toBe(true);
        expect(classList.contains('player-count-3')).toBe(true);
    });

    test('calls playSection with correct index when PlayButton is clicked', () => {
        render(<MultiPlayer {...defaultProps} />);
        const players = screen.queryAllByRole('button');
        fireEvent.click(players[1]);
        expect(mockPlaySection).toHaveBeenCalledWith(1);
    });

    test('applies correct label to PlayButton components', () => {
        render(<MultiPlayer {...defaultProps} />);
        expect(screen.getByText('Label 1')).toBeTruthy();
        expect(screen.getByText('Label 2')).toBeTruthy();
        expect(screen.getByText('Label 3')).toBeTruthy();
    });

    test('renders images when provided', () => {
        const sectionsWithImage = mockSections.map(section => {
            section.image = {link: '/link/to/image.png', label: 'alt text'};
            return section;
        });
        render(<MultiPlayer {...defaultProps} sections={sectionsWithImage}/>);
        expect(screen.queryAllByAltText('alt text')).toHaveLength(3);
    });

});
