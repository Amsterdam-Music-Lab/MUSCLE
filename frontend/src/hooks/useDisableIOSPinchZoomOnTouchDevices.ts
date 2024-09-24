import { useEffect } from 'react';

const useDisableIOSPinchZoomOnTouchDevices = () => useEffect(() => {
    const isTouchDevice = () => !!('ontouchstart' in window || !!(navigator.maxTouchPoints));

    const handlePinchZoom = (event: Event) => {
        if (isTouchDevice()) {
            event.preventDefault();
        }
    };

    document.addEventListener('gesturestart', handlePinchZoom);

    return () => {
        document.removeEventListener('gesturestart', handlePinchZoom);
    };
}, []);


export default useDisableIOSPinchZoomOnTouchDevices;
