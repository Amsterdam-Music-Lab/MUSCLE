// collapsible_blocks.js

function initializeBlockForm(blockForm) {
  const header = blockForm.querySelector('h3');

  // Only add toggle button if it doesn't exist
  if (header && !header.querySelector('.collapse-toggle')) {
    const toggleBtn = document.createElement('span');
    toggleBtn.className = 'collapse-toggle';
    toggleBtn.innerHTML = '►';  // Start collapsed
    toggleBtn.style.marginLeft = '10px';
    toggleBtn.style.cursor = 'pointer';
    header.appendChild(toggleBtn);

    // Add click handler to header
    header.addEventListener('click', function (e) {
      // Don't trigger if clicking on other buttons in the header
      if (e.target.classList.contains('djn-remove-handler') ||
        e.target.classList.contains('inline-deletelink')) {
        return;
      }

      toggleBlockVisibility(blockForm);
    });
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
}

function toggleBlockVisibility(blockForm) {
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
    toggleBtn.innerHTML = '▼';
    blockForm.classList.remove('collapsed');
  } else {
    toggleBtn.innerHTML = '►';
    blockForm.classList.add('collapsed');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Initialize all existing blocks
  document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
    initializeBlockForm(blockForm);
  });

  // Add expand/collapse all buttons at the top
  const firstBlock = document.querySelector('.djn-inline-form[data-inline-model="experiment-block"]');
  if (firstBlock) {
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'collapse-buttons-container';
    buttonsContainer.style.marginBottom = '10px';

    const expandAllBtn = document.createElement('button');
    expandAllBtn.type = 'button';
    expandAllBtn.innerText = 'Expand All Blocks';
    expandAllBtn.className = 'expand-all-btn';
    expandAllBtn.onclick = function () {
      document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
        if (blockForm.classList.contains('collapsed')) {
          toggleBlockVisibility(blockForm);
        }
      });
    };

    const collapseAllBtn = document.createElement('button');
    collapseAllBtn.type = 'button';
    collapseAllBtn.innerText = 'Collapse All Blocks';
    collapseAllBtn.className = 'collapse-all-btn';
    collapseAllBtn.onclick = function () {
      document.querySelectorAll('.djn-inline-form[data-inline-model="experiment-block"]').forEach(blockForm => {
        if (!blockForm.classList.contains('collapsed')) {
          toggleBlockVisibility(blockForm);
        }
      });
    };

    buttonsContainer.appendChild(expandAllBtn);
    buttonsContainer.appendChild(collapseAllBtn);
    firstBlock.parentNode.insertBefore(buttonsContainer, firstBlock);
  }
});

// Add observer for dynamically added blocks
const observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    mutation.addedNodes.forEach(function (node) {
      if (node.nodeType === 1 && node.matches('.djn-inline-form[data-inline-model="experiment-block"]')) {
        initializeBlockForm(node);
      }
    });
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
