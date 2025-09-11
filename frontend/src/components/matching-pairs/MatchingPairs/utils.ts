/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { act } from "@testing-library/react";

// Helper functions used in testing

export const filterCards = (result, filter) =>
  result.current.cards.filter(filter);

export const selectedCards = (result) => filterCards(result, (c) => c.selected);

export const selectCard = async (result, id: number) => {
  await act(async () => {
    await result.current.selectCard(id);
  });
};

export const endTurn = async (result) => {
  await act(async () => {
    result.current.endTurn();
  });
};

export const playTurn = async (result, id1: number, id2: number) => {
  await selectCard(result, id1);
  await selectCard(result, id2);
};

export const playCompleteTurn = async (result, id1: number, id2: number) => {
  await playTurn(result, id1, id2);
  await endTurn(result);
};
