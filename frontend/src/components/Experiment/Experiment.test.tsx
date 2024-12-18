import { MemoryRouter } from 'react-router-dom';
import { act, render, screen, waitFor } from '@testing-library/react';
import { vi, it, expect, describe, beforeEach } from 'vitest';

import Experiment from './Experiment';

let mockUseParams = vi.fn();

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useParams: () => mockUseParams()
    };
});

// Mock useGet
const mockFetchData = vi.fn();
let mockData: any = null;
let mockLoading = false;

// Mock '@/API' module
vi.mock('@/API', async () => {
    const actual = await vi.importActual<typeof import('@/API')>('@/API');
    return {
        ...actual,
        useExperiment: () => [mockData, mockLoading, mockFetchData],
        useConsent: () => [null, false],
    };
});

const getBlock = (overrides = {}) => {
    return {
        slug: 'some_slug',
        name: 'Some Block',
        ...overrides
    };
}

const block1 = getBlock({
    slug: 'some_slug',
    name: 'Some Block'
});

const theme = {
    backgroundUrl: 'someurl.com',
    bodyFontUrl: 'bodyFontUrl.com',
    description: 'Description of the theme',
    headingFontUrl: 'headingFontUrl.com',
    logo: {
        title: 'Logo title',
        description: 'Logo description',
        file: 'logo.jpg',
        alt: 'Logo alt',
        href: 'https://www.example.com',
        rel: 'noopener noreferrer',
        target: '_blank'
    },
    name: 'Awesome theme',
    footer: {
        disclaimer: 'disclaimer',
        logos: [
            {
                'file': 'some/logo.jpg',
                'href': 'some.url.net',
                'alt': 'Our beautiful logo',
            }
        ],
        privacy: 'privacy'
    }
}

const blockWithAllProps = getBlock({ image: 'some_image.jpg', description: 'Some description' });

describe('Experiment', () => {

    beforeEach(() => {
        mockUseParams.mockReturnValue({
            name: 'some_experiment', description: 'Some description',
            slug: 'some_experiment', languages: [{ code: 'en', label: 'English' }, { code: 'nl', label: 'Dutch' }], language: 'en'
        });

        // Reset mock data and loading before each test
        mockData = {
            name: 'some_experiment',
            description: 'Some description',
            slug: 'some_experiment',
            consent: {
                text: 'This is our consent form!',
                title: 'Consent form',
                confirm: 'I agree',
                deny: 'I disagree',
                view: 'CONSENT'
            },
            dashboard: [],
            nextBlock: block1,
            theme,
            languages: [
                { code: 'en', label: 'English' },
                { code: 'nl', label: 'Dutch' },
            ],
            language: 'en',
        };
        mockLoading = false;
        mockFetchData.mockClear();
    });

    it('forwards to a single block if it receives an empty dashboard array', async () => {
        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>);
        await waitFor(() => {
            expect(screen.queryByRole('menu')).toBeFalsy();
        })
    });

    it('shows a loading spinner while loading', () => {
        mockLoading = true;
        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('.loader-container')).not.toBeNull();
        })
    });

    it('shows the image if it is available', () => {
        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('img')).not.toBeNull();
        })
    });

    it('shows the description if it is available', () => {
        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );
        waitFor(() => {
            const description = screen.getByText('Some description');
            expect(description).not.toBeNull();
        })
    });

    it('shows consent first if available', async () => {
        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(document.querySelector('.consent-text')).not.toBeNull();
        })
    });

    it('shows a footer if a theme with footer is available', async () => {
        mockData = {
            ...mockData,
            dashboard: [blockWithAllProps],
            nextBlock: block1,
            consent: null,
            theme,
        };

        render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(document.querySelector('.aha__footer')).not.toBeNull();
        })
    })

    it('re-fetches the experiment on switch language', async () => {
        const rendered = render(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );

        // Find the language switcher and buttons
        const languageSwitcher = screen.getByTestId('language-switcher');
        const languageSwitchButtons = languageSwitcher.querySelectorAll('button');

        // mock fetch data to return the new language
        mockFetchData.mockImplementation(() => {
            mockData = {
                ...mockData,
                language: 'nl'
            };
        });

        // Click the second language button (assuming index 1 is 'nl')
        act(() => {
            languageSwitchButtons[1].click();
        });

        // Wait for re-fetch
        await waitFor(() => {
            expect(mockFetchData).toHaveBeenCalledTimes(1);
            expect(mockFetchData).toHaveBeenCalledWith({ language: 'nl' });
        });

        rendered.rerender(
            <MemoryRouter>
                <Experiment />
            </MemoryRouter>
        );

        // Click the same language button again; fetchData should not be called again
        act(() => {
            languageSwitchButtons[1].click();
        });

        await waitFor(() => {
            expect(mockFetchData).toHaveBeenCalledTimes(1);
        });

        // Click the first language button (index 0 is 'en')
        act(() => {
            languageSwitchButtons[0].click();
        });

        // Wait for re-fetch
        await waitFor(() => {
            expect(mockFetchData).toHaveBeenCalledTimes(2);
            expect(mockFetchData).toHaveBeenCalledWith({ language: 'en' });
        });
    });
})
