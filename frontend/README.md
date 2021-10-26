# AML experiment client

The AML experiment client if the user facing part of the AML experiments. It mainly:

-   Shows a homepage/introduction
-   Handles the experiment flow by showing views based on the data received from the AML experiment server
-   Shows a user profile for the current experiment

### Experiment views

-   To use a new experiment view, add it to the experiment rules in your AML experiment server.
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
