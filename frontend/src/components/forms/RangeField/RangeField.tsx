/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import type { FieldProps } from "../types";
import { useState } from "react";
import { Range } from "react-range";
import classNames from "classnames";
import { Variant } from "@/types/themeProvider";
import styles from "./RangeField.module.scss";
import "@/scss/theme.scss";

export interface RangeOption<Value> {
  value: Value;
  label?: ReactNode;
  position?: number;
}

function generateOptions<Value>(
  min: number,
  max: number,
  step: number,
  autoTickLabels: boolean
): RangeOption<Value>[] {
  const options = [];
  for (let val = min; val <= max; val += step) {
    options.push({
      value: val,
      label: autoTickLabels ? String(val) : undefined,
      position: val,
    });
  }
  return options;
}

function havePositions<Value>(options: RangeOption<Value>[]) {
  return options.map((opt) => opt?.position).every(Boolean);
}

function getTickLabels<Value>(
  options: RangeOption<Value>[],
  showIntermediateTickLabels: boolean
) {
  return options.map((option, index) => {
    if (!showIntermediateTickLabels) {
      return index === 0 || index === options.length - 1
        ? option.label
        : undefined;
    }
    return option?.label;
  });
}

export interface RangeFieldProps<Value>
  extends Omit<FieldProps<Value>, "value" | "onChange" | "name"> {
  /** The currently selected values */
  values: Value[];

  /**
   * A list of possible options to choose from. Each option has
   * a `value`, `label` and `position`.
   */
  options?: RangeOption<Value>[];

  /** The minimum value. Ignored if `options` is provided. */
  min?: number;

  /** Maximum value. Ignored if `options` is provided. */
  max?: number;

  /** Step size. Ignored if `options` is provided. */
  step?: number;

  /** Callback called when the selection changes */
  onChange?: (newValues: Value[]) => void;

  /** Whether the field is disabled */
  disabled?: boolean;

  label?: string;

  /** Theme variant used to fill selected options */
  variant?: Variant;

  thumbSize: string;

  /**
   * The initial position of the slider, when no value is set.
   */
  initialPosition?: number;

  /** Whether to show the ticks */
  showTicks?: boolean;

  /** Whether to show tick labels. Ignored if `showTicks=false`.  */
  showTickLabels?: boolean;

  /** Whether to show the label moving with the thumb. */
  showThumbLabel?: boolean;

  /**
   * Whether to show the ticklables inside the slider. If true,
   */
  showTickLabelsInside?: boolean;

  /**
   * An array of tick labels. Should be the same length as `options`.
   * If provided, `autoTickLabels` and `showIntermediateTickLabels` are
   * ignored.
   */
  tickLabels?: (string | undefined)[];

  /**
   * Whether to automatically infer tick labels whenever a tick label
   * is missing. If true, it will use tick values as labels. Default true;
   * ignored if `tickLabels is provided`.
   */
  autoTickLabels?: boolean;

  /**
   * Whether to show labels for intermediate ticks. If false, only the
   * labels of the endpoints are shown. Default false; ignored if `tickLabels`
   * is provided.
   */
  showIntermediateTickLabels?: boolean;

  /**
   * Whether the first and last tick label are aligned flush with the tick.
   * If false, these labels will also be centered below the tick. Default true.
   * Ignored when `showTickLabelsInside={true}`.
   */
  flushTickLabels?: boolean;
}

/**
 * A component that allows users to select values using a slider. At the
 * moment only a single thumb can be used, and so the field will function
 * as a slider. The underlying component, react-range, however allows
 * for using multiple thumbs to select a range. For now, however, it is
 * adviced to use `SliderField`, a thin wrapper around this component.
 *
 * Here typical use case might be a likert scale:
 *
 * ```tsx
 * <SliderField
 *  value="agree"
 *  options={[
 *    { value: "strongly_disagree", label: "strongly disagree" },
 *    { value: "disagree", label: "disagree" },
 *    { value: "neutral", label: "neither agree nor disagree" },
 *    { value: "agree", label: "agree" },
 *    { value: "strongly_agree", label: "strongly agree" },
 *   ]} />
 * ```
 */
