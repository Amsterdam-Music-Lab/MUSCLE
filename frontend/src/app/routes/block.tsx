import type Block from "@/types/Block";
import type { ExperimentHelmetProps } from "./experiment";

import {
  Navigate,
  useLoaderData,
  useRouteLoaderData,
  redirect,
} from "react-router-dom";
import { ExperimentHelmet } from "./experiment";
// export { blockLoader } from "../loaders/blockLoader";
import { useRef } from "react";
import { fetchBlock, fetchNextRound } from "../api";
import Session from "@/types/Session";
import useBoundStore from "@/util/stores";

export async function blockLoader({ params }) {
  const block = await fetchBlock(params.blockSlug);
  if (!block) throw new Response("Block not found", { status: 404 });
  if (!block.session_id) throw "Session could not be created";

  // Save session in global store (since round depends on it)
  const session: Session = { id: block.session_id };
  useBoundStore.getState().setSession(session);

  // Load the first (!) round
  // const round = await fetchNextRound(session);
  // if (!round) throw "Round could not be loaded";
  // return redirect(`next?s=${session.id}`);

  // const theme = useBoundStore((state) => state.theme);
  // const setTheme = useBoundStore((state) => state.setTheme);
  // const resetTheme = useBoundStore((state) => state.resetTheme);

  return { block, session };
}

export interface BlockHelmetProps extends ExperimentHelmetProps {
  block: Block;
}

export function BlockHelmet({
  experiment,
  block,
  ...experimentHelmetProps
}: BlockHelmetProps) {
  const { data, ...rest } = experimentHelmetProps;
  let title = "Block";
  if (block?.name) title = `${title} – ${block.name}`;
  if (experiment?.name) title = `${title} – ${experiment.name}`;
  return (
    <ExperimentHelmet
      experiment={experiment}
      title={title}
      description={block.description}
      image={block.image?.file}
      data={{ type: "Block", ...data }}
      {...rest}
    />
  );
}

export function BlockPage() {
  const { participant } = useRouteLoaderData("root");
  const { experiment } = useRouteLoaderData("experiment");
  const { block, session, round } = useLoaderData();

  const playlist = useRef(null);

  // console.log(block, session, round);

  // Global state
  // const setGlobalCurrentAction = useBoundStore((s) => s.setCurrentAction);

  // Local component state, refs, etc
  // the current action. Note that every block consists
  // of rounds, which are sequences of actions, each action renders a view.
  // const startState = { view: "LOADING" } as Action;
  // const [actions, setActions] = useState<Action[]>([]);
  // const [currentAction, setCurrentAction] = useState<Action | null>(startState);
  // const playlist = useRef(null);

  // //////////////////////////////////////////////////////////////////////

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

  // /**
  //  * Continue to the next action in the current round
  //  */
  // const goToNextActionInRound = useCallback(
  //   (round: Action[]) => {
  //     setActions(round);
  //     const nextAction = round.shift() || null;
  //     updateCurrentAction(nextAction);
  //   },
  //   [updateCurrentAction]
  // );

  // /**
  //  * Continue to the next round within a block. This requires fetching
  //  * the round from the server.
  //  */
  // const goToNextRound = async (session: Session) => {
  //   const round = await getNextRound({ session });
  //   if (round) {
  //     goToNextActionInRound(round.next_round);
  //   } else {
  //     setError(
  //       "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
  //     );
  //     updateCurrentAction(null);
  //   }
  // };

  // /**
  //  * Continue to the next action. This is either the next action in the current
  //  * round, if such an action is left, or otherwise the first action in the
  //  * next round.
  //  */
  // const goToNextAction = async (endRound = false) => {
  //   if (!endRound && actions.length) {
  //     goToNextActionInRound(actions);
  //   } else {
  //     goToNextRound(session);
  //   }
  // };

  // /**
  //  * Handle the result of an action
  //  */
  // const handleActionResult = useResultHandler({ session, participant });

  // //////////////////////////////////////////////////////////////////////

  // /**
  //  * Go to the first round when the block and partipant have been loaded
  //  */
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

  // return <Navigate to={`next?s=${session.id}`} />;

  return (
    <>
      <BlockHelmet block={block} experiment={experiment} />
    </>
  );
}
