import ProgressBar from "../components/ProgressBar/ProgressBar";
import useBoundStore from "@/util/stores";

export default {
    title: "Progress/ProgressBar",
    component: ProgressBar,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        value: 3,
        max: 20,
        label: "3 / 20",
    },
    decorators: [
        (Story) => {
            const setTheme = useBoundStore((state) => state.setTheme);
            setTheme({ colorPrimary: "#d843e2" });
            return (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        )},
    ],
};
