import React from 'react';
import { vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import ButtonArray from './_ButtonArray';
import { QuestionViews } from '@/types/Question'

const getProps = (overrides = {}) => ({
    question: {
        "key": "know_song",
        "view": QuestionViews.BUTTON_ARRAY,
        "explainer": "",
        "question": "1. Do you know this song?",
        "result_id": 12345,
        "is_skippable": false,
        "submits": false,
        "style": "boolean",
        "choices": {
            "yes": "Yes",
            "unsure": "Unsure",
            "no": "No"
        },
        "min_values": 1,
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

        expect(button.classList.contains('checked')).to.be.true;
    });

    it('does not add the "checked" class to a button when it is not selected', () => {
        const props = getProps({ value: 'yes' });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Unsure');

        expect(button.classList.contains('checked')).to.be.false;
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
});
