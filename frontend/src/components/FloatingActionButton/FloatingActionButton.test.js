import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import FloatingActionButton from './FloatingActionButton';

describe('FloatingActionButton', () => {
    it('renders the button with the initial icon', () => {
        render(<FloatingActionButton icon="fa-comment" />);
        const icon = screen.getByTestId('floating-action-button__icon');
        expect(icon).toBeInTheDocument();
        expect(icon).toHaveClass('fa-comment');
    });

    it('toggles the content on click', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const content = getByTestId('floating-action-button');
        expect(content).toHaveClass('floating-action-button--expanded');

        fireEvent.click(toggleButton);
        expect(content).not.toHaveClass('floating-action-button--expanded');
    });

    it('displays the correct icon when expanded', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment" />);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const icon = getByTestId('floating-action-button__icon');
        expect(icon).toBeInTheDocument();
        expect(icon).toHaveClass('fa-times');
    });

    it('closes the expanded content when the overlay is clicked', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const overlay = getByTestId('floating-action-button__overlay');
        fireEvent.click(overlay);

        const content = getByTestId('floating-action-button__content');
        expect(content).not.toHaveClass('floating-action-button--expanded');
    });

    it('initially renders in a collapsed state', () => {
        render(<FloatingActionButton icon="fa-comment" />);
        expect(screen.getByTestId('floating-action-button')).not.toHaveClass('floating-action-button--expanded');
    });

    it('correctly applies position classes', () => {
        render(<FloatingActionButton position="bottom-left" />);
        expect(screen.getByTestId('floating-action-button')).toHaveClass('floating-action-button--bottom');
        expect(screen.getByTestId('floating-action-button')).toHaveClass('floating-action-button--left');
    });

    it('applies custom class name', () => {
        render(<FloatingActionButton className="custom-class" />);
        expect(screen.getByTestId('floating-action-button')).toHaveClass('custom-class');
    });

    it('updates aria-hidden attribute of overlay correctly', () => {
        render(<FloatingActionButton />);
        const overlay = screen.getByTestId('floating-action-button__overlay');
        expect(overlay).toHaveAttribute('aria-hidden', 'true');
        fireEvent.click(screen.getByTestId('floating-action-button__toggle-button'));
        expect(overlay).toHaveAttribute('aria-hidden', 'false');
    });
});
