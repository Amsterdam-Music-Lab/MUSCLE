export const stateNextRound = (state) => {
  let newState = state.next_round.shift();
  newState.next_round = state.next_round;
  return newState;
}
