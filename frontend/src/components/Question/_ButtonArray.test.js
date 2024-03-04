import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ButtonArray from './_ButtonArray';

const getProps = (overrides = {}) => ({
    question: {
        "key": "know_song",
        "view": "BUTTON_ARRAY",
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
    onChange: jest.fn(),
    value: null,
    ...overrides,
});

describe('ButtonArray', () => {
    it('adds the "checked" class to a button when it is selected', () => {
        const props = getProps({ value: 'yes' });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Yes');

        expect(button).toHaveClass('checked');
    });

    it('does not add the "checked" class to a button when it is not selected', () => {
        const props = getProps({ value: 'yes' });
        const { getByText } = render(<ButtonArray {...props} />);

        const button = getByText('Unsure');

        expect(button).not.toHaveClass('checked');
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
