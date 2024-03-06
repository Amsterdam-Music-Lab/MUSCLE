import React from 'react';
import { createRoot } from 'react-dom/client';
import { act } from 'react-dom/test-utils';
import FontLoader from './FontLoader';


describe('FontLoader', () => {
  let container = null;
  let root = null;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    document.head.querySelectorAll('link, style').forEach(el => el.remove());
    container.remove();
    container = null;
    root.unmount();
  });


  it('renders without crashing', () => {
    act(() => {
      root = createRoot(container);
      root.render(<FontLoader />);
    });
    expect(container.innerHTML).toBe('');
  });

  it('loads the font and sets the global font style', async () => {
    const fontUrl = 'https://fonts.googleapis.com/css?family=Roboto';
    const fontType = 'heading';

    act(() => {
      root = createRoot(container);
      root.render(<FontLoader fontUrl={fontUrl} fontType={fontType} />);
    });

    const linkElement = document.querySelector('link[href="' + fontUrl + '"]');
    const styleElement = document.querySelector('style');

    expect(linkElement).not.toBeNull();
    expect(styleElement).not.toBeNull();
    expect(styleElement.innerHTML).toContain('font-family: "Roboto", sans-serif;');

    act(() => {
      root.unmount();
    });

    const removedLinkElement = document.querySelector('link[href="' + fontUrl + '"]');
    const removedStyleElement = document.querySelector('style');

    expect(removedLinkElement).toBeNull();
    expect(removedStyleElement).toBeNull();
  });

  it('does not load the font if fontUrl is not provided', async () => {
    act(() => {
      root = createRoot(container);
      root.render(<FontLoader />);
    });

    const linkElement = document.querySelector('link');
    const styleElement = document.querySelector('style');

    expect(linkElement).toBeNull();
    expect(styleElement).toBeNull();
  });
});