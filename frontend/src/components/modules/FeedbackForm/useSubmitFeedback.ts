/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Participant } from "@/types/Participant";
import { useCallback } from "react";
import { postFeedback } from "@/API";

export function useSubmitFeedback(blockSlug: string, participant: Participant) {
  const onSubmit = useCallback(
    async (value: string) => {
      const result = await postFeedback({
        feedback: value,
        blockSlug,
        participant,
      });
      return result;
    },
    [blockSlug, participant]
  );
  return onSubmit;
}
