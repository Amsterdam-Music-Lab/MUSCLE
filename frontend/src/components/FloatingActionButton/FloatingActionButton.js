
import React from 'react';
import classNames from 'util/classNames';

const FloatingActionButton = ({
    children,
    icon = 'fa-comment',
    position = 'center-right',
    className,
}) => {

    const [expanded, setExpanded] = React.useState(false);

    /**
     * @param {string} position
     * @returns {string}
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

