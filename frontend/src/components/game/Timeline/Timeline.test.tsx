import { describe, test, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders.tsx";
import Timeline, { getTimeline } from "./Timeline.tsx";
import styles from "./Timeline.module.scss";

describe("getTimeline", () => {
  test("returns config with default sizes and dot enabled", () => {
    const timeline = getTimeline({
      symbols: ["dot", "star", "dot", "star-5"],
    });

    expect(timeline).toEqual([
      { symbol: "dot", size: 10, trophy: false, animate: false },
      { symbol: "star", size: 30, trophy: true, animate: false },
      { symbol: "dot", size: 10, trophy: false, animate: false },
      { symbol: "star-5", size: 30, trophy: true, animate: false },
    ]);
  });

  test("respects trophySize and animate", () => {
    const timeline = getTimeline({
      symbols: ["dot", "star"],
      dotSize: 5,
      trophySize: 40,
      animate: true,
    });

    expect(timeline).toEqual([
      { symbol: "dot", size: 5, trophy: false, animate: false },
      { symbol: "star", size: 40, trophy: true, animate: true },
    ]);
  });

  test("hides dots when showDots is false", () => {
    const result = getTimeline({
      symbols: ["dot", "star", "dot"],
      showDots: false,
    });

    expect(result).toEqual([
      { symbol: null, size: 10, trophy: false, animate: false },
      { symbol: "star", size: 30, trophy: true, animate: false },
      { symbol: null, size: 10, trophy: false, animate: false },
    ]);
  });
});

describe("Timeline component", () => {
  const timelineConfig = getTimeline({
    symbols: ["dot", "star", "dot", "star-5"],
    dotSize: 10,
    trophySize: 20,
    animate: true,
  });

  test("renders symbols and spine segments", () => {
    const { container } = render(
      <Timeline timeline={timelineConfig} step={2} />
    );
    const steps = container.querySelectorAll(`.${styles.step}`);
    expect(steps).toHaveLength(4);
    const spines = container.querySelectorAll(`.${styles.spineSegment}`);
    expect(spines).toHaveLength(3);
  });

  test("does not render symbols if showSymbols is false", () => {
    render(<Timeline timeline={timelineConfig} step={1} showSymbols={false} />);

    const symbols = document.querySelectorAll('[class*="symbol"]');
    expect(symbols.length).toBe(0);
  });
});
