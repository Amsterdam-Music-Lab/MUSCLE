/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import { createContext, useContext, useRef, useEffect, useState } from "react";

/** A hook that allows you to use the orientation context */
export type Orientation = "landscape" | "portrait";
export const OrientationContext = createContext<Orientation>("portrait");
export const useOrientation = () => useContext(OrientationContext);

interface UseOrientationDetectionProps {
  threshold?: number;
}
/**
 * A hook that allows you to detect the orientation of a referenced element
 */
export function useOrientationDetector<T extends HTMLElement>({
  threshold = 0.05,
}: UseOrientationDetectionProps = {}) {
  const ref = useRef<T>(null);
  const [orientation, setOrientation] = useState<"portrait" | "landscape">(
    "portrait"
  );

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      if (Math.abs(width - height) / Math.max(width, height) < threshold) {
        // Skip updating orientation if too close
        return;
      }

      const newOrientation = width > height ? "landscape" : "portrait";
      setOrientation(newOrientation);
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, orientation };
}

/**
 * OrientationProvider provides the orientation context
 * based on the size of its own container.
 */
interface OrientationProviderProps {
  children: ReactNode;

  /**
   * Whether to make the orientation provider fullscreen, so
   * with width 100vw and height 100vh
   */
  fullscreen?: boolean;

  /**
   * Optional threshold used when determining orientation.
   * If the difference between the width and height is below this
   * number, no update is fired.
   */
  threshold?: number;
}

/**
 * Provides and orientation context based on the orientation of this component.
 */
export function OrientationProvider({
  children,
  threshold,
  fullscreen = false,
}: OrientationProviderProps) {
  const { ref, orientation } = useOrientationDetector<HTMLDivElement>({
    threshold,
  });

  return (
    <div
      ref={ref}
      style={
        fullscreen
          ? { width: "100vw", height: "100vh" }
          : { width: "100%", height: "100%" }
      }
    >
      <OrientationContext.Provider value={orientation}>
        {children}
      </OrientationContext.Provider>
    </div>
  );
}
