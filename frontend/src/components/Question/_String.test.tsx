import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen, createEvent } from '@testing-library/react';
import String from './_String';

describe('String component', () => {
    const defaultProps = {
        question: {
            input_type: 'text',
            max_length: 100,
        },
        onChange: vi.fn(),
    };

    it('renders correctly with default props', () => {
        render(<String {...defaultProps} />);
        const input = screen.getByRole('textbox');
        expect(input).toBeDefined();
        expect(input).to.equal(document.activeElement);

    });

    it('calls onChange when input value changes', () => {
        const onChange = vi.fn();
        render(<String {...defaultProps} onChange={onChange} />);
        const input = screen.getByRole('textbox');
        fireEvent.change(input, { target: { value: 'test' } });
        expect(onChange).toHaveBeenCalledWith('test');
    });

    it('prevents default behavior on Enter key press', () => {
        render(<String {...defaultProps} />);
        const input = screen.getByRole('textbox');
        const myEvent = createEvent.keyDown(input, { key: 'Enter' });
        const preventDefaultMock = vi.fn();
        myEvent.preventDefault = preventDefaultMock;
        fireEvent(input, myEvent);
        expect(preventDefaultMock).toHaveBeenCalled();
    });

    it('handles number input type correctly', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
                max_value: 100,
            },
            onChange,
        };
        render(<String {...props} />);
        const input = screen.getByRole('spinbutton');
        fireEvent.change(input, { target: { value: '50' } });
        expect(onChange).toHaveBeenCalledWith('50');
    });

    it('respects min and max values for number input', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
                max_value: 100,
            },
            onChange,
        };
        render(<String {...props} />);
        const input = screen.getByRole('spinbutton');
        fireEvent.change(input, { target: { value: '150' } });
        expect(onChange).not.toHaveBeenCalled();
    });

    it('respects max_length for text input', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                input_type: 'text',
                max_length: 5,
            },
            onChange,
        };
        render(<String {...props} />);
        const input = screen.getByRole('textbox');
        fireEvent.change(input, { target: { value: '123456' } });
        expect(onChange).not.toHaveBeenCalled();
    });

    it('sets initial value correctly', () => {
        render(<String {...defaultProps} value="initial" />);
        const input = screen.getByRole('textbox');

        if (!input) {
            throw new Error('Input not found');
        }

        expect(input.value).toBe('initial');
    });

    it('throws an error when min_value or max_value is not provided for number input', () => {
        const props = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
            },
        };
        expect(() => render(<String {...props} />)).toThrow('min_value and max_value are required for the String component with input type is "number"');

        const props2 = {
            ...defaultProps,
            question: {
                input_type: 'number',
                max_value: 100,
            },
        };
        expect(() => render(<String {...props2} />)).toThrow('min_value and max_value are required for the String component with input type is "number"');

        const props3 = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
                max_value: null,
            },
        };
        expect(() => render(<String {...props3} />)).toThrow('min_value and max_value are required for the String component with input type is "number"');

        const props4 = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
                max_value: undefined,
            },
        };
        expect(() => render(<String {...props4} />)).toThrow('min_value and max_value are required for the String component with input type is "number"');

        const props5 = {
            ...defaultProps,
            question: {
                input_type: 'number',
                min_value: 0,
                max_value: 100,
            },
        };
        expect(() => render(<String {...props5} />)).not.toThrow();
    });
});
