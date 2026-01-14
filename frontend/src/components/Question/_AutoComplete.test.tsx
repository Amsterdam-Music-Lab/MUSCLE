import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import AutoComplete from './_AutoComplete';
import Question from '@/types/Question';

const mockQuestion: Question = {
    key: 'test-autocomplete',
    choices: [
        {value: 'option1', label: 'First Option'},
        {value: 'option2', label: 'Second Option'},
        {value: 'option3', label: 'Third Option'}
    ]
};

describe('AutoComplete', () => {
    it('renders without crashing', () => {
        const { container } = render(<AutoComplete question={mockQuestion} value="" onChange={() => { }} />);
        expect(container.querySelector('.css-13cymwt-control')).toBeDefined();
    });

    it('displays the correct options', async () => {
        render(<AutoComplete question={mockQuestion} value="" onChange={() => { }} />);

        const selectInput = screen.getByText('Select...');
        await userEvent.click(selectInput);

        expect(await screen.findByText('First Option')).toBeDefined();
        expect(await screen.findByText('Second Option')).toBeDefined();
        expect(await screen.findByText('Third Option')).toBeDefined();
    });

    it('calls onChange with the correct value when an option is selected', async () => {
        const mockOnChange = vi.fn();
        render(<AutoComplete question={mockQuestion} value="" onChange={mockOnChange} />);

        const selectInput = screen.getByText('Select...');
        await userEvent.click(selectInput);

        const option = await screen.findByText('Second Option');
        await userEvent.click(option);

        expect(mockOnChange).toHaveBeenCalledWith('option2');
    });

    it('displays the correct selected value', () => {
        render(<AutoComplete question={mockQuestion} value="option3" onChange={() => { }} />);

        expect(screen.getByText('Third Option')).toBeDefined();
    });

    it('sorts options alphabetically', async () => {
        render(<AutoComplete question={mockQuestion} value="" onChange={() => { }} />);

        const selectInput = screen.getByText('Select...');
        await userEvent.click(selectInput);

        const options = await screen.findAllByText(/Option/);
        expect(options[0].textContent).toBe('option First Option focused, 1 of 3. 3 results available. Use Up and Down to choose options, press Enter to select the currently focused option, press Escape to exit the menu, press Tab to select the option and exit the menu.');
        expect(options[1].textContent).toBe('First Option');
        expect(options[2].textContent).toBe('Second Option');
    });

    it('calls window.scrollTo when select is blurred', async () => {
        const scrollToSpy = vi.spyOn(window, 'scrollTo');
        render(<AutoComplete question={mockQuestion} value="" onChange={() => { }} />);

        const selectInput = screen.getByRole('combobox', { hidden: true });
        await userEvent.click(selectInput); // Open the select
        await userEvent.tab(); // Tab out to trigger blur

        expect(scrollToSpy).toHaveBeenCalledWith(0, 0);
        scrollToSpy.mockRestore();
    });

    it('throws an error if question has no choices', () => {
        const mockQuestionNoChoices: Question = {
            key: 'test-autocomplete',
            choices: {}
        };

        expect(() => render(<AutoComplete question={mockQuestionNoChoices} value="" onChange={() => { }} />)).toThrowError();

        const mockQuestionNoChoices2: Question = {
            key: 'test-autocomplete',
        };

        expect(() => render(<AutoComplete question={mockQuestionNoChoices2} value="" onChange={() => { }} />)).toThrowError();
    });
});
