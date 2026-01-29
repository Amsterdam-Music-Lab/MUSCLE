import eslint from '@eslint/js';
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';

export default defineConfig(
	eslint.configs.recommended,
	tseslint.configs.recommended,
	{
		languageOptions: {
			parserOptions: {
				ecmaVersion: 2021,
				sourceType: 'module',
			},
			globals: {
				window: 'readonly',
				document: 'readonly',
				console: 'readonly',
			},
		},
	}
);