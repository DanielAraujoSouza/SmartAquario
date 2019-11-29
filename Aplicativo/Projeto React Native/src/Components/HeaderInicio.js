import * as React from 'react';
import { useState, useEffect } from 'react';
import { View, } from 'react-native';
import { withNavigation} from 'react-navigation';
import { Appbar, DefaultTheme, Provider as PaperProvider, Text } from 'react-native-paper';
import { TouchableOpacity } from 'react-native-gesture-handler';

const theme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      primary: '#019DDE',
      accent: 'red',
    },
  };

function HeaderInicio ({ navigation }){

  const [showDrop, setShowDrop] = useState(false); 


  showDropdown = () => {
    if(showDrop){
      setShowDrop(false)
    }else{
      setShowDrop(true)
    }
  }

  
  return (
    <PaperProvider theme={theme} >
      <Appbar.Header>
        <Appbar.Content
         title='Início'
        />
        <Appbar.Action icon="dots-vertical" onPress={() => showDropdown()} />
        
        { showDrop &&
        <View style={{ width:'35%', height: 40, backgroundColor: 'white', position: 'absolute', right: 0, top: 55, borderRadius: 10, shadowColor: "#000", shadowOffset: { width: 0, height: 7, }, shadowOpacity: 0.43, shadowRadius: 9.51, elevation: 15, }}>
          <TouchableOpacity onPress={() => navigation.navigate('Login')}>
            <Text style={{fontSize: 24, marginTop: 5, textAlign: 'center', width: '100%', height: '100%' }}>sair</Text>
          </TouchableOpacity>
        </View>
        
        }
        
      </Appbar.Header>
    </PaperProvider>
  );
};


export default withNavigation(HeaderInicio);