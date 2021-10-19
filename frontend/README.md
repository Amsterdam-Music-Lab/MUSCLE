# Hooked client

The Hooked client if the user facing part of the Hooked experiments. It mainly:

-   Shows a homepage/introduction
-   Handles the experiment flow by showing views based on the data received from the Hooked server
-   Shows a user profile for the current experiment

## Install

### Prerequisites

-   Install `node` (Javascript runtime environment, https://nodejs.org/) on your local system.
-   Install `yarn` (package manager, https://yarnpkg.com/) on your local system.

### Install packages

-   Install packages: run `yarn install` in the repository root
-   Copy `.env.dev.dist` to `.env` - adapt it to your needs

### Start

-   First start the Hooked server
-   Start application: `yarn start`

---

Tip: Make sure you have your Hooked-server running at localhost:8000 as the Hooked-client will run on localhost:3000. (Same domains, required for sharing cookies)

---

## Development

### Prerequisites

-   Install `prettier` (code formatter, https://prettier.io/) on your local system and setup your editor to format on save.

### Develop

-   Start application: `yarn start`
-   Watch scss: `yarn run scss`
-   When you make changes to your files, the client is automatically compiled and (hot) reloaded in the browser

---

Tip: Make sure to fix all jslint warnings/errors (output of `yarn start` or browser console messages)

---

### Experiment views

-   To use a new experiment view, add it to the experiment rules in your Hooked server.
    -   The unique view ID (e.g. `MY_COMPONENT`) should match the component in the client
-   Create a new component

    -   Create your new component file, e.g. : `src/components/MyComponent/MyComponent.js`
    -   Add custom component styling in a scss file,e.g. `src/components/MyComponent/MyComponent.scss` and import it in `src/components/components.scss`

-   Add to Experiment

    -   Import your file to `src/components/Experiment/Experiment.js`
        ```javascript
        import MyComponent from "../MyComponent/MyComponent";
        ```
    -   Add your view to the render function switch:
        ```javascript
        case "MY_COMPONENT":
            return <MyComponent {...attrs} />;
        ```

---

Tip: Use SongBool or SongSync as an example when creating a new view with audio playback.

---

## Production

To create a production build:

-   Copy `.env.prod.dist` to `.env` - adapt it to your needs
-   Optionally add/tweak the `homepage` field in `package.json` (in case the client is hosted in a specific folder instead of the server root).
-   Run build command: `yarn run build`
-   Copy the build folder contents to your server
