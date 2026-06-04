// based on https://stackoverflow.com/a/46543292
interface RGB {
    r: number;
    g: number;
    b: number;
}

const hexToRgb = (hex: string) : RGB => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return {
    r: parseInt(result? result[1] : "0", 16),
    g: parseInt(result? result[2]: "0", 16),
    b: parseInt(result? result[3]: "0", 16)
  }
}

const getFade = (value: number, fromSource: number, toSource: number, fromTarget: number, toTarget: number): number => {
  return (value - fromSource) / (toSource - fromSource) * (toTarget - fromTarget) + fromTarget;
}

const getDifference = (startVal: number, endVal: number, percentFade: number): number => {
    return (endVal - startVal) * percentFade + startVal;
}

export const getGradientColor = (startColor: string, endColor: string, min: number, max: number, value: number): string => {
  const startRGB = hexToRgb(startColor);
  const endRGB = hexToRgb(endColor);
  const percentFade = getFade(value, min, max, 0, 1);
  const diffRed = getDifference(startRGB.r, endRGB.r, percentFade);
  const diffGreen = getDifference(startRGB.g, endRGB.r, percentFade);
  const diffBlue = getDifference(startRGB.b, endRGB.b, percentFade);

  return "rgb(" + Math.round(diffRed) + ", " + Math.round(diffGreen) + ", " + Math.round(diffBlue) + ")";
}
