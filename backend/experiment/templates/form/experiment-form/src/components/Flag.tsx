import React from 'react';
import WorldFlag from 'react-world-flags';
import { getCountryCode, getLanguageName } from '../utils/languageUtils';

interface FlagProps {
  languageCode: string;
  className?: string;
  showLabel?: boolean;
}

export const Flag: React.FC<FlagProps> = ({ languageCode, className = '', showLabel = false }) => {
  const countryCode = getCountryCode(languageCode);
  const languageName = getLanguageName(languageCode);

  return (
    <div className="inline-flex items-center gap-2" title={languageName}>
      <WorldFlag
        code={countryCode}
        className={`h-4 w-auto shadow-sm ${className}`}
        fallback={<span className="text-xs">{countryCode}</span>}
      />
      {showLabel && <span>{languageName}</span>}
    </div>
  );
};
