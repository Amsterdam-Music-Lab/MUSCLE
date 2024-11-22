import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

import { QuestionViews } from "@/types/Question";

import FeedbackForm from "./FeedbackForm";

const form = [
    {
        key: 'test_question',
        view: QuestionViews.BUTTON_ARRAY,
        question: ['What is the average speed of a Swallow?'],
        choices: { 'slow': '1 km/h', 'fast': '42 km/h' }
    }
]

describe('FeedbackForm', () => {

    it('renders a heading, and a group of radio buttons', () => {
        render(<FeedbackForm
            form={form}
        />)
        const heading = screen.getByRole('heading');
        expect(heading).toBeTruthy();
        expect(heading.textContent).toBe('What is the average speed of a Swallow?');
        expect(screen.getByRole('group')).toBeTruthy();
        expect(screen.queryAllByRole('radio')[0]).toBeTruthy();
    });

});
