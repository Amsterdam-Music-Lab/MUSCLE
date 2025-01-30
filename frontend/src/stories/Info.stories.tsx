import Info from "../components/Info/Info";

export default {
    title: "Info/Info",
    component: Info,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        heading: "This is the heading",
        body: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",
        button_label: "Button Label",
        button_link: "https://www.example.com",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithButton = {
    args: {
        heading: "This is the heading",
        body: "Cantus firmus, vox humana, Melodia fluitans, symphonia grandis. Modulatio ingeniosa, tonus profundus, Fugae artificium, chori celestis.",
        button_label: "Button Label",
        onNext: () => alert("Next"),
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithOnNext = {
    args: {
        heading: "This is the heading",
        body: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",
        button_label: "Button Label",
        onNext: () => alert("Next"),
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithLink = {
    args: {
        heading: "This is the heading",
        body: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",
        button_label: "Button Label",
        button_link: "https://www.example.com",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithoutButton = {
    args: {
        heading: "This is the heading",
        body: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
