
const indigo = "#2B2BEE";
const pink = "#D843E2"
const red = "#FA5577";
const yellow = "#FFB14C";
// const teal = "#39D7B8";

export const mcgLight = {
  name: "mcgLight",
  useGradients: true,
  background: "#ffffff",
  text: "#111111",
  primary: {
    startColor: indigo,
    endColor: red,
    scale: 1,
    subtleScale: 3,
  },
  secondary: {
    startColor: pink,
    endColor: yellow,
    scale: 1,
    subtleScale: 3,
  }
}

export const themes = {
  default: mcgLight,
  mcgLight,
}

export type Theme = typeof mcgLight;

export type ThemeName = keyof typeof themes;