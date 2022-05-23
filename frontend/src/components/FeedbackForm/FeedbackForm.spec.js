import React from "react";
import { cleanup, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

import FeedbackForm from "./FeedbackForm";

const form = [
    {
        key: 'test_question',
        view: 'BUTTON_ARRAY',
        question: ['What is the average speed of a Swallow?'],
        choices: {'slow': '1 km/h', 'fast': '42 km/h'}
    }
]

describe('FeedbackForm', () => {
    afterEach(cleanup);

    it('renders a heading, and a group of radio buttons', () => {
        render(<FeedbackForm
            form={form}
        />)
        expect(screen.getByRole('heading')).toHaveTextContent('What is the average speed of a Swallow?');
        expect(screen.getByRole('group')).toBeInTheDocument();
        expect(screen.queryAllByRole('radio')[0]).toBeInTheDocument();
    });

});
