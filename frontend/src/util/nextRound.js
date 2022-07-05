// Get next round from given state
export const stateNextRound = (state) => {
  if (!state.next_round){
    return {};
  }

  if (!Array.isArray(state.next_round)){
    return state.next_round;
  }

  const newState = state.next_round.shift();
  newState.next_round = state.next_round;
  return newState;
}