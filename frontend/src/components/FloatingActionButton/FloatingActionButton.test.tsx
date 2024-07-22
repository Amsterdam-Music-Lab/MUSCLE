import { it, describe, expect } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import FloatingActionButton from './FloatingActionButton';

describe('FloatingActionButton', () => {
    it('renders the button with the initial icon', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment" >Test Content</FloatingActionButton>);
        const icon = getByTestId('floating-action-button__icon');

        expect(document.body.contains(icon)).toBe(true);
        expect(icon.classList.contains('fa-comment')).toBe(true);
    });

    it('toggles the content on click', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const content = getByTestId('floating-action-button');
        expect(content.classList.contains('floating-action-button--expanded')).toBe(true);

        fireEvent.click(toggleButton);
        expect(content.classList.contains('floating-action-button--expanded')).toBe(false);
    });

    it('displays the correct icon when expanded', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const icon = getByTestId('floating-action-button__icon');

        expect(document.body.contains(icon)).toBe(true);
        expect(icon.classList.contains('fa-times')).toBe(true);
    });

    it('closes the expanded content when the overlay is clicked', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const overlay = getByTestId('floating-action-button__overlay');
        fireEvent.click(overlay);

        const content = getByTestId('floating-action-button__content');
        expect(content.classList.contains('floating-action-button--expanded')).toBe(false);
    });

    it('initially renders in a collapsed state', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--expanded')).toBe(false);
    });

    it('correctly applies position classes', () => {
        const { getByTestId } = render(<FloatingActionButton position="bottom-left">Test Content</FloatingActionButton>);
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--bottom')).toBe(true);
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--left')).toBe(true);
    });

    it('applies custom class name', () => {
        const { getByTestId } = render(<FloatingActionButton className="custom-class">Test Content</FloatingActionButton>);
        const button = getByTestId('floating-action-button');
        expect(button.classList.contains('custom-class')).toBe(true);
    });

    it('updates aria-hidden attribute of overlay correctly', () => {
        const { getByTestId } = render(<FloatingActionButton>Test Content</FloatingActionButton>);
        const overlay = getByTestId('floating-action-button__overlay');
        expect(overlay.attributes.getNamedItem('aria-hidden').value).toEqual('true');

        fireEvent.click(getByTestId('floating-action-button__toggle-button'));
        expect(overlay.attributes.getNamedItem('aria-hidden').value).toEqual('false');
    });
});
