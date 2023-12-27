module.exports = {
    "extends": [
        "eslint:recommended",
        "plugin:react/recommended",
        "plugin:storybook/recommended",
    ],
    "rules": {

        // Set no-undef to warn instead of error for now
        // no-undef means that variables must be defined before use
        "no-undef": [
            "warn",
        ],

        // Set comma-dangle to warn instead of error for now
        // comma-dangle means that a comma is required after the last element in an array or object
        "comma-dangle": [
            "warn",
            "always-multiline",
        ],

        // Set quotes to warn instead of error for now
        // quotes means that strings must be double quoted
        "quotes": [
            "warn",
            "double",
        ],

        // Set arrow-parens to warn instead of error for now
        // arrow-parens means that arrow functions must have parentheses around the arguments
        "arrow-parens": [
            "warn",
            "always",
        ],

        // Set react/react-in-jsx-scope to warn instead of error for now
        // react/react-in-jsx-scope means that React must be in scope when using JSX
        "react/react-in-jsx-scope": [
            "warn",
        ],

        // Turn off react/prop-types for now
        // react/prop-types means that props must be defined for React components
        "react/prop-types": [
            "off",
        ],

        // Enforce the sort order of imports (disabled for now)
        // "sort-imports": [
        //     "warn",
        //     {
        //         "ignoreCase": false,
        //         "ignoreDeclarationSort": false,
        //         "ignoreMemberSort": false,
        //         "memberSyntaxSortOrder": [
        //             "none",
        //             "all",
        //             "multiple",
        //             "single",
        //         ],
        //     },
        // ],

        // Limit line length to 120 characters
        // "max-len": [
        //     "error",
        //     {
        //         "code": 120,
        //         "ignoreComments": true,
        //         "ignoreStrings": true,
        //         "ignoreTemplateLiterals": true,
        //         "ignoreRegExpLiterals": true,
        //     },
        // ],
    },
    "settings": {
        "react": {
            "version": "18",
        },
    },
    "parserOptions": {
        "ecmaVersion": 2020,
        "sourceType": "module",
        "ecmaFeatures": {
            "jsx": true,
            "impliedStrict": true,
        },
    },
}
