class MarkdownPreview extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });

        // Create a style element
        const style = document.createElement('style');
        style.style.display = 'none';
        style.textContent = `

                    :host {
                        display: block;
                        padding: 1rem;
                        background-color: var(--body-bg);
                        color: var(--body-fg);
                        border-radius: 5px;
                        overflow: auto;
                        line-height: 1.75;
                    }

                    * {
                        all: initial;
                        font-family: inherit;
                        box-sizing: border-box;
                    }

                    h1, h2, h3, h4, h5, h6 {
                        display: block;
                        color: var(--text-fg);
                        background-color: transparent;
                        font-weight: bold;
                        line-height: 1.25;
                        margin-top: 0.5em;
                        margin-bottom: 0.5em;
                    }

                    h1 {
                        font-size: 2em;
                    }

                    h2 {
                        font-size: 1.75em;
                    }

                    h3 {
                        font-size: 1.5em;
                    }

                    h4 {
                        font-size: 1.25em;
                    }

                    h5 {
                        font-size: 1em;
                    }

                    h6 {
                        font-size: 0.875em;
                    }

                    p {
                        display: block;
                        margin-top: 1rem;
                        margin-bottom: 1rem;
                    }

                    a {
                        color: var(--link-fg);
                        text-decoration: underline;
                    }

                    a:hover {
                        color: var(--link-hover-fg);
                        text-decoration: underline;
                    }

                    strong {
                        font-weight: bold;
                    }

                    em {
                        font-style: italic;
                    }

                    ul, ol {
                        display: block;
                        margin-top: 1rem;
                        margin-bottom: 1rem;
                        padding-left: 2rem;
                    }

                    ul li, ol li {
                        display: list-item;
                        margin-bottom: .25rem;
                        list-style-position: inside;
                        list-style-type: disc;
                    }

                    blockquote {
                        display: block;
                        margin-top: 1em;
                        margin-bottom: 1em;
                        padding: 0.5em 1em;
                        background-color: #f5f5f5;
                        border-left: 4px solid #ccc;
                    }

                    code {
                        display: inline;
                        font-family: Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace;
                        background-color: #f5f5f5;
                        padding: 0.2em 0.4em;
                        font-size: 0.9em;
                        border-radius: 3px;
                    }

                    pre {
                        display: block;
                        margin-top: 1em;
                        margin-bottom: 1em;
                        background-color: #f5f5f5;
                        padding: 1em;
                        overflow: auto;
                        border-radius: 5px;
                    }

                    pre code {
                        background-color: transparent;
                        padding: 0;
                        white-space: pre;
                    }

                    img {
                        max-width: 100%;
                        height: auto;
                    }
                `;

        // Attach the style element to the shadow root
        shadow.appendChild(style);

        // Now, create and append the content container
        const contentDiv = document.createElement('div');
        contentDiv.setAttribute('id', 'markdownContent');
        // Append the content container to the shadow root
        shadow.appendChild(contentDiv);
    }

    set markdown(html) {
        this.shadowRoot.getElementById('markdownContent').innerHTML = html;
    }
}

customElements.define('markdown-preview', MarkdownPreview);

function renderMarkdown(textarea, markdownPreview) {
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const url = markdownPreview.getAttribute('data-url');

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify({
            markdown: textarea.value
        })
    })
        .then(response => response.json())
        .then(data => {
            markdownPreview.markdown = data.html;
        });
}

function initializeMarkdownWidget(widget) {
    const tabs = widget.querySelectorAll('.tab');
    const textarea = widget.querySelector('textarea');
    const markdownPreview = widget.querySelector('markdown-preview');

    // Remove existing event listeners before adding new ones
    tabs.forEach(tab => {
        tab.removeEventListener('click', tabClickHandler);
        tab.addEventListener('click', tabClickHandler);
    });

    textarea.removeEventListener('blur', textareaBlurHandler);
    textarea.addEventListener('blur', textareaBlurHandler);

    // Initial render
    renderMarkdown(textarea, markdownPreview);
}

function tabClickHandler(event) {
    const widget = event.target.closest('.markdown-preview-text-input');
    const tabs = widget.querySelectorAll('.tab');
    const tabContents = widget.querySelectorAll('.tab-content');
    const clickedIndex = Array.from(tabs).indexOf(event.target);

    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');

    tabContents.forEach(content => content.classList.remove('active'));
    tabContents[clickedIndex].classList.add('active');
}

function textareaBlurHandler(event) {
    const widget = event.target.closest('.markdown-preview-text-input');
    const markdownPreview = widget.querySelector('markdown-preview');
    renderMarkdown(event.target, markdownPreview);
}

function initializeAllMarkdownWidgets() {
    const markdownWidgets = document.querySelectorAll('.markdown-preview-text-input');
    markdownWidgets.forEach(initializeMarkdownWidget);
}

document.addEventListener('DOMContentLoaded', function () {
    initializeAllMarkdownWidgets();

    // Set up a MutationObserver to watch for new elements
    const targetNode = document.body;
    const config = { childList: true, subtree: true };

    const callback = function (mutationsList, observer) {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const newWidgets = node.querySelectorAll('.markdown-preview-text-input');
                        newWidgets.forEach(initializeMarkdownWidget);
                    }
                });
            }
        }
    };

    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
});

// Handle Django's formset 'add' button
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('add-form-row')) {
        // Wait for Django to add the new form to the DOM
        setTimeout(initializeAllMarkdownWidgets, 0);
    }
});