export default function RangeField<Value>({
  values = [],
  options,
  min,
  max,
  step,
  onChange = () => {},
  error,
  disabled,
  label,
  initialPosition,
  tickLabels,
  variant = "primary",
  thumbSize,
  showThumbLabel = false,
  showTicks = true,
  showTickLabels = true,
  autoTickLabels = true,
  showTickLabelsInside = false,
  showIntermediateTickLabels = false,
  flushTickLabels = true,
}: RangeFieldProps<Value>) {
  const [hasValue, setHasValue] = useState(values.length > 0);

  if (values.length > 1) {
    throw Error("A range field with multiple thumbs is not yet supported.");
  }

  // Ensure we have both a valid options object and min, max and step defined.
  if (
    (!options || !options?.length) &&
    (min === undefined || max === undefined || step === undefined)
  ) {
    throw Error("Either provide `options` or `min`, `max` and `step`");
  }
  if (options) {
    // Add positions if the options don't have positions yet
    if (!havePositions(options))
      options.forEach((opt, idx) => (opt.position = idx));

    // Infer the min and max position, and the stepsize
    min = options[0].position!;
    max = options[options.length - 1].position!;
    step = step ?? (max - min) / (options.length - 1);
  } else {
    options = generateOptions(min!, max!, step!, autoTickLabels);
  }

  // Use tickLabels if specified, otherwise get the labels from option.label.
  if (tickLabels && tickLabels.length !== options.length) {
    console.warn("`tickLabels` should have the same length as `option`");
  }
  tickLabels = tickLabels ?? getTickLabels(options, showIntermediateTickLabels);

  // This callback first maps positions to values, and then calls onChange
  // with the values as argument.
  const handleChange = (positions: number[]) => {
    // Flag that a value has been set. This is to style the initial value
    if (!hasValue) setHasValue(true);

    const values = options
      .filter((opt) => positions.includes(opt.position!))
      .map((opt) => opt.value);
    onChange(values);
  };

  // The positions corresponding to active values
  let positions: number[] = options
    .filter((opt) => values.includes(opt.value))
    .map((opt) => opt.position!);

  if (!positions.length) {
    positions = [initialPosition ?? min ?? 0];
  }

  // Ensures that clicking the thumb or a tick sets an initial value.
  const handleFirstInteraction = () => {
    if (!hasValue) handleChange([...positions]);
  };

  if (showTickLabelsInside) {
    flushTickLabels = false;
  }

  return (
    <div>
      <div
        className={classNames(
          styles.rangeField,
          hasValue && styles.hasValue,
          error && styles.error,
          disabled && styles.disabled,
          showThumbLabel && styles.showThumbLabel,
          showTicks && styles.showTicks,
          showTickLabelsInside && styles.showTickLabelsInside,
          flushTickLabels && styles.flushTickLabels
        )}
        style={{ "--thumb-size": thumbSize }}
      >
        <Range
          label={label}
          values={positions}
          min={min}
          max={max}
          step={step}
          onChange={handleChange}
          disabled={disabled}
          renderTrack={(args) => <Track {...args} />}
          renderThumb={({ props: { key, ...rest }, ...args }) => (
            <Thumb
              key={key}
              props={rest}
              label={
                showThumbLabel &&
                options.filter((opt) => opt.value === values[args.index])[0]
                  .label
              }
              className={classNames(!error && `fill-${variant}`)}
              {...args}
              onMouseDown={handleFirstInteraction}
              onTouchStart={handleFirstInteraction}
            />
          )}
          renderMark={({ props: { key, ...rest }, index }) =>
            showTicks && (
              <Tick
                key={key}
                props={rest}
                label={showTickLabels && tickLabels[index]}
                className={classNames(
                  index === 0 && styles.first,
                  index === options.length - 1 && styles.last,
                  values.includes(options[index].value) && styles.active
                )}
                onMouseDown={handleFirstInteraction}
                onTouchStart={handleFirstInteraction}
              />
            )
          }
        />
      </div>
      {error && <p className={styles.errorMessage}>{error}</p>}
    </div>
  );
}

function Track({ children, isDragged, disabled, props }) {
  return (
    <div className={classNames(styles.track)}>
      <div className={classNames(styles.trackInner)} {...props}>
        {children}
      </div>
    </div>
  );
}

function Thumb({ isDragged, props, label, className, ...divProps }) {
  return (
    <div
      className={classNames(
        styles.thumb,
        isDragged & styles.dragging,
        className
      )}
      {...props}
      {...divProps}
    >
      {label && <div className={styles.thumbLabel}>{label}</div>}
    </div>
  );
}

function Tick({ props, label, className, ...divProps }) {
  return (
    <div
      className={classNames(styles.tick, className)}
      {...props}
      {...divProps}
    >
      <div className={styles.tickMark} />
      <div className={styles.tickLabel}>{label}</div>
    </div>
  );
}
