
import React from 'react';
import classNames from '@/util/classNames';

/**
 * The FloatingActionButton component is a reusable component that renders a floating action button with customizable position, icon, and content.
 * @param {Object} props - The props object containing the following properties:
 *   - children: The content to be rendered inside the floating action button.
 *   - icon: The icon class name for the button. Default value is 'fa-comment'.
 *   - position: The position of the button. Possible values are 'bottom-left', 'bottom-right', 'top-left', 'top-right', 'center-left', 'center-right'. Default value is 'center-right'.
 *   - className: Additional CSS class names for the button.
 * @returns {JSX.Element} The rendered FloatingActionButton component.
 */
const FloatingActionButton = ({
    children,
    icon = 'fa-comment',
    position = 'center-right', // 'bottom-left', 'bottom-right', 'top-left', 'top-right', 'center-left', 'center-right' (default)
    className,
}) => {

    const [expanded, setExpanded] = React.useState(false);

    /**
     * The getPositionClassNames function generates CSS class names based on the provided position string for a floating action button.
     * Which is used to position the button and overlay.
     * @param {string} position (e.g. 'bottom-left', 'center-right')
     * @returns {string} (e.g. 'floating-action-button--bottom floating-action-button--left' or 'floating-action-button--center floating-action-button--right')
     */
    const getPositionClassNames = (position) => {
        const [vertical, horizontal] = position.split('-');
        return `floating-action-button--${vertical} ${horizontal ? `floating-action-button--${horizontal}` : ''}`;
    }

    return (<>
        <div
            data-testid="floating-action-button"
            className={
                classNames("floating-action-button",
                    getPositionClassNames(position),
                    expanded && 'floating-action-button--expanded',
                    className
                )}
        >
            <button
                data-testid="floating-action-button__toggle-button"
                className='floating-action-button__toggle-button'
                onClick={() => setExpanded(!expanded)}
            >
                <i
                    data-testid="floating-action-button__icon"
                    className={`floating-action-button__icon fa ${expanded ? 'fa-times' : icon}`}
                />
            </button>
            <div
                data-testid="floating-action-button__content"
                className='floating-action-button__content'
            >
                {children}
            </div>
        </div>
        <div
            data-testid="floating-action-button__overlay"
            className={
                classNames(
                    'floating-action-button__overlay',
                    expanded && 'floating-action-button__overlay--expanded'
                )}
            onClick={() => setExpanded(false)}
            aria-hidden={expanded ? 'false' : 'true'}
            role="presentation"
        >
        </div>
    </>
    );
};

export default FloatingActionButton;

