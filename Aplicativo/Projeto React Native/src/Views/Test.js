import * as React from 'react';
import { StyleSheet, View } from 'react-native';
import { DefaultTheme, Provider as PaperProvider} from 'react-native-paper';


import Header from '../Components/Header';

import Navegacao from '../Components/Navegacao';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
  },
};


export default class Inicio extends React.Component {

  render(){
    return (
      <View style={styles.container}>
        <PaperProvider theme={theme} >
            <Header></Header>
        </PaperProvider>
        <Navegacao></Navegacao>  
      </View>  
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
});

