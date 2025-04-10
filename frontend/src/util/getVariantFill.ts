import { useTheme } from "@/theme/ThemeProvider";
import { type Variant } from "@/theme/themes";
import { type GradientFill } from "../components/svg/types";

export function getVariantFill(variant: Variant): GradientFill | null {
  const theme = useTheme();
  if(!theme.theme || !theme.theme[variant]) {
    return
  } 
  const _variant = theme?.theme[variant]
  const fill = {
    endColor: _variant.endColor,
    startColor: _variant.startColor,
    angle: _variant?.angle,
    scale: _variant?.scale,
  }
  return fill
}