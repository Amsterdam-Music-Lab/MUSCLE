import { useEffect } from 'react';

const useDisableRightClickOnTouchDevices = () => useEffect(() => {
  const isTouchDevice = () => !!('ontouchstart' in window || !!(navigator.maxTouchPoints));

  const handleContextMenu = (event) => {
    if (isTouchDevice()) {
      event.preventDefault();
    }
  };

  document.addEventListener('contextmenu', handleContextMenu);

  return () => {
    document.removeEventListener('contextmenu', handleContextMenu);
  };
}, []);


export default useDisableRightClickOnTouchDevices;
