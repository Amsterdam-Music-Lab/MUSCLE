export interface FieldProps<Value> {
  /** Value of the input */
  value?: Value;

  /** Name for the input field */
  name: string;

  /** Callback fired when the input changes */
  onChange: (newValue: Value) => void;

  /** Whether the input is disabled. */
  disabled?: boolean;

  /** An optional error message */
  error?: string;

  /** Whether to show the error (even if there is one) */
  showError?: boolean;
}

export interface FieldOption<Value> {
  /** The value of the option */
  value: Value;

  /** A label describing the value */
  label?: string;

  /** Whether it is disabled */
  disabled?: boolean;
}
