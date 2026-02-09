import Info from "../components/Info/Info";
import useBoundStore from "@/util/stores";

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2'});
};

const InfoDecorator = (Story) => {
    StoreDecorator();
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
        >
            <Story />
        </div>
    )
}

export default {
    title: "Info/Info",
    component: Info,
    parameters: {
        layout: "fullscreen",
    },
};

const defaultArgs = {
    heading: "This is the heading",
    body: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",  
}

export const Default = {
    args: {
        ...defaultArgs,
        button: {
            label: "Button Label",
            link: "https://www.example.com",
        }
    },
    decorators: [InfoDecorator],
};

export const WithButton = {
    args: {
        ...defaultArgs,
        button: {
            label: "Button Label",
        },
        onNext: () => alert("Next"),
    },
    decorators: [InfoDecorator],
};

export const WithOnNext = {
    args: {
        ...defaultArgs,
        button: {
            label: "Button Label",
        },
        onNext: () => alert("Next"),
    },
    decorators: [InfoDecorator],
};

export const WithLink = {
    args: {
        ...defaultArgs,
        button: {
            label: "Button Label",
            link: "https://www.example.com",
        }
    },
    decorators: [InfoDecorator],
};

export const WithoutButton = {
    args: defaultArgs,
    decorators: [InfoDecorator],
};
