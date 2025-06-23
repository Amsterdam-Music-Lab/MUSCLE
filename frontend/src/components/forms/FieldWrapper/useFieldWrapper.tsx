/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { FieldWrapperChildProps } from "../types";
import type { FieldWrapperProps } from "../FieldWrapper";
import { useId, useCallback, useMemo } from "react";
import FieldWrapper from "./FieldWrapper";

export interface UseFieldWrapperProps {
  error?: string;
  showError?: boolean;
}

export function useFieldWrapper({
  error,
  showError = true,
}: UseFieldWrapperProps) {
  const id = useId();
  const hasError = error && showError;
  const errorId = `error-${id}`;
  const fieldId = `field-${id}`;

  const fieldProps = useMemo(
    () =>
      ({
        hasError,
        id: fieldId,
        "aria-describedby": hasError ? errorId : undefined,
        "aria-invalid": hasError,
      } as FieldWrapperChildProps),
    [hasError, fieldId, errorId]
  );

  const Wrapper = useCallback(
    (props: Omit<FieldWrapperProps, "fieldId" | "errorId" | "error">) => (
      <FieldWrapper
        error={hasError ? error : undefined}
        errorId={errorId}
        fieldId={fieldId}
        showError={showError}
        {...props}
      />
    ),
    [error, hasError, errorId, fieldId, showError]
  );
  return {
    FieldWrapper: Wrapper,
    fieldProps: fieldProps,
    hasError,
    errorId,
    fieldId,
  };
}
