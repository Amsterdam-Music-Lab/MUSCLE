import { render, fireEvent, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Question, {QuestionProps} from './Question';
import { QuestionViews } from '@/types/Question';

describe('Question Component', () => {
    const mockOnChange = vi.fn();

    const defaultProps = {
        question: {
            key: 'test-question',
            question: 'Test Question',
            view: QuestionViews.STRING,
            value: '',
            choices: {
                '1': 'One',
                '2': 'Two',
            },
            style: {}
        },
        onChange: mockOnChange,
        id: 42,
    };

    const getProps = (props = {}) => ({ ...defaultProps, ...props });

    it('renders the question text', () => {
        render(<Question {...defaultProps} />);
        expect(screen.getByText('Test Question')).toBeTruthy();
    });

    it('renders an explainer when provided', () => {
        const props = {
            ...defaultProps,
            question: {
                ...defaultProps.question,
                explainer: 'This is an explainer',
            },
        };
        render(<Question {...props} />);
        expect(screen.getByText('This is an explainer')).toBeTruthy();
    });

    it('renders the expected response when provided and TESTING is true', () => {
        const props = {
            ...defaultProps,
            question: {
                ...defaultProps.question,
                expected_response: 'Expected response',
            },
        };
        // Mock the TESTING environment variable
        vi.stubGlobal('process', { env: { TESTING: 'true' } });
        render(<Question {...props} />);
        expect(screen.getByText('Expected response')).toBeTruthy();
        vi.unstubAllGlobals();
    });

    it('calls onChange when the value changes', () => {
        render(<Question {...defaultProps} />);
        const input = screen.getByRole('textbox');
        fireEvent.change(input, { target: { value: 'New Value' } });
        expect(mockOnChange).toHaveBeenCalledWith('New Value', 42);
    });

    it('applies classNames if question.style is defined', () => {
        const props = defaultProps;
        props.question.style = 'some-style';
        const { container } = render(<Question {...props} />);
        expect(container.querySelector('.some-style')).toBeTruthy();
    });

    it('disables the input when disabled prop is true', () => {
        const props = getProps({
            disabled: true,
            question: {
                ...defaultProps.question,
                view: QuestionViews.BUTTON_ARRAY,
                choices: { '1': 'One', '2': 'Two' },
            }
        });
        render(<Question {...props} />);
        const input = screen.getByTestId('toggle-button-1');
        expect(input).toBeTruthy();
        expect(input.attributes.getNamedItem('disabled')).toBeTruthy();
    });
});
