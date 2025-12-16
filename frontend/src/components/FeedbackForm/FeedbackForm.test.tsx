import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import { QuestionViews } from "@/types/Question";

import FeedbackForm from "./FeedbackForm";


const radiosQuestion = {
    key: 'test_question',
    view: QuestionViews.RADIOS,
    text: 'What is the average speed of a Swallow?',
    choices: { 'slow': '1 km/h', 'fast': '42 km/h' }
}
const buttonsQuestion = {
    key: 'test_question2',
    view: QuestionViews.BUTTON_ARRAY,
    text: 'An African or European swallow?',
    choices: { 'undecided': 'uh', 'counter': 'what?' }
}

const defaultProps = {
    submitButton: {
        label: 'submit'
    },
    submitResult: vi.fn()
}


describe('FeedbackForm', () => {

    it('renders a heading and a form with the selected question view', () => {
        const form = [
            radiosQuestion
        ];
        render(<FeedbackForm
            {...defaultProps}
            form={form}
        />)
        const heading = screen.getByRole('heading');
        expect(heading).toBeTruthy();
        expect(heading.textContent).toBe('What is the average speed of a Swallow?');
        expect(screen.queryByRole('form')).toBeTruthy();
        expect(screen.queryAllByRole('radio')).toHaveLength(2);
        
    });

    it('renders submit button when the form has one question which is not BUTTON_ARRAY', () => {
        const form = [
            radiosQuestion
        ];
        render(<FeedbackForm
            {...defaultProps}
            form={form}
        />)
        expect(screen.getByRole('button')).toBeTruthy();
        expect(screen.queryByText('submit')).toBeTruthy();
    });

    it('renders submit button when the form has multiple questions', () => {
        const form = [
            radiosQuestion,
            buttonsQuestion
        ];
        render(<FeedbackForm
            {...defaultProps}
            form={form}
        />)
        expect(screen.queryByText('submit')).toBeTruthy();
    });

    it('does not render submit button when the form has one BUTTON_ARRAY question', () => {
        const form = [
            buttonsQuestion
        ];
        render(<FeedbackForm
            {...defaultProps}
            form={form}
        />)
        expect(screen.queryByText('submit')).toBeFalsy();
    });

});
