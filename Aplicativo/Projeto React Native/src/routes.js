import { createAppContainer, createSwitchNavigator } from 'react-navigation';

import Login from './Views/Login'
import Inicio from './Views/Inicio'
import Apres from './Views/Apres'

const Routes = createAppContainer(
    createSwitchNavigator({
        Apres,
        Login,
        Inicio,
    })
);

export default Routes;
