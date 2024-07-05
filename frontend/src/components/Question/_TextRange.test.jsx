import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import TextRange from './_TextRange'; // Adjust the import path as necessary

// Mock the dependencies
vi.mock('react-rangeslider', () => ({
    default: ({ value, onChange, min, max }) => (
        <input
            type="range"
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
            min={min}
            max={max}
            data-testid="mock-slider"
        />
    ),
}));

vi.mock('./_RangeLimits', () => ({
    default: ({ minVal, maxVal }) => (
        <div data-testid="mock-range-limits">
            {minVal} - {maxVal}
        </div>
    ),
}));

vi.mock('./_RangeTitle', () => ({
    default: ({ question, value }) => (
        <div data-testid="mock-range-title">
            {question.title} - {value}
        </div>
    ),
}));

describe('TextRange Component', () => {
    const mockQuestion = {
        title: 'Test Question',
        choices: {
            '1': 'Choice 1',
            '2': 'Choice 2',
            '3': 'Choice 3',
        },
    };

    it('renders correctly with empty value', () => {
        const { getByTestId } = render(
            <TextRange question={mockQuestion} value="" onChange={() => { }} />
        );

        const slider = getByTestId('mock-slider');
        expect(slider).toBeTruthy();
        expect(slider.value).toBe('10'); // (3 choices * 5) - 5 = 10
    });

    it('renders correctly with a selected value', () => {
        const { getByTestId } = render(
            <TextRange question={mockQuestion} value="2" onChange={() => { }} />
        );

        const slider = getByTestId('mock-slider');
        expect(slider).toBeTruthy();
        expect(slider.value).toBe('10'); // Index 1 * 10 = 10
    });

    it('calls onChange with correct value when slider changes', async () => {
        const mockOnChange = vi.fn();
        const { getByTestId } = render(
            <TextRange question={mockQuestion} value="" onChange={mockOnChange} />
        );

        const slider = getByTestId('mock-slider');
        fireEvent.change(slider, { target: { value: '5' } });

        await vi.waitFor(() => expect(mockOnChange).toHaveBeenCalledTimes(1));
        expect(mockOnChange).toHaveBeenCalledWith('2');
    });

    it('renders RangeLimits with correct min and max values', () => {
        const { getByTestId } = render(
            <TextRange question={mockQuestion} value="" onChange={() => { }} />
        );

        const rangeLimits = getByTestId('mock-range-limits');
        expect(rangeLimits.textContent).toBe('Choice 1 - Choice 3');
    });

    it('renders RangeTitle with correct props', () => {
        const { getByTestId } = render(
            <TextRange question={mockQuestion} value="2" onChange={() => { }} emphasizeTitle={true} />
        );

        const rangeTitle = getByTestId('mock-range-title');
        expect(rangeTitle.textContent).toBe('Test Question - 2');
    });

    it('applies empty class when value is empty', () => {
        const { container } = render(
            <TextRange question={mockQuestion} value="" onChange={() => { }} />
        );

        expect(container.firstChild.classList.contains('empty')).toBe(true);
    });

    it('does not apply empty class when value is set', () => {
        const { container } = render(
            <TextRange question={mockQuestion} value="2" onChange={() => { }} />
        );

        expect(container.firstChild.classList.contains('empty')).toBe(false);
    });
});
