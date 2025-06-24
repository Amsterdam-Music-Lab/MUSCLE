/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

/**
 * Utility function for adding a description to a story:
 *
 * ```ts
 * export const Default: Story = {
 *  ...description("Description of this story"),
 *  args: {
 *    //...
 *  }
 * };
 * ```
 */
export function description(description: string) {
  return {
    parameters: {
      docs: {
        description: {
          story: description,
        },
      },
    },
  };
}
