import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import DropDown from './_DropDown';
import Question from '@/types/Question';

const mockQuestion: Question = {
    key: 'test-dropdown',
    choices: [
        {value: 'option1', label: 'First Option'},
        {value: 'option2', label: 'Second Option'},
        {value: 'option3', label: 'Third Option'}
    ]
};

describe('DropDown', () => {
    it('renders without crashing', () => {
        render(<DropDown question={mockQuestion} value="" onChange={() => { }} />);
        expect(screen.getByRole('combobox')).toBeDefined();
    });

    it('displays all choices', () => {
        render(<DropDown question={mockQuestion} value="" onChange={() => { }} />);
        const options = screen.getAllByRole('option');
        expect(options.length).toBe(4); // 3 choices + 1 empty option
        expect(options[1].textContent).toBe('First Option');
        expect(options[2].textContent).toBe('Second Option');
        expect(options[3].textContent).toBe('Third Option');
    });

    it('sets the correct default value', () => {
        render(<DropDown question={mockQuestion} value="option2" onChange={() => { }} />);
        expect((screen.getByRole('combobox') as HTMLSelectElement).value).toBe('option2');
    });

    it('calls onChange with correct value when an option is selected', async () => {
        const onChange = vi.fn();
        render(<DropDown question={mockQuestion} value="" onChange={onChange} />);

        await userEvent.selectOptions(screen.getByRole('combobox'), 'option2');
        expect(onChange).toHaveBeenCalledWith('option2');
    });

    it('has an empty option', () => {
        render(<DropDown question={mockQuestion} value="" onChange={() => { }} />);
        const emptyOption = screen.getAllByRole('option')[0];
        expect(emptyOption).toBeDefined();
        expect(emptyOption.value).toBe('');
    });

    it('sets the correct name attribute', () => {
        render(<DropDown question={mockQuestion} value="" onChange={() => { }} />);
        expect((screen.getByRole('combobox') as HTMLSelectElement).name).toBe('test-dropdown');
    });

    it('throws an error when no choices are provided', () => {
        const invalidQuestion: Question = {
            key: 'invalid-dropdown',
            choices: []
        };

        expect(() => render(<DropDown question={invalidQuestion} value="" onChange={() => { }} />))
            .toThrow('DropDown question must have choices');
    });
});
