import { useState } from 'react';
// import { useForm } from "react-hook-form";
import axios from "axios";
// import { yupResolver } from '@hookform/resolvers/yup';
// import * as Yup from 'yup';
import './styles/App.scss';

import Button from './components/button/Button';
import InputLabel from './components/inputLabel/InputLabel';
import MapYa from './components/mapYa/MapYa';
import RadioButton from './components/radioButton/RadioButton';

const arrEI: Array<string> = ['дтп', 'жкх', 'взрывы', 'природа', 'токсины', 'другое']

const App = (): JSX.Element => {

    const [alarm, setAlarm] = useState<number>(-1);
    const [input, setInput] = useState<string>('');
    const [radioButton, setRadioButton] = useState<string>('');
    const [arrData, setArrData] = useState<Array<string>>(['неизвестно']);

    const [show, setShow] = useState<boolean>(false);
    const [isError, setIsError] = useState<boolean>(false);
    const [message, setMessage] = useState<boolean>(false);

    const [dtpData, setDtpData] = useState({});
    const [toxicData, setToxicData] = useState({});
    const [gkhData, setGkhData] = useState({});
    const [explosionsData, setExplosionsData] = useState({});
    const [naturalData, setNaturalData] = useState({});
    const [anotherData, setAnotherData] = useState({});

    const handleChangeRadio: React.ChangeEventHandler<HTMLInputElement> = (event) => {
        setRadioButton(event.target.value);
    };

    const onClickAlarm: any = (rating: number) => {
        setAlarm(rating);
    }

    const onClickArrData: any = (arrData: Array<string>) => {
        setArrData(arrData);
    }

    async function fetchData(input: string) {
        setMessage(true);
        try {
            const res = await axios.get(`http://172.19.0.2:8000/pizdec?date=${input}`);
            console.log(res.data.event);
            setDtpData(res.data.event.dtp);
            setToxicData(res.data.event.toxic);
            setGkhData(res.data.event.GKH)
            setExplosionsData(res.data.event.explosions);
            setNaturalData(res.data.event.natural);
            setAnotherData(res.data.event.another);
            setIsError(false);
            setShow(true);
            setMessage(false);
            // console.log(res.data);
        } catch (err) {
            console.log(err);
            setIsError(true);
            setShow(false);
        }
    }

    const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();
        if (input) {
            console.log('Запрос');
            fetchData(input);
        }
    }

    const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        setInput(e.target.value);
    };

    return (
        <>
            <section className='main-part'>
                <div className='main-left'>
                    <h2 className='tittle-web grad'>S a f e P e r m</h2>

                    <form name='form' className='form' onSubmit={handleSubmit} style={{ margin: '10px' }}>
                        <InputLabel
                            value={input}
                            onChange={handleChange}
                            className='search'
                            placeholder='Дата (ГГГГ-ММ-ДД)'
                            style={{ margin: '20px' }}
                        >
                            Дата
                        </InputLabel>
                        <Button className='btn' style={{ margin: '20px' }}>Предсказать</Button>
                    </form>

                    {isError && <p className='error'>Ошибка! Введите дату ГГГГ-ММ-ДД</p>}
                    {message && <p className='message'>Загрузка...</p>}

                    {show &&
                        <>
                            <div className='radio-buttons-list'>
                                <RadioButton
                                    className='1'
                                    label="ДТП"
                                    checked={radioButton === arrEI[0]}
                                    value={arrEI[0]}
                                    obj={dtpData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                                <RadioButton
                                    className='2'
                                    label="ЖКХ"
                                    checked={radioButton === arrEI[1]}
                                    value={arrEI[1]}
                                    obj={gkhData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                                <RadioButton
                                    className='3'
                                    label="Взрывы"
                                    checked={radioButton === arrEI[2]}
                                    value={arrEI[2]}
                                    obj={explosionsData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                                <RadioButton
                                    className='4'
                                    label="Природа"
                                    checked={radioButton === arrEI[3]}
                                    value={arrEI[3]}
                                    obj={naturalData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                                <RadioButton
                                    className='5'
                                    label="Токсины"
                                    checked={radioButton === arrEI[4]}
                                    value={arrEI[4]}
                                    obj={toxicData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                                <RadioButton
                                    className='6'
                                    label="Другое"
                                    checked={radioButton === arrEI[5]}
                                    value={arrEI[5]}
                                    obj={anotherData}
                                    onChange={handleChangeRadio}
                                    onClickAlarm={onClickAlarm}
                                    onClickArrData={onClickArrData}
                                />
                            </div>

                            <div className='res-days'>
                                {arrData.slice(0, arrData.length - 1).map((elem, index) => {
                                    let i = index + 1;
                                    return <p className='day' key={index}>День {i}: {elem}</p>
                                })}
                                <p className='res'>Итоговая оценка безопасности: {arrData.slice(-1)}</p>
                            </div>
                        </>
                    }
                </div>

                <div className='main-right'>
                    <MapYa warning={alarm} />
                </div>
            </section>
        </>
    )
}

export default App
