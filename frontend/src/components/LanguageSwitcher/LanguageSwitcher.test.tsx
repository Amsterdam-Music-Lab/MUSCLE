import { render, screen, fireEvent } from '@testing-library/react';
import { it, expect, describe, vi } from 'vitest';
import LanguageSwitcher from './LanguageSwitcher';

describe('LanguageSwitcher Component', () => {
  const languages = [
    { code: 'en', label: 'English' },
    { code: 'nl', label: 'Dutch' },
  ];

  it('renders language buttons', () => {
    render(
      <LanguageSwitcher
        languages={languages}
        currentLangCode="en"
        onSwitchLanguage={() => { }}
      />
    );

    expect(document.querySelector('.language-switcher')).not.toBeNull();
    expect(screen.getByText('English')).not.toBeNull();
  });

  it('calls onSwitchLanguage when a language button is clicked', () => {
    const onSwitchLanguage = vi.fn();
    render(
      <LanguageSwitcher
        languages={languages}
        currentLangCode="en"
        onSwitchLanguage={onSwitchLanguage}
      />
    );

    fireEvent.click(screen.getByText('Dutch'));
    expect(onSwitchLanguage).toHaveBeenCalledWith('nl');
  });

  it('highlights the current language', () => {
    render(
      <LanguageSwitcher
        languages={languages}
        currentLangCode="en"
        onSwitchLanguage={() => { }}
      />
    );

    const activeButton = screen.getByText('English');
    expect(activeButton.classList.contains('btn-positive')).toBe(true);
  });
});
