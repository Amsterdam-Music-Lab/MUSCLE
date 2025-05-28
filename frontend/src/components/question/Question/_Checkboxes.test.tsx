import type Question from '@/types/Question';

import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Checkboxes from './_Checkboxes';

const mockQuestion: Question = {
    key: 'test-checkboxes',
    choices: {
        'option1': 'First Option',
        'option2': 'Second Option',
        'option3': 'Third Option'
    }
};

describe('Checkboxes', () => {
    it('renders without crashing', () => {
        render(<Checkboxes question={mockQuestion} value="" onChange={() => { }} />);
        expect(screen.getByText('First Option')).toBeDefined();
        expect(screen.getByText('Second Option')).toBeDefined();
        expect(screen.getByText('Third Option')).toBeDefined();
    });

    it('displays all choices', () => {
        render(<Checkboxes question={mockQuestion} value="" onChange={() => { }} />);
        Object.values(mockQuestion.choices).forEach(choice => {
            expect(screen.getByText(choice)).toBeDefined();
        });
    });

    it('checks boxes based on initial value', () => {
        render(<Checkboxes question={mockQuestion} value="option1,option3" onChange={() => { }} />);
        expect(screen.getByText('First Option').parentElement.classList.contains('checked')).toBe(true);
        expect(screen.getByText('Second Option').parentElement.classList.contains('checked')).toBe(false);
        expect(screen.getByText('Third Option').parentElement.classList.contains('checked')).toBe(true);
    });

    it('calls onChange with correct value when checkbox is clicked', async () => {
        const onChange = vi.fn();
        render(<Checkboxes question={mockQuestion} value="" onChange={onChange} />);

        await userEvent.click(screen.getByText('Second Option'));
        expect(onChange).toHaveBeenCalledWith('option2');

        await userEvent.click(screen.getByText('First Option'));
        expect(onChange).toHaveBeenCalledWith('option2,option1');
    });

    it('unchecks a box when clicked twice', async () => {
        const onChange = vi.fn();
        render(<Checkboxes question={mockQuestion} value="option1,option2" onChange={onChange} />);

        await userEvent.click(screen.getByText('Second Option'));
        expect(onChange).toHaveBeenCalledWith('option1');
    });

    it('handles keyboard interactions', async () => {
        const onChange = vi.fn();
        render(<Checkboxes question={mockQuestion} value="" onChange={onChange} />);

        const firstOption = screen.getByText('First Option').parentElement;

        if (!firstOption) {
            throw new Error('First option not found');
        }

        firstOption.focus();
        await fireEvent.keyDown(firstOption, { key: 'Enter', code: 'Enter', charCode: 13, keyCode: 13 });

        expect(onChange).toHaveBeenCalledWith('option1');
    });

    it('throws an error when no choices are provided', () => {
        const invalidQuestion: Question = {
            key: 'invalid-checkboxes',
            choices: {}
        };

        expect(() => render(<Checkboxes question={invalidQuestion} value="" onChange={() => { }} />))
            .toThrow('Checkboxes question must have choices');

        const noChoicesQuestion: Question = {
            key: 'invalid-checkboxes',
        };

        expect(() => render(<Checkboxes question={noChoicesQuestion} value="" onChange={() => { }} />))
            .toThrow('Checkboxes question must have choices');
    });
});
