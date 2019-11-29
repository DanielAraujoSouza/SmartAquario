import * as React from 'react';
import color from 'color';
import { DefaultTheme, BottomNavigation, Text, Provider as PaperProvider } from 'react-native-paper';

import Config from '../Views/Config';
import Actions from '../Views/Actions';
import Dashboard from '../Views/Dashboard';


const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#E77902',
    activeColor: '#fff',
    inactiveColor: color('#fff')
      .alpha(0.8)
      .rgb()
      .string(),
  },
};

const ConfigRoute = () => <Config/>;

const ActionsRoute = () => <Actions/>;

const DashboardRoute = () => <Dashboard/>;



export default class Navegacao extends React.Component {
  state = {
    index: 1,
    routes: [
      { key: 'config', title: 'Configurações', icon: 'cogs', color: theme.primary },
      { key: 'actions', title: 'Ações e Rotinas', icon: 'fish', color: theme.primary },
      { key: 'dashboard', title: 'Dashboard', icon: 'chart-bell-curve', color: theme.primary },
    ],
    
  };

  _handleIndexChange = index => this.setState({ index });

  _renderScene = BottomNavigation.SceneMap({
    config: ConfigRoute,
    actions: ActionsRoute,
    dashboard: DashboardRoute,
  });


 

  render() {
    return (

          <BottomNavigation
            activeColor={theme.activeColor} 
            inactiveColor={theme.inactiveColor}
            navigationState={this.state}
            onIndexChange={this._handleIndexChange}
            renderScene={this._renderScene}
          />
      
    );
  }
}