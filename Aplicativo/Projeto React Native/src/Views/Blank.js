import * as React from 'react';
import { StyleSheet, View } from 'react-native';
import { DefaultTheme, Provider as PaperProvider, Text} from 'react-native-paper';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
  },
};

export default class BLANK_VIEW  extends React.Component {

  render(){
    return (
      <PaperProvider theme={theme} >
        <View style={styles.container}>
          <Text>BLANK_VIEW</Text>
        </View>  
      </PaperProvider>  
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

