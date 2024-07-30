import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Radios from './_Radios';
import Question from '@/types/Question';

const mockQuestion: Question = {
    key: 'test-radios',
    choices: {
        '1': 'First Option',
        '2': 'Second Option',
        '3': 'Third Option'
    }
};

describe('Radios', () => {
    it('renders without crashing', () => {
        render(<Radios question={mockQuestion} value="" onChange={() => { }} />);
        expect(screen.getByText('First Option')).toBeDefined();
        expect(screen.getByText('Second Option')).toBeDefined();
        expect(screen.getByText('Third Option')).toBeDefined();
    });

    it('throws an error when no choices are provided', () => {
        const invalidQuestion = { ...mockQuestion, choices: {} };
        expect(() => render(<Radios question={invalidQuestion} value="" onChange={() => { }} />))
            .toThrow('Radios question must have choices');
    });

    it('renders choices in correct order', () => {
        render(<Radios question={mockQuestion} value="" onChange={() => { }} />);
        const options = screen.getAllByRole('radio');
        expect(options[0].textContent).toBe('First Option');
        expect(options[1].textContent).toBe('Second Option');
        expect(options[2].textContent).toBe('Third Option');
    });

    it('marks the correct option as checked', () => {
        render(<Radios question={mockQuestion} value="2" onChange={() => { }} />);
        const checkedOption = screen.getByText('Second Option').parentElement;

        if (!checkedOption) {
            throw new Error('Option not found');
        }

        expect(checkedOption.classList.contains('checked')).toBe(true);
    });

    it('calls onChange with correct value when an option is clicked', async () => {
        const onChange = vi.fn();
        render(<Radios question={mockQuestion} value="" onChange={onChange} />);

        await userEvent.click(screen.getByText('Second Option'));
        expect(onChange).toHaveBeenCalledWith('2');
    });

    it('handles keyboard interactions', async () => {
        const onChange = vi.fn();
        render(<Radios question={mockQuestion} value="" onChange={onChange} />);

        const firstOption = screen.getByText('First Option').parentElement;

        if (!firstOption) {
            throw new Error('Option not found');
        }

        firstOption.focus();
        fireEvent.keyDown(firstOption, { key: 'Enter', code: 'Enter', keyCode: 13, charCode: 13 });

        expect(onChange).toHaveBeenCalledWith('1');
    });

    it('applies correct classes to radio options', () => {
        render(<Radios question={mockQuestion} value="2" onChange={() => { }} />);
        const options = screen.getAllByRole('radio');
        expect(options[0].classList.contains('radio')).toBe(true);
        expect(options[0].classList.contains('checked')).toBe(false);
        expect(options[1].classList.contains('radio')).toBe(true);
        expect(options[1].classList.contains('checked')).toBe(true);
    });

    it('sets correct tabIndex on radio options', () => {
        render(<Radios question={mockQuestion} value="" onChange={() => { }} />);
        const options = screen.getAllByRole('radio');
        options.forEach(option => {
            expect(option.tabIndex).toBe(0);
        });
    });
});
