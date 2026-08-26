import { render, fireEvent, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Question from './Question';
import { QuestionViews } from '@/types/Question';

describe('Question Component', () => {
    const mockOnChange = vi.fn();

    const defaultProps = {
        question: {
            identifier: 'test-question',
            text: 'Test Question',
            view: QuestionViews.STRING,
            maxLength: 200,
            value: '',
            choices: [
                {value: '1', label: 'One'},
                {value: '2', label: 'Two'},
            ],
            style: {}
        },
        onChange: mockOnChange,
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

    it('calls onChange when the value changes', async () => {
        render(<Question {...defaultProps} />);
        const input = await screen.findByRole('textbox');
        fireEvent.change(input, { target: { value: 'New Value' } });
        expect(mockOnChange).toHaveBeenCalledWith('New Value');
    });

    it('applies classNames if question.style is defined', () => {
        const props = defaultProps;
        props.question.style = 'some-style';
        const { container } = render(<Question {...props} />);
        expect(container.querySelector('.some-style')).toBeTruthy();
    });

    it('disables the input when disabled prop is true', async () => {
        const props = getProps({
            disabled: true,
            question: {
                ...defaultProps.question,
                view: QuestionViews.BUTTON_ARRAY,
                choices: [
                    {value: '1', label: 'One'},
                    {value: '2', label: 'Two'},
                ],
            }
        });
        render(<Question {...props} />);
        const input = await screen.findByTestId('toggle-button-1');
        expect(input).toBeTruthy();
        expect(input.attributes.getNamedItem('disabled')).toBeTruthy();
    });
});
