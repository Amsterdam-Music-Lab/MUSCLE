import { vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import ButtonArray from './_ButtonArray';
import { QuestionViews } from '@/types/Question'
import { expect, describe, it } from 'vitest';

const getProps = (overrides = {}) => ({
    question: {
        "key": "know_song",
        "view": QuestionViews.BUTTON_ARRAY,
        "explainer": "",
        "question": "1. Do you know this song?",
        "style": "boolean",
        "choices": [
            {value: "yes", label: "Yes"},
            {value: "unsure", label: "Unsure"},
            {value: "no", label: "No"}
        ],
    },
    disabled: false,
    onChange: vi.fn(),
    value: null,
    ...overrides,
});

describe('ButtonArray', () => {

    it('adds the "checked" class to a button when it is selected', () => {
        const props = getProps({ value: 'yes' });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Yes');

        expect(button.classList.contains('checked')).toBeTruthy();
    });

    it('does not add the "checked" class to a button when it is not selected', () => {
        const props = getProps({ value: 'yes' });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Unsure');

        expect(button.classList.contains('checked')).toBeFalsy();
    });

    it('calls the onChange function when a button is clicked', () => {
        const props = getProps();
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Yes');
        fireEvent.click(button);

        expect(props.onChange).toHaveBeenCalledWith('yes');
    });

    it('does not call the onChange function when a disabled button is clicked', () => {
        const props = getProps({ disabled: true });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Yes');
        fireEvent.click(button);

        expect(props.onChange).not.toHaveBeenCalled();
    });

    it('throws an error if the question has no choices', () => {
        const props = getProps({ question: { ...getProps().question, choices: [] } });

        expect(() => render(<ButtonArray {...props} />)).toThrowError('ButtonArray question must have choices');

        const props2 = getProps({ question: { ...getProps().question } });
        delete props2.question.choices;

        expect(() => render(<ButtonArray {...props2} />)).toThrowError('ButtonArray question must have choices');
    });

});
