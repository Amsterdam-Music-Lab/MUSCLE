import { css } from '@emotion/react'

export const styleButton = (buttonColor: string) => {
    return css`
        background-color: ${buttonColor};
        color: white;
        &.border-outside {
            box-shadow: 0 0 0 0.2em rgba(${buttonColor}, 0.5);
        }
        &:hover:not(.disabled):not(:disabled) {
            background-color: hsl(from ${buttonColor} h s 40%);
            color: white;
        }
        &:focus, &.checked {
            box-shadow: 0 0 0 0.2rem rgba(${buttonColor}, 0.5);
        }
    `
}