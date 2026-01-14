import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/react';
import Number from './_Number';

describe('Number component', () => {
    const defaultProps = {
        question: {
            minValue: 0,
            maxValue: 100,
        },
        onChange: vi.fn(),
    };

    it('handles number input type correctly', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                minValue: 0,
                maxValue: 100,
            },
            onChange,
        };
        render(<Number {...props} />);
        const input = screen.getByRole('spinbutton');
        fireEvent.change(input, { target: { value: '50' } });
        expect(onChange).toHaveBeenCalledWith('50');
    });

    it('respects min and max values for number input', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                minValue: 0,
                maxValue: 100,
            },
            onChange,
        };
        render(<Number {...props} />);
        const input = screen.getByRole('spinbutton');
        fireEvent.change(input, { target: { value: '150' } });
        expect(onChange).not.toHaveBeenCalled();
    });

    it('throws an error when min_value or max_value is not provided for number input', () => {
        const props = {
            ...defaultProps,
            question: {
                minValue: 0,
            },
        };
        expect(() => render(<Number {...props} />)).toThrow('min_value and max_value are required for the Number component');

        const props2 = {
            ...defaultProps,
            question: {
                maxValue: 100,
            },
        };
        expect(() => render(<Number {...props2} />)).toThrow('min_value and max_value are required for the Number component');

        const props3 = {
            ...defaultProps,
            question: {
                minValue: 0,
                maxValue: null,
            },
        };
        expect(() => render(<Number {...props3} />)).toThrow('min_value and max_value are required for the Number component');

        const props4 = {
            ...defaultProps,
            question: {
                minValue: 0,
                maxValue: undefined,
            },
        };
        expect(() => render(<Number {...props4} />)).toThrow('min_value and max_value are required for the Number component');

        const props5 = {
            ...defaultProps,
            question: {
                minValue: 0,
                maxValue: 100,
            },
        };
        expect(() => render(<Number {...props5} />)).not.toThrow();
    });
});
