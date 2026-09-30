import { css, keyframes } from '@emotion/react'

import Theme from '@types/Theme';

export const styleButton = (buttonColor: string) => {
    return css`
        background-color: ${buttonColor};
        color: white;
        &.border-outside {
            box-shadow: 0 0 0 0.2em hsl(from ${buttonColor} h s 40%);
        }
        &:hover:not(.disabled):not(:disabled) {
            background-color: hsl(from ${buttonColor} h s 50%);
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

const scoreBackgroundAnimation = (backgroundColor: string) => keyframes`
    0% {
        opacity: 0;
        fill: transparent;
    }
    50% {
        opacity: 1;
    }
    100% {
        fill: ${backgroundColor};
    }
`

export const animateScoreBackground = (score: number, theme: Theme) => {
    const backgroundColor = score > 0 ? theme.colorPositive : score === 0 ? theme.colorGrey : theme.colorNegative;
    return css`
    .aha__circle .circle-percentage {
        animation-name: ${scoreBackgroundAnimation(backgroundColor)};
    }
    `
}