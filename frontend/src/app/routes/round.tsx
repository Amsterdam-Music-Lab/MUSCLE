import Session from "@/types/Session";
import { fetchNextRound } from "../api";
import {
  useNavigate,
  useLocation,
  Navigate,
  useLoaderData,
  useRouteLoaderData,
  redirect,
} from "react-router-dom";
import { useRef, useState, useCallback } from "react";
import type Action from "@/types/Action";
import useBoundStore from "@/util/stores";

export async function roundLoader({ request }) {
  const sessionId = new URL(request.url).searchParams.get("s");
  if (!sessionId) throw "No valid valid session found";
  const session: Session = { id: parseInt(sessionId) };
  const round = await fetchNextRound(session);
  if (!round) throw "Next round could not be loaded";
  console.log("round loader", session, round);
  return { round, session };
}

export function RoundPage() {
  const { participant } = useRouteLoaderData("root");
  const { experiment } = useRouteLoaderData("experiment");
  const { block } = useRouteLoaderData("block");
  const { round, session } = useLoaderData();
  console.log("ROUND");

  const [actions, setActions] = useState<Action>(round);
  const [currentAction, setCurrentAction] = useState<Action>(actions[0]);
  const playlist = useRef(null);

  //////////////////////////////////////////////////////////////////////

  // /**
  //  * Update the current action to the passed action, updating
  //  * both the local and global state and forcing a re-render
  //  */
  // const updateCurrentAction = useCallback(
  //   (action: Action) => {
  //     const newAction = action ? { ...action } : null;
  //     setCurrentAction(newAction);
  //     setGlobalCurrentAction(newAction);
  //   },
  //   [setCurrentAction, setGlobalCurrentAction]
  // );

  /**
   * Continue to the next round within a block. This requires fetching
   * the round from the server.
   */
  // const goToNextRound = async (session: Session) => {
  // const round = await getNextRound({ session });
  // if (round) {
  //   goToNextActionInRound(round.next_round);
  // } else {
  //   setError(
  //     "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
  //   );
  //   updateCurrentAction(null);
  // }
  // };

  const navigate = useNavigate();
  const { pathname } = useLocation();

  /**
   * Continue to the next action in the current round
   */
  const goToNextActionInRound = useCallback(
    (round: Action[]) => {
      setActions(round);
      const nextAction = round.shift() || null;
      setCurrentAction(nextAction);
    },
    [setCurrentAction]
  );

  /**
   * Continue to the next action. This is either the next action in the current
   * round, if such an action is left, or otherwise the first action in the
   * next round.
   */
  const goToNextAction = async (endRound = false) => {
    if (!endRound && actions.length) {
      goToNextActionInRound(actions);
    } else {
      // Go go same page again
      return navigate(`${pathname}?s=${session.id}&t=${Date.now()}`);
    }
  };

  /**
   * Handle the result of an action
   */
  // const handleActionResult = useResultHandler({ session, participant });

  //////////////////////////////////////////////////////////////////////

  /**
   * Go to the first round when the block and partipant have been loaded
   */
  // useEffect(() => {
  //   if (participant && block && !(!block.session_id && session)) {
  //     goToNextRound({ id: block.session_id });
  //   }
  // }, [block, session]);

  // // Check if there's a valid action
  // useEffect(() => {
  //   if (!currentAction || !currentAction.view)
  //     setError("No valid current action");
  // }, [currentAction, setError]);

  // // Whether the action has a valid view
  // const isValidAction = currentAction?.view in VIEW_NAMES;

  // return !isValidAction ? (
  //   <View
  //     name="error"
  //     message={`Invalid action unsupported view (${JSON.stringify(
  //       currentAction
  //     )}`}
  //   />
  // ) : (
  //   <View
  //     name={VIEW_NAMES[currentAction.view]}
  //     onNext={goToNextAction}
  //     onResult={handleActionResult}
  //     playlist={playlist}
  //     action={currentAction}
  //   />
  // );

  return "ASDFADFASD";
}
