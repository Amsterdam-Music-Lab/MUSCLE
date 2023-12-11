import { romanNumeral } from './roman';

describe('romanNumeral', () => {
  it('converts basic numbers correctly', () => {
    expect(romanNumeral(1)).toBe('I');
    expect(romanNumeral(5)).toBe('V');
    expect(romanNumeral(10)).toBe('X');
    expect(romanNumeral(50)).toBe('L');
    expect(romanNumeral(100)).toBe('C');
    expect(romanNumeral(500)).toBe('D');
    expect(romanNumeral(1000)).toBe('M');
  });

  it('converts composite numbers correctly', () => {
    expect(romanNumeral(23)).toBe('XXIII');
    expect(romanNumeral(44)).toBe('XLIV');
    expect(romanNumeral(89)).toBe('LXXXIX');
    expect(romanNumeral(199)).toBe('CXCIX');
    expect(romanNumeral(499)).toBe('CDXCIX');
  });

  it('handles subtractive notation correctly', () => {
    expect(romanNumeral(4)).toBe('IV');
    expect(romanNumeral(9)).toBe('IX');
    expect(romanNumeral(40)).toBe('XL');
    expect(romanNumeral(90)).toBe('XC');
    expect(romanNumeral(400)).toBe('CD');
    expect(romanNumeral(900)).toBe('CM');
    expect(romanNumeral(444)).toBe('CDXLIV');
    expect(romanNumeral(999)).toBe('CMXCIX');
  });

  it('converts large numbers correctly', () => {
    expect(romanNumeral(1984)).toBe('MCMLXXXIV');
    expect(romanNumeral(2022)).toBe('MMXXII');
    expect(romanNumeral(3999)).toBe('MMMCMXCIX');
    expect(romanNumeral(4444)).toBe('MMMMCDXLIV');
    expect(romanNumeral(9999)).toBe('MMMMMMMMMCMXCIX');
  });

  it('handles edge cases correctly', () => {
    expect(romanNumeral(0)).toBe('');
    expect(romanNumeral(-1)).toBe('');
  });
});
