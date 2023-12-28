
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
        <div className={
            classNames("floating-action-button",
                getPositionClassNames(position),
                expanded && 'floating-action-button--expanded',
                className
            )}>
            <button
                className='floating-action-button__toggle-button'
                onClick={() => setExpanded(!expanded)}
            >
                {expanded ? <i className={`floating-action-button__icon fa fa-times`}></i> : <i className={`floating-action-button__icon fa ${icon}`}></i>}
            </button>
            <div className='floating-action-button__content'>
                {children}
            </div>
        </div>
        <div className={
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

