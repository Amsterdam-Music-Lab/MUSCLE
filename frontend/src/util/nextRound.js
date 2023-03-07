export const stateNextRound = (state) => {
  let newState = state.next_round.shift();
  if (!newState) return;
  newState.next_round = state.next_round;
  return newState;
}
