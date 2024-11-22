import { renderHook } from '@testing-library/react';
import { vi, describe, beforeEach, test, expect } from 'vitest';
import useHeadDataFromExperiment from './useHeadDataFromExperiment';
import IExperiment from '@/types/Experiment';

describe('useHeadDataFromExperiment', () => {
    const mockSetHeadData = vi.fn();
    const mockResetHeadData = vi.fn();

    beforeEach(() => {
        vi.resetAllMocks();
        // Mock window.location
        Object.defineProperty(window, 'location', {
            value: { href: 'https://example.com/experiment' },
            writable: true
        });
    });

    test('should set head data when experiment is provided', () => {
        const mockExperiment: IExperiment = {
            name: 'Test Experiment',
            description: '<p>This is a <strong>test</strong> description</p>',
            theme: {
                logo: {
                    file: '/test-logo.jpg'
                }
            }
        } as IExperiment;

        renderHook(() => useHeadDataFromExperiment(mockExperiment, mockSetHeadData, mockResetHeadData));

        expect(mockSetHeadData).toHaveBeenCalledWith({
            title: 'Test Experiment',
            description: 'This is a test description',
            image: '/test-logo.jpg',
            url: 'https://example.com/experiment',
            structuredData: {
                "@type": "Experiment",
            },
        });
    });

    test('should use default image when theme logo is not provided', () => {
        const mockExperiment: IExperiment = {
            name: 'Test Experiment',
            description: 'Test description',
        } as IExperiment;

        renderHook(() => useHeadDataFromExperiment(mockExperiment, mockSetHeadData, mockResetHeadData));

        expect(mockSetHeadData).toHaveBeenCalledWith(expect.objectContaining({
            image: "/images/aml-logolarge-1200x630.jpg",
        }));
    });

    test('should not set head data when experiment is null', () => {
        renderHook(() => useHeadDataFromExperiment(null, mockSetHeadData, mockResetHeadData));

        expect(mockSetHeadData).not.toHaveBeenCalled();
    });

    test('should reset head data on unmount', () => {
        const { unmount } = renderHook(() => useHeadDataFromExperiment({} as IExperiment, mockSetHeadData, mockResetHeadData));

        unmount();

        expect(mockResetHeadData).toHaveBeenCalled();
    });
});
