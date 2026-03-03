import { css } from '@emotion/react'

export const styleButton = (buttonColor: string) => {
    return css`
        background-color: ${buttonColor};
        color: white;
        &.border-outside {
            box-shadow: 0 0 0 0.2rem rgba(${buttonColor}, 0.5);
        }
        &:hover:not(.disabled):not(:disabled) {
            background-color: hsl(from ${buttonColor} h s 40%);
            color: white;
        }
        &.checked {
            box-shadow: 0 0 0 0.2rem hsl(from ${buttonColor} h s 40%);
        }
        &:focus {
            box-shadow: 0 0 0 0.2rem hsl(from ${buttonColor} h s 40%);
        }
    `
}

export const styleButtonOutline = (buttonColor: string) => {
    return css`
        border-color: ${buttonColor};
        color: ${buttonColor};
        &:hover:not(.disabled):not(:disabled) {
            background-color: ${buttonColor};
            color: white;
        }
        &:focus {
            box-shadow: 0 0 0 0.2rem hsl(from ${buttonColor} h s 40%);
        }
    `
}