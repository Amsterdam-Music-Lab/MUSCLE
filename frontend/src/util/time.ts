export const getCurrentTime = () => Date.now() / 1000;

export const getTimeSince = (time: number) => getCurrentTime() - time;
