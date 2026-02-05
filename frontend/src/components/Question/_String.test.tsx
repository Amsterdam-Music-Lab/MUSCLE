import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen, createEvent } from '@testing-library/react';
import String from './_String';

describe('String component', () => {
    const defaultProps = {
        question: {
            maxLength: 100,
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

    it('respects maxLength for text input', () => {
        const onChange = vi.fn();
        const props = {
            ...defaultProps,
            question: {
                maxLength: 5,
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
});
