import * as React from "react";
import GradientCirclesSVG from "./GradientCirclesSVG";
import "./GradientCircles.scss";

interface GradientCirclesProps {
    color1?: string;
    color2?: string;
    blur?: number;
    numCircles?: number;
    animate?: boolean;
    meanDuration?: number;
    minRadiusFactor?: number;
}

/**
 * A div filled with randomly positioned gradient circles, and
 * an optional blur over it. The circles can also be animated, in
 * which case the gradient will slowly rotate. The colors, number 
 * of circles, and the blur can all be set.
 * 
 * Note that the duration of the animation is random, but you can 
 * set the mean duration. The radius of the circles is also randomly
 * determined using minRadius + 10^(1 + 3 * rand) where rand is a 
 * random float between 0 and 1. minRadius determines the smallest 
 * circles.
 */
export default function GradientCircles({
  color1 = "#ff0000",
  color2 = "#0000ff",
  blur = 0,
  gradientOffset = 0,
  animate = false,
  numCircles = 12,
  minRadiusFactor = null,
  meanDuration = null,
} : GradientCirclesProps) {
  return (
    <div className="gradient-circles" style={{"--blur": `${blur}px`}}>
      <div className="gradient-circles-wrapper">
        <GradientCirclesSVG 
          color1={color1} 
          color2={color2} 
          animate={animate} 
          gradientOffset={gradientOffset}
          numCircles={numCircles} 
          meanDuration={meanDuration}
          minRadiusFactor={minRadiusFactor}
          />
      </div>
      {blur !== 0 && <div className="gradient-circles-blur"><div /></div>}
    </div>
  );
}