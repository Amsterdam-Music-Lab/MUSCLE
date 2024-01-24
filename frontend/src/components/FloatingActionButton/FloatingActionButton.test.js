import React from 'react';
import { getByTestId, render, fireEvent, screen } from '@testing-library/react';
import FloatingActionButton from './FloatingActionButton';

describe('FloatingActionButton', () => {
    it('renders the button with the initial icon', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment" />);
        const icon = getByTestId('floating-action-button__icon');

        expect(icon).to.exist;
        expect(icon).classList.contains('fa-comment');
    });

    it('toggles the content on click', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const content = getByTestId('floating-action-button');
        expect(content).classList.contains('floating-action-button--expanded').to.be.true;

        fireEvent.click(toggleButton);
        expect(content).classList.contains('floating-action-button--expanded').to.be.false;
    });

    it('displays the correct icon when expanded', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment" />);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const icon = getByTestId('floating-action-button__icon');

        expect(icon).to.exist;
        expect(icon).classList.contains('fa-times');
    });

    it('closes the expanded content when the overlay is clicked', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment"><div>Test Content</div></FloatingActionButton>);

        const toggleButton = getByTestId('floating-action-button__toggle-button');
        fireEvent.click(toggleButton);

        const overlay = getByTestId('floating-action-button__overlay');
        fireEvent.click(overlay);

        const content = getByTestId('floating-action-button__content');
        expect(content).classList.contains('floating-action-button--expanded').to.be.false;
    });

    it('initially renders in a collapsed state', () => {
        const { getByTestId } = render(<FloatingActionButton icon="fa-comment" />);
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--expanded')).to.be.false;
    });

    it('correctly applies position classes', () => {
        const { getByTestId } = render(<FloatingActionButton position="bottom-left" />);
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--bottom')).to.be.true;
        expect(getByTestId('floating-action-button').classList.contains('floating-action-button--left')).to.be.true;
    });

    it('applies custom class name', () => {
        const { getByTestId } = render(<FloatingActionButton className="custom-class" />);
        expect(document.body.contains(getByTestId("floating-action-button").querySelector(".custom-class"))).to.be.true;
    });

    it('updates aria-hidden attribute of overlay correctly', () => {
        const { getByTestId } = render(<FloatingActionButton />);
        const overlay = getByTestId('floating-action-button__overlay');
        expect(overlay).to.have.attribute('aria-hidden', 'true');

        fireEvent.click(getByTestId('floating-action-button__toggle-button'));
        expect(overlay).to.have.attribute('aria-hidden', 'false');
    });
});
