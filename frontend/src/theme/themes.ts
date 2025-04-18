/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Theme} from "@/types/themeProvider"

const indigo = "#2B2BEE";
const pink = "#D843E2";
const red = "#FA5577";
const yellow = "#FFB14C";
const teal = "#39D7B8";
const green = "#00b612";


export const mcgLight: Theme = {
  name: "mcgLight",
  type: "light",
  fontUrl:
    "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  fontFamily: "Inter, sans-serif",
  useGradients: true,
  background: "#ffffff",
  text: "#111111",
  borderRadius: 1,
  primary: {
    solid: indigo,
    startColor: indigo,
    endColor: red,
    scale: 2,
    subtleScale: 3,
  },
  secondary: {
    solid: pink,
    startColor: pink,
    endColor: yellow,
    scale: 4,
    subtleScale: 3,
    offset: -2.5,
    angle: -60,
  },
};

export const mcgDark: Theme = {
  ...mcgLight,
  name: "mcgDark",
  type: "dark",
  background: "#333",
  text: "#eee",
  primary: {
    ...mcgLight.primary,
    solid: pink,
    startColor: indigo,
    endColor: teal,
  },
  secondary: {
    ...mcgLight.secondary,
    solid: indigo,
    startColor: yellow,
    endColor: green,
  },
};

export const amlDark: Theme = {
  name: "amlDark",
  type: "dark",
  // Todo should be Roboto?
  fontUrl:
    "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300&family=Noto+Serif+SC:wght@600&display=swap",
  fontFamily: "Inter, sans-serif",
  useGradients: true,
  background: "#ffffff",
  backgroundUrl: "/public/images/background.jpg",
  text: "#111111",
  primary: {
    solid: indigo,
    startColor: indigo,
    endColor: red,
    scale: 1,
    subtleScale: 3,
  },
  secondary: {
    solid: pink,
    startColor: pink,
    endColor: yellow,
    scale: 1,
    subtleScale: 3,
  },
};

export const themes = {
  default: mcgLight,
  mcgLight,
  mcgDark,
  amlDark,
};

export type ThemeName = keyof typeof themes;
