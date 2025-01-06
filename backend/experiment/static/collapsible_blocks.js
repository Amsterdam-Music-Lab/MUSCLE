/**
 * Initializes an (inline) block form by adding a collapsible toggle button to the header
 * and setting up the initial collapsed state of the form.
 *
 * @param {HTMLElement} blockForm - The block form element to initialize.
 */
function initializeBlockForm(blockForm) {

  console.log('initializeBlockForm');

  let header = blockForm.querySelector('h3');

  // Only add toggle button if it doesn't exist
  if (header && !header.querySelector('.collapse-toggle')) {
    const toggleBtn = document.createElement('span');
    toggleBtn.className = 'collapse-toggle';
    toggleBtn.innerHTML = '▼';
    toggleBtn.style.marginLeft = '10px';
    toggleBtn.style.cursor = 'pointer';
    header.appendChild(toggleBtn);
  }

  header = blockForm.querySelector('h3');

  const hasClickEventListener = header.getAttribute('data-initialized') === 'true';

  if (!hasClickEventListener) {
    // Add click handler to header
    header.addEventListener('click', toggleVisibilityClickHandler);
  }

  header.setAttribute('data-initialized', 'true');

  function toggleVisibilityClickHandler(e) {
    toggleBlockVisibility(blockForm);
  }

  // Initialize as collapsed by default
  const contentSections = [
    blockForm.querySelector('fieldset'),                                            // Main block form
    blockForm.querySelector('.djn-group-nested[data-inline-model="experiment-blocktranslatedcontent"]')  // Translated content form
  ];

  contentSections.forEach(section => {
    if (section) {
      section.style.display = 'none';
    }
  });

  blockForm.classList.add('collapsed');

  // Initialize playlist input
  django.jQuery('.django-select2').djangoSelect2();
}

function toggleBlockVisibility(blockForm) {

  console.log('toggleBlockVisibility');

  const contentSections = [
    blockForm.querySelector('fieldset'),                                            // Main block form
    blockForm.querySelector('.djn-group-nested[data-inline-model="experiment-blocktranslatedcontent"]')  // Translated content form
  ];

  const toggleBtn = blockForm.querySelector('.collapse-toggle');
  const isCollapsed = blockForm.classList.contains('collapsed');

  contentSections.forEach(section => {
    if (section) {
      section.style.display = isCollapsed ? 'block' : 'none';
    }
  });

  if (isCollapsed) {
    toggleBtn.innerHTML = '▲';
    blockForm.classList.remove('collapsed');
  } else {
    toggleBtn.innerHTML = '▼';
    blockForm.classList.add('collapsed');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Initialize all existing blocks
  document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
    initializeBlockForm(blockForm);

    // Expand block form if there are errors in it (i.e. .errors or .errorlist)
    if (blockForm.querySelector('.errors, .errorlist')) {
      toggleBlockVisibility(blockForm);
    }
  });

  // Add expand/collapse all buttons at the top
  const firstBlock = document.querySelector('.djn-inline-form[data-inline-model="experiment-block"]');

  if (firstBlock) {
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'collapse-buttons-container';

    const expandAllBtn = document.createElement('button');
    expandAllBtn.type = 'button';
    expandAllBtn.innerText = 'Expand All Blocks';
    expandAllBtn.className = 'expand-all-btn';

    // Add click handler to expand all blocks
    expandAllBtn.addEventListener('click', function (e) {
      e.stopPropagation();

      document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
        if (blockForm.classList.contains('collapsed')) {
          toggleBlockVisibility(blockForm);
        }
      });
    });

    const collapseAllBtn = document.createElement('button');
    collapseAllBtn.type = 'button';
    collapseAllBtn.innerText = 'Collapse All Blocks';
    collapseAllBtn.className = 'collapse-all-btn';

    collapseAllBtn.addEventListener('click', function (e) {
      e.stopPropagation();

      document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
        if (!blockForm.classList.contains('collapsed')) {
          toggleBlockVisibility(blockForm);
        }
      });
    });

    buttonsContainer.appendChild(expandAllBtn);
    buttonsContainer.appendChild(collapseAllBtn);
    firstBlock.parentNode.insertBefore(buttonsContainer, firstBlock);
    firstBlock.parentNode.parentNode.querySelector('h2').appendChild(buttonsContainer);
  }

  // Add observer for dynamically added blocks (e.g. when adding a new block)
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      mutation.addedNodes.forEach(function (node) {
        if (node.nodeType === 1 && node.matches('.djn-inline-form[data-inline-model="experiment-block"]')) {

          // Initialize newly added block by adding toggle button, etc.
          initializeBlockForm(node);

          // Expand every newly added inline block form
          toggleBlockVisibility(node);
        }
      });
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

});
