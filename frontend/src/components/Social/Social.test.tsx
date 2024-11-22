import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Social from './Social'; // Adjust the import path as necessary
import ISocial from '@/types/Social';

// Mock the next-share components
vi.mock('next-share', () => ({
    FacebookShareButton: ({ children }: React.ComponentProps<'div'>) => <div data-testid="facebook-share">{children}</div>,
    TwitterShareButton: ({ children }: React.ComponentProps<'div'>) => <div data-testid="twitter-share">{children}</div>,
    WeiboShareButton: ({ children }: React.ComponentProps<'div'>) => <div data-testid="weibo-share">{children}</div>,
    WhatsappShareButton: ({ children }: React.ComponentProps<'div'>) => <div data-testid="whatsapp-share">{children}</div>,
}));

describe('Social Component', () => {
    const mockSocial: ISocial = {
        channels: ['facebook', 'whatsapp', 'twitter', 'weibo', 'share', 'clipboard'],
        url: 'https://example.com',
        content: 'Check this out!',
        tags: ['test', 'vitest'],
    };

    beforeEach(() => {
        // Reset all mocks before each test
        vi.resetAllMocks();
    });

    it('renders all social media buttons when all apps are included', () => {
        render(<Social social={mockSocial} />);
        expect(document.querySelector('.fa-facebook-f')).toBeDefined();
        expect(document.querySelector('.fa-whatsapp')).toBeDefined();
        expect(document.querySelector('.fa-x-twitter')).toBeDefined();
        expect(document.querySelector('.fa-weibo')).toBeDefined();
    });

    it('renders only specified social media buttons', () => {
        const limitedSocial: ISocial = { ...mockSocial, channels: ['facebook', 'twitter'] };
        render(<Social social={limitedSocial} />);
        expect(document.querySelector('.fa-facebook-f')).toBeDefined();
        expect(document.querySelector('.fa-x-twitter')).toBeDefined();
        expect(document.querySelector('.fa-whatsapp')).toBeNull();
        expect(document.querySelector('.fa-weibo')).toBeNull();
    });

    it('renders share button when navigator.share is available', () => {
        // Mock navigator.share and navigator.canShare
        Object.defineProperty(window.navigator, 'share', {
            value: vi.fn().mockResolvedValue(undefined),
            configurable: true
        });
        Object.defineProperty(window.navigator, 'canShare', {
            value: vi.fn().mockReturnValue(true),
            configurable: true
        });

        render(<Social social={mockSocial} />);
        expect(screen.getByTestId('navigator-share')).toBeDefined();
    });

    it('calls navigator.share when share button is clicked', () => {
        const shareMock = vi.fn().mockResolvedValue(undefined);
        Object.defineProperty(window.navigator, 'share', {
            value: shareMock,
            configurable: true
        });
        Object.defineProperty(window.navigator, 'canShare', {
            value: vi.fn().mockReturnValue(true),
            configurable: true
        });

        render(<Social social={mockSocial} />);
        fireEvent.click(screen.getByTestId('navigator-share'));
        expect(shareMock).toHaveBeenCalledWith({
            text: mockSocial.content,
            url: mockSocial.url
        });
    });

    it('renders clipboard button and calls navigator.clipboard.writeText when clicked', async () => {
        const writeTextMock = vi.fn().mockResolvedValue(undefined);
        Object.defineProperty(navigator, 'clipboard', {
            value: { writeText: writeTextMock },
            configurable: true
        });

        render(<Social social={mockSocial} />);
        const clipboardButton = screen.getByTestId('clipboard-share');
        expect(clipboardButton).toBeDefined();

        fireEvent.click(clipboardButton);
        expect(writeTextMock).toHaveBeenCalledWith(mockSocial.url);
    });
});
