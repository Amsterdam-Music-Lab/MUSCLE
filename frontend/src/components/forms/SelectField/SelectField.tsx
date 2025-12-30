/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { FieldOption } from "../types";
import type { SelectProps as ReactSelectProps } from "react-select";
import type { BaseFieldProps } from "../FieldWrapper";

import classNames from "classnames";
import { default as ReactSelect } from "react-select";
import { useLingui } from "@lingui/react/macro";
import { useFieldWrapper } from "../FieldWrapper";
import styles from "./SelectField.module.scss";

export interface SelectOption<Value> extends FieldOption<Value> {}

export interface SelectFieldProps<Value>
  extends BaseFieldProps,
    Omit<ReactSelectProps, "isSearchable" | "isClearable" | "isDisabled"> {
  options: SelectOption<Value>[];

  onChange: (newValue: Value) => void;

  // Aliases for consistent APIs

  /** Whether the options can be searched. Default true. */
  searchable?: ReactSelectProps["isSearchable"];

  /** Whether it is possible to clear the input. Default false. */
  clearable?: ReactSelectProps["isClearable"];
}

/**
 * An input field that allows the user to select one of multiple options
 * using a select input that can be searched.
 *
 * Note that this component is a thin wrapper around react-select.
 */
export default function SelectField<Value>({
  // Base field props
  error,
  showError,
  label,
  disabled,
  required,
  fieldWrapperProps = {},

  // Select props
  value,
  options,
  onChange,
  placeholder,
  clearable = false,
  searchable = true,
  ...selectProps
}: SelectFieldProps<Value>) {
  const { t } = useLingui();

  // Field wrapper and properties for input element
  const { FieldWrapper, hasError, fieldProps } = useFieldWrapper({
    error,
    showError,
  });

  const handleChange = (option: SelectOption<Value>) => {
    if (onChange) onChange(option.value);
  };

  const makeTheme = (theme) => ({
    ...theme,
    colors: {
      ...theme.colors,
      primary: "var(--primary-solid)",
      danger: "var(--danger-solid)",
    },
  });

  return (
    <FieldWrapper
      label={label}
      disabled={disabled}
      required={required}
      {...fieldWrapperProps}
    >
      <ReactSelect
        value={options.filter((opt) => opt.value === value)[0]}
        options={options}
        isDisabled={disabled}
        isClearable={clearable}
        isSearchable={searchable}
        className={classNames(styles.select, hasError && styles.hasError)}
        classNames={{
          container: (state) =>
            classNames(
              state.isFocused && styles.focused,
              state.isDisabled && styles.disabled
            ),
        }}
        placeholder={placeholder ?? t`Select...`}
        onChange={handleChange}
        theme={makeTheme}
        {...fieldProps} // These props don't end up at the right place yet
        {...selectProps}
      />
    </FieldWrapper>
  );
}
