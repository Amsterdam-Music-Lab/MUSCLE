import { fetchBlock } from "../api";

export async function blockLoader({ params }) {
  const block = await fetchBlock(params.blockSlug);
  if (!block) throw new Response("Block not found", { status: 404 });

  // const session = useBoundStore.getState().session;
  // const setSession = useBoundStore.getState().setSession;
  // const setBlock = useBoundStore.getState().setBlock;
  // const theme = useBoundStore((state) => state.theme);
  //   const setTheme = useBoundStore((state) => state.setTheme);
  //   const resetTheme = useBoundStore((state) => state.resetTheme);
  //   setSession({ id: block.session_id });

  return block;
}
