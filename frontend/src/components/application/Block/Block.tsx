/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type Session from "@/types/Session";
import type { Action } from "@/types/Action";
import { useState, useEffect, useCallback, useRef } from "react";
import useBoundStore from "@/util/stores";
import { getNextRound } from "@/API";
import useResultHandler from "@/hooks/useResultHandler";
import { View } from "@/components/application";
import useLogLifeCycle from "@/util/useLogLifeCycle";
import { useBlockContext } from "../App/AppRoutes";

const VIEW_NAMES = {
  TRIAL_VIEW: "trial",
  EXPLAINER: "explainer",
  SCORE: "score",
  FINAL: "final",
  PLAYLIST: "playlists",
  LOADING: "loading",
  INFO: "info",
  ERROR: "error",
};

/**
 * Component that controls an experiment block:
 * - Loads the block and participant
 * - Renders the view based on the state that is provided by the server
 * - It handles sending results to the server
 */
export default function Block() {
  useLogLifeCycle("Block"); // TO BE REMOVED

  const { block, session } = useBlockContext();

  // Global state
  const setError = useBoundStore((state) => state.setError);
  const participant = useBoundStore((state) => state.participant);
  const setGlobalCurrentAction = useBoundStore((s) => s.setCurrentAction);

  // Local component state, refs, etc
  // the current action. Note that every block consists
  // of rounds, which are sequences of actions, each action renders a view.
  const startState = { view: "LOADING" } as Action;
  const [actions, setActions] = useState<Action[]>([]);
  const [currentAction, setCurrentAction] = useState<Action | null>(startState);
  const playlist = useRef(null);

  //////////////////////////////////////////////////////////////////////

  /**
   * Update the current action to the passed action, updating
   * both the local and global state and forcing a re-render
   */
  const updateCurrentAction = useCallback(
    (action: Action) => {
      const newAction = action ? { ...action } : null;
      setCurrentAction(newAction);
      setGlobalCurrentAction(newAction);
    },
    [setCurrentAction, setGlobalCurrentAction]
  );

  /**
   * Continue to the next action in the current round
   */
  const goToNextActionInRound = useCallback(
    (round: Action[]) => {
      setActions(round);
      const nextAction = round.shift() || null;
      updateCurrentAction(nextAction);
    },
    [updateCurrentAction]
  );

  /**
   * Continue to the next round within a block. This requires fetching
   * the round from the server.
   */
  const goToNextRound = async (session: Session) => {
    const round = await getNextRound({ session });
    if (round) {
      goToNextActionInRound(round.next_round);
    } else {
      setError(
        "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
      );
      updateCurrentAction(null);
    }
  };

  /**
   * Continue to the next action. This is either the next action in the current
   * round, if such an action is left, or otherwise the first action in the
   * next round.
   */
  const goToNextAction = async (endRound = false) => {
    if (!endRound && actions.length) {
      goToNextActionInRound(actions);
    } else {
      goToNextRound(session);
    }
  };

  /**
   * Handle the result of an action
   */
  const handleActionResult = useResultHandler({ session, participant });

  //////////////////////////////////////////////////////////////////////

  /**
   * Go to the first round when the block and partipant have been loaded
   */
  useEffect(() => {
    if (participant && block && !(!block.session_id && session)) {
      goToNextRound({ id: block.session_id });
    }
  }, [block, session]);

  // Check if there's a valid action
  useEffect(() => {
    if (!currentAction || !currentAction.view)
      setError("No valid current action");
  }, [currentAction, setError]);

  // Whether the action has a valid view
  const isValidAction = currentAction?.view in VIEW_NAMES;

  return !isValidAction ? (
    <View
      name="error"
      message={`Invalid action unsupported view (${JSON.stringify(
        currentAction
      )}`}
    />
  ) : (
    <View
      name={VIEW_NAMES[currentAction.view]}
      onNext={goToNextAction}
      onResult={handleActionResult}
      playlist={playlist}
      action={currentAction}
    />
  );
}
