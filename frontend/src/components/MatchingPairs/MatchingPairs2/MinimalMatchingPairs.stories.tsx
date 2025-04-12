import MinimalMatchingPairs from "./MinimalMatchingPairs";

const decorator = (Story) => (
  <div id="root" style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export default {
  title: "Matching Pairs/Minimal",
  component: MinimalMatchingPairs,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const cards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    value: index % 8,
  }))
  .sort(() => Math.random() - 0.5);

export const Default = {
  args: { cards: [...cards] },
  decorators: [decorator],
};
