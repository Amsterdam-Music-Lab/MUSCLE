# AML experiment client

The AML experiment client if the user facing part of the AML experiments. It mainly:

-   Shows a homepage/introduction
-   Handles the experiment flow by showing views based on the data received from the AML experiment server
-   Shows a user profile for the current experiment

### Block views

-   To use a new block view, add it to the block rules in your AML experiment server.
    -   The unique view ID (e.g. `MY_COMPONENT`) should match the component in the client
-   Create a new component

    -   Create your new component file, e.g. : `src/components/MyComponent/MyComponent.js`
    -   Add custom component styling in a scss file,e.g. `src/components/MyComponent/MyComponent.scss` and import it in `src/components/components.scss`

-   Add to (Experiment) Block

    -   Import your file to `src/components/Block/Block.jsx`
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

### Environment Variables

Use the following variables to configure your index.html file:

```
FRONTEND_HTML_PAGE_TITLE=Amsterdam Music Lab Experiment
FRONTEND_HTML_OG_DESCRIPTION=Listening experiments from the Amsterdam Music Lab. Test your musical knowledge and skills in engaging citizen-science experiments.
FRONTEND_HTML_OG_IMAGE=https://app.amsterdammusiclab.nl/images/og-hooked.jpg
FRONTEND_HTML_OG_TITLE=Amsterdam Music Lab Experiment
FRONTEND_HTML_OG_URL=https://app.amsterdammusiclab.nl
FRONTEND_HTML_BODY_CLASS=
```
