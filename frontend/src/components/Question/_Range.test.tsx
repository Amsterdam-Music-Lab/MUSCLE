import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/react';
import Range from './_Range';

describe('Range component', () => {
    const defaultProps = {
        question: {
            minValue: 0,
            maxValue: 100,
        },
        value: 50,
        onChange: vi.fn(),
    };

    it('renders correctly with given props', () => {
        render(<Range {...defaultProps} />);
        expect(screen.getByText('50')).toBeTruthy();
        expect(screen.getByText('0')).toBeTruthy();
        expect(screen.getByText('100')).toBeTruthy();
    });

    it('displays arrow icon when value is empty', () => {
        render(<Range {...defaultProps} value={undefined} />);
        expect(screen.getByText('↔')).toBeTruthy();
    });

    it('calls onChange when slider value changes', () => {
        render(<Range {...defaultProps} />);
        const slider = document.querySelector('.rangeslider-horizontal') as HTMLElement;
        fireEvent.mouseDown(slider, { clientX: 75 });
        expect(defaultProps.onChange).toHaveBeenCalled();
    });

    it('uses middle value when value prop is empty', () => {
        render(<Range {...defaultProps} value={undefined} />);
        const slider = document.querySelector('.rangeslider-horizontal') as HTMLElement;
        expect(slider.attributes['aria-valuenow'].value).toBe('50');
    });

    it('throws an error when minValue or maxValue is not provided', () => {
        const props = { ...defaultProps, question: { minValue: 0 } };
        expect(() => render(<Range {...props} />)).toThrow('minValue and maxValue are required for the Range component');

        const props2 = { ...defaultProps, question: { maxValue: 100 } };
        expect(() => render(<Range {...props2} />)).toThrow('minValue and maxValue are required for the Range component');

        const props3 = { ...defaultProps, question: { minValue: 0, maxValue: null } };
        expect(() => render(<Range {...props3} />)).toThrow('minValue and maxValue are required for the Range component');

        const props4 = { ...defaultProps, question: { minValue: 0, maxValue: undefined } };
        expect(() => render(<Range {...props4} />)).toThrow('minValue and maxValue are required for the Range component');

        const props5 = { ...defaultProps, question: { minValue: 0, maxValue: 100 } };
        expect(() => render(<Range {...props5} />)).not.toThrow();
    });
});
