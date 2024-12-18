import { Language } from '@/types/Experiment';
import React from 'react';
import Button from '../Button/Button';
import './LanguageSwitcher.scss';

interface LanguageSwitcherProps {
  languages: Language[];
  currentLangCode: string;
  onSwitchLanguage: (langCode: string) => void;
}

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ languages, onSwitchLanguage, currentLangCode }) => {

  return (
    <div className="language-switcher">
      <label className='language-switcher__label'>Language:</label>
      {languages.map((lang) => (
        <Button key={lang.code} title={lang.label} onClick={() => onSwitchLanguage(lang.code)} clickOnce={false} className={lang.code === currentLangCode ? 'btn-positive' : 'btn-negative'} size='md'>
        </Button>
      ))}
    </div>
  );
};

export default LanguageSwitcher;
