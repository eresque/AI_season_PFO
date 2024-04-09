import React from "react";
import classNames from 'classnames';
import './style.scss';

type RadioButtonProps = {
    className?: string,
    label: string,
    value: string,
    obj: Object,
    checked: boolean,
    onChange: React.ChangeEventHandler<HTMLInputElement>,
    onClickAlarm: React.MouseEventHandler<HTMLLabelElement>,
    onClickArrData: React.MouseEventHandler<HTMLLabelElement>
};

const RadioButton = (props: RadioButtonProps) => {

    const classes = classNames(
        'radio-btn',
        props.className,
    );

    const obj: any = props.obj;
    const arrData: any = [];
    Object.keys(obj).forEach((key) => {
        arrData.push(obj[key].toString());
    });

    return (
        <>
            <label 
                className={classes} 
                onClick={() => {
                    props.onClickAlarm(obj.risk_factor); 
                    props.onClickArrData(arrData);
                }}
            >
                <input
                    type="radio"
                    checked={props.checked}
                    value={props.value}
                    onChange={props.onChange}
                />
                <p className="radio-name">{props.label}</p>
            </label>
        </>
    );
};

export default RadioButton;