import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import HTML from './HTML';

describe('HTML', () => {
    it('renders the HTML content correctly', () => {
        const htmlContent = '<p>Test content</p>';
        const { container } = render(<HTML body={htmlContent} />);
        expect(container.innerHTML).to.include(htmlContent);
    });

    it('applies the default inner className', () => {
        const { container } = render(<HTML body="<div>Test</div>" />);
        const innerDiv = container.querySelector('.html-content');

        if (!innerDiv) {
            throw new Error('Inner div not found');
        }

        expect(innerDiv.classList.contains('text-center')).toBe(true);
        expect(innerDiv.classList.contains('pb-3')).toBe(true);
    });

    it('applies a custom inner className', () => {
        const customClass = 'custom-class';
        const { container } = render(<HTML body="<div>Test</div>" innerClassName={customClass} />);
        const innerDiv = container.querySelector('.html-content');

        if (!innerDiv) {
            throw new Error('Inner div not found');
        }

        expect(innerDiv.classList.contains(customClass)).toBe(true);
        expect(innerDiv.classList.contains('text-center')).toBe(false);
        expect(innerDiv.classList.contains('pb-3')).toBe(false);
    });

    it('renders complex HTML content', () => {
        const complexHTML = `
      <div>
        <h1>Title</h1>
        <p>Paragraph <strong>with bold text</strong></p>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
        </ul>
      </div>
    `;
        const { container } = render(<HTML body={complexHTML} />);
        expect(container.innerHTML).to.include(complexHTML);
    });

    it('renders the outer aha__HTML class', () => {
        const { container } = render(<HTML body="<div>Test</div>" />);
        const outerDiv = container.firstChild;

        if (!outerDiv) {
            throw new Error('Outer div not found');
        }

        expect(outerDiv.classList.contains('aha__HTML')).toBe(true);
    });

    it('handles empty body content', () => {
        const { container } = render(<HTML body="" />);
        const innerDiv = container.querySelector('.html-content');

        if (!innerDiv) {
            throw new Error('Inner div not found');
        }

        expect(innerDiv.innerHTML).to.equal('');
    });

    it('handles TrustedHTML type for body prop', () => {
        const trustedHTML = {
            toString: () => '<p>Trusted HTML</p>',
        } as TrustedHTML;
        const { container } = render(<HTML body={trustedHTML} />);
        expect(container.innerHTML).to.include('<p>Trusted HTML</p>');
    });
});
