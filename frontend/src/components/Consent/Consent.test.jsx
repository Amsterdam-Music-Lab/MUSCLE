import React from 'react';
import { fireEvent, render, waitFor } from '@testing-library/react';
import Consent from './Consent';
import { useConsent } from '../../API'
import { saveAs } from 'file-saver';
import { vi } from 'vitest';

global.Blob = vi.fn().mockImplementation((content, options) => ({
    content,
    options
}));

global.URL.createObjectURL = vi.fn();

vi.mock('file-saver', () => ({
    saveAs: vi.fn(),
}));

vi.mock('../../API', () => ({
    createConsent: vi.fn(),
    useConsent: vi.fn(),
}));

const mockBlock = {
    slug: 'test-experiment',
    loading_text: 'Loading...',
};

describe('Consent', () => {
    it('renders loading state correctly', () => {
        useConsent.mockReturnValue([null, true]); // Mock loading state
        const { getByText } = render(<Consent experiment={{ slug: 'test-experiment', loading_text: 'Loading...' }} />);
        expect(document.body.contains(getByText('Loading...'))).to.be.true;
    });

    it('renders consent text when not loading', () => {
        useConsent.mockReturnValue([null, false]);
        const { getByText } = render(<Consent text="<p>Consent Text</p>" experiment={mockBlock} />);
        expect(document.body.contains(getByText('Consent Text'))).to.be.true;
    });

    it('calls onNext when Agree button is clicked', async () => {
        useConsent.mockReturnValue([null, false]);
        const onNext = vi.fn();
        const { getByText } = render(<Consent onNext={onNext} confirm="Agree" experiment={mockBlock} />);
        fireEvent.click(getByText('Agree'));

        await waitFor(() => expect(onNext).toHaveBeenCalled());
    });

    it('triggers download when Download button is clicked', async () => {
        useConsent.mockReturnValue([null, false]);
        const { getByTestId } = render(<Consent text="<p>Consent Text</p>" experiment={mockBlock} />);
        fireEvent.click(getByTestId('download-button'));

        await waitFor(() => expect(saveAs).toHaveBeenCalled());
    });

    it('auto advances if consent is already given', () => {
        useConsent.mockReturnValue([true, false]);
        const onNext = vi.fn();
        render(<Consent onNext={onNext} experiment={mockBlock} />);
        expect(onNext).toHaveBeenCalled();
    });

    it('calculates style for consent text correctly', () => {
        useConsent.mockReturnValue([null, false]);
        Object.defineProperty(window, 'innerHeight', { writable: true, configurable: true, value: 800 });
        const { getByTestId } = render(<Consent text="<p>Consent Text</p>" experiment={mockBlock} />);
        const consentText = getByTestId('consent-text');
        expect(consentText.style.height).toBe('500px');
    });



});
