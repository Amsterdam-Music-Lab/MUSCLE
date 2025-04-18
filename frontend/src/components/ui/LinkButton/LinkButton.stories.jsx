import LinkButton from "./LinkButton";

export default {
  title: "UI/LinkButton",
  component: LinkButton,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div
    style={{
      maxWidth: "200px",
      height: "100%",
      padding: "1rem",
      background: "#eee",
    }}
  >
    <Story />
  </div>
);

export const ExternalLink = {
  args: {
    children: "Google",
    link: "https://google.com",
  },
  decorators: [decorator],
};

export const InternalLink = {
  args: {
    children: "Google",
    link: "/",
  },
  decorators: [decorator],
};

export const NoLink = {
  args: {
    children: "Google",
    onClick: () => {
      window.alert("Click!");
    },
  },
  decorators: [decorator],
};

export const Size = {
  args: {
    children: "Google",
    link: "/",
    size: "lg",
    variant: "secondary",
  },
  decorators: [decorator],
};
