import { YMaps, Map, Polygon, ZoomControl } from '@pbe/react-yandex-maps';
import coordinatesOfPerm from './../../coordinatesOfPerm';
import './style.scss';

type MapYaProps = {
    warning: number
};

const MapYa = (props: MapYaProps): JSX.Element => {

    const fillColorFn = (warning: number): string => {
        switch (warning) {
            case 0:
                return "#00FF00";
                break;

            case 1:
                return "#c9d700";
                break;

            case 2:
                return "#d72700";
                break;

            default:
                return "#0000001d";
                break;
        }
    }

    const strokeColorFn = (warning: number): string => {
        switch (warning) {
            case 0:
                return "#199700";
                break;

            case 1:
                return "#a7b300";
                break;

            case 2:
                return "#7a1600";
                break;

            default:
                return "#1e1e1e";
                break;
        }
    }

    return (
        <div className="mapYa">
            <YMaps>
                <Map
                    className='map'
                    defaultState={{
                        center: [59, 56.068261],
                        zoom: 7,
                        controls: []
                    }}
                    options={{
                        maxZoom: 8,
                        minZoom: 7
                    }}
                >
                    <ZoomControl />
                    <Polygon
                        geometry={[coordinatesOfPerm]}
                        options={{
                            fillColor: fillColorFn(props.warning),
                            strokeColor: strokeColorFn(props.warning),
                            opacity: 0.5,
                            strokeWidth: 3,
                        }}
                    />
                </Map>
            </YMaps>
        </div>
    );
};

export default MapYa;