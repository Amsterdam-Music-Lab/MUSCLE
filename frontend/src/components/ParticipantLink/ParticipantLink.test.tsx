import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import ParticipantLink from './ParticipantLink';

// Mock the useParticipantLink hook
const mockUseParticipantLink = vi.fn();
vi.mock('../../API', () => ({
    useParticipantLink: () => mockUseParticipantLink(),
}));

// Mock the clipboard API
const mockClipboard = {
    writeText: vi.fn(),
};
Object.defineProperty(navigator, 'clipboard', {
    value: mockClipboard,
    configurable: true,
});

describe('ParticipantLink Component', () => {
    const mockLink = {
        url: 'https://app.amsterdammusiclab.nl/experiment/participant/reload/123456/1a2b3c4d/',
        copy_message: 'Copy Link',
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders loading state', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([null, true]);
        render(<ParticipantLink />);
        expect(screen.getByTestId('loading')).toBeTruthy();
    });

    it('renders nothing when link is null', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([null, false]);
        const { container } = render(<ParticipantLink />);
        expect(container.firstChild).toBeNull();
    });

    it('renders link when available', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink />);
        expect(screen.getByRole('textbox')).toBeTruthy();
        expect(screen.getByRole('button', { name: 'Copy Link' })).toBeTruthy();
    });

    it('displays full link by default', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink />);
        const textbox = screen.getByRole('textbox') as HTMLInputElement;
        expect(textbox.value).toBe(mockLink.url);
    });

    it('displays only participant ID when participantIDOnly is true', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink participantIDOnly={true} />);
        const textbox = screen.getByRole('textbox') as HTMLInputElement;
        expect(textbox.value).toBe('123456');
    });

    it('copies link to clipboard when button is clicked', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink />);
        fireEvent.click(screen.getByRole('button', { name: 'Copy Link' }));
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(mockLink.url);
    });

    it('copies link to clipboard when button is activated with keyboard', async () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink />);
        const button = screen.getByRole('button', { name: 'Copy Link' });
        await fireEvent.keyDown(button, { key: 'Enter', code: 13, charCode: 13 });
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(mockLink.url);
    })

    it('selects input text when copying', () => {
        vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
        render(<ParticipantLink />);
        const input = screen.getByRole('textbox');
        const selectSpy = vi.spyOn(input, 'select');
        const setSelectionRangeSpy = vi.spyOn(input, 'setSelectionRange');
        fireEvent.click(screen.getByRole('button', { name: 'Copy Link' }));
        expect(selectSpy).toHaveBeenCalled();
        expect(setSelectionRangeSpy).toHaveBeenCalledWith(0, 99999);
    });
});
