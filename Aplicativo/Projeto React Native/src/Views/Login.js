import * as React from 'react';
import { StyleSheet, Image, View } from 'react-native';
import { TextInput, Button, DefaultTheme, Provider as PaperProvider, Text, Dialog, Portal, Paragraph} from 'react-native-paper';
import logo from '../assets/Logo.png'
import warning from '../assets/warning.png'

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
  },
};

export default class Login extends React.Component {
  state = {
    text: '',
    password: '',
    dialogVisible: false
  };

  Login = () => {
    if (this.state.text == "user" && this.state.password == "senha") {
      this.props.navigation.navigate('Inicio')
    } else {
      this.setState({dialogVisible: true})
    }
  }

  render(){
    return (
      <PaperProvider theme={theme} >
        <View style={styles.container}>
          
          <Image source={logo} style={{ width: '55%', height: 100 }} resizeMode="contain"/>

          <View style={styles.form} >
            
            <TextInput
              style={{ height: 40}}
              mode='outlined'
              label='Email'
              value={this.state.text}
              onChangeText={text => this.setState({ text })}
            />    

            <View style={{ height: 10 }} />

            <TextInput
              secureTextEntry={true}
              style={{ height: 40}}
              mode='outlined'
              label='Senha'
              value={this.state.password}
              onChangeText={password => this.setState({ password })}
            />

            <Text style={styles.textlink}>Esqueci minha senha</Text>
            <Text style={styles.textlink}>Não tem cadastro? Clique aqui!</Text>

            <Button style={{ marginTop: 20 }} icon="login" mode="contained" onPress={() => this.Login()}>
              entrar
            </Button>


            <Text style={{ marginTop: 30, textAlign: 'center', fontSize: 10 }}>Smart Aquarium™ 2019</Text>
          
          </View>

          <Portal>
            <Dialog
              visible={this.state.dialogVisible}
              onDismiss={() => this.setState({ dialogVisible: false })}>
              <Dialog.Content>
                <Paragraph style={{ width: '100%', textAlign: 'center'}}>Credenciais inválidas</Paragraph>
                <View style={{ width: '100%', alignItems: 'center', justifyContent: 'center' }}>
                  <Image source={warning} style={{ marginTop: 10, width: '55%', height: 60 }} resizeMode="contain"/>
                </View>
              </Dialog.Content>
              <Dialog.Actions>
                <Button onPress={() => this.setState({ dialogVisible: false })}>Tentar Novamente</Button>
              </Dialog.Actions>
            </Dialog>
          </Portal>

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
  form:{
    marginTop: 20,
    alignSelf: 'stretch',
    paddingHorizontal: 20,
  },
  textlink:{
    marginTop: 10,
    fontSize: 12,
  }
});

