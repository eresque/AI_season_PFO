import React from 'react';
import classNames from 'classnames';
import './style.scss';

type ButtonProps = {
    children: React.ReactNode,
    onClick: React.MouseEventHandler<HTMLButtonElement>,
    className: string,
    active: boolean,
    style?: React.CSSProperties
};

const Button = (props: ButtonProps): JSX.Element => {

    const classes = classNames(
        props.className,
        'active-' + props.active.toString(),
    );

    return(
        <button 
            className={classes}
            onClick={props.onClick}
            style={props.style}
        >{props.children}</button>
    );
};

Button.defaultProps = {
    children: 'Button',
    onClick: () => {},
    className: '',
    active: false,
    style: {}
};

export default Button; 