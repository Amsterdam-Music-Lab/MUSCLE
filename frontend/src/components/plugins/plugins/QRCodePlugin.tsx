/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { Variant } from "@/types/themeProvider";
import { useTheme } from "@/theme/ThemeProvider";
import { lazy, Suspense } from "react";
const QRCodeSVG = lazy(() =>
  import("qrcode.react").then((mod) => ({
    default: mod.QRCodeSVG,
  }))
);

export interface QRCodePluginArgs {
  value: string;
  level?: "L" | "M" | "Q" | "H";
  size?: number;
  variant?: Variant;
}

function QRCode({
  value,
  level = "L",
  size = 70,
  variant,
  fgColor,
}: QRCodePluginArgs) {
  const { theme } = useTheme();
  if (variant && !fgColor) fgColor = theme[variant]?.solid;
  return (
    <Suspense fallback="Loading QR...">
      <QRCodeSVG
        value={value}
        level={level}
        size={size}
        fgColor={fgColor}
        style={{ minWidth: `${size}px` }}
      />
    </Suspense>
  );
}

export interface QRCodePluginSpec extends PluginSpec<QRCodePluginArgs> {
  name: "qrcode";
}

export interface QRCodePluginMeta extends PluginMeta<QRCodePluginArgs> {
  name: "qrcode";
}

export const qrCodePlugin: QRCodePluginMeta = {
  name: "qrcode",
  component: QRCode,
  description: "Renders a QR code",
};
