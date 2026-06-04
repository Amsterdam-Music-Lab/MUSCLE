import eslint from '@eslint/js';
import { defineConfig, globalIgnores } from 'eslint/config';
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
				console: 'readonly',
				document: 'readonly',
				fetch: 'readonly',
				module: 'readonly',
				navigator: 'readonly',
				process: 'readonly',
				require: 'readonly',
				URL: 'readonly',
				window: 'readonly',
			},
		},
	},
	globalIgnores(["src/**/*.test.tsx", "src/stories/*"])
);