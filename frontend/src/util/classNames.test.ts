import classNames from './classNames';
import { describe, expect, it } from 'vitest';

describe('classNames function', () => {
    it('joins multiple string arguments', () => {
        expect(classNames('class1', 'class2', 'class3')).toBe('class1 class2 class3');
    });

    it('filters out falsy values', () => {
        expect(classNames('class1', '', 'class2', null, 'class3', undefined, false)).toBe('class1 class2 class3');
    });

    it('returns an empty string for only falsy values', () => {
        expect(classNames('', null, undefined, false)).toBe('');
    });

    it('returns an empty string for no arguments', () => {
        expect(classNames()).toBe('');
    });
});
