import { render, screen } from '@testing-library/react';
import { renderLabel } from "./label";

import { describe, it, expect } from 'vitest';

describe('renderLabel', () => {

    it('renders html label correctly', () => {
        render(renderLabel('<div>Some content</div>'));
        expect(screen.getByText("Some content")).not.toBeNull();
    });

    it('returns string label as is', () => {
        const label = 'StringLabel';
        const { getByText } = render(renderLabel(label));

        const labelElement = getByText(label)
        expect(document.body.contains(labelElement)).toBe(true);
    });

    it('handles empty or undefined labels correctly', () => {
        expect(renderLabel('')).toBe('');
        expect(renderLabel(undefined)).toBe(undefined);
    });

});
