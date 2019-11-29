import * as React from 'react';
import { StyleSheet, Image, View, ScrollView, AsyncStorage } from 'react-native';
import { Avatar, Title, Paragraph, Button, DefaultTheme, FAB, Provider as PaperProvider, Text, Card, TextInput } from 'react-native-paper';
import HeaderInicio from '../Components/HeaderInicio';
import Icon from 'react-native-vector-icons/MaterialIcons'
import notAquariums from '../assets/notAquariums.png'
import { TouchableOpacity, FlatList } from 'react-native-gesture-handler';
import { black } from 'ansi-colors';
import init from 'react_native_mqtt';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
    plusIcon: '#fff',
    text: '#000'
  },
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const host = '44.227.11.98';
const port = 9001;
user = 'Lula';

init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  sync: {},
});

export default class Inicio extends React.Component {
  state = {
    addCard: false,
    conexao: false,
    aquario: '',
    loading: false,
    conected: false,
    cards: []
  }

  async componentDidMount() {
    getAllKeys = async () => {
      let keys = []
      try {
        keys = await AsyncStorage.getAllKeys()
        console.log(keys)
        return keys
      } catch(e) {
        console.log(e)
      }
    }
    try {
      keys = await getAllKeys()
      if(keys.length <= 0) {
        console.log("Dados vazios")
        return
      }

      keysAquarios = keys.filter((key) => {
        return(key.startsWith('SmartAquario')
      )})
      if(keysAquarios.length !== 0) {
        console.log("Tem aquario")
        await keysAquarios.forEach(async key => { 
            try {
              console.log("Chave:")
              console.log(key)
              const value = await AsyncStorage.getItem(key)
              const aquario = {
                id: key,
                nome: value
              }
              
              this.setState({
                cards:[...this.state.cards, aquario]
              })
              console.log(this.state.cards)
            } catch(e) {
              console.log(e)
            }
        })
    }
    } catch (e) {
      console.log(e)
    }
  }

  componentDidUpdate() {

  }

  handleAddCard = () => {
    this.setState({ addCard: true })
  }

  closeAddCard = () => {
    this.setState({ 
      addCard: false,
      aquarioid: '',
      aquarioname: ''
    })
  }

  deleteCard = async (item) => {
    try {
      await AsyncStorage.removeItem(item)
      await AsyncStorage.removeItem('AQUARIO_PASSADO')
      this.setState({
        cards: this.state.cards.filter((_,i) => i !== index)
      })
      this.forceUpdate();
    } catch(e) {
      console.log(e)
    }
  }

  openCard = async (item) => {
    try {
      await AsyncStorage.setItem("AQUARIO_PASSADO", item)
      this.props.navigation.navigate('Apres')
    } catch (e) {

    }
  }

  handleConnect = async (aquario) => {
    const client = new Paho.MQTT.Client(host, port, user);

    // callback da msg
    onMessageArrived = async (entry) => {
      console.log("Chegou uma mensagem  ")
      console.log(entry.payloadString);
      const res = JSON.parse(entry.payloadString)
      if (res.SAID.length !== 0 && res.MSG.length !== 0 && res.SAID === res.MSG && res.MSG !== 'erro') {
        await AsyncStorage.setItem(res.SAID, res.MSG)
        if (this.state.aquarioid.length != 0 && this.state.aquarioname.length != 0){
          await AsyncStorage.setItem(this.state.aquarioid, this.state.aquarioname)
          this.setState({
            aquarioid: '',
            aquarioname: ''
          })
          this.forceUpdate();
        }
      } else
        console.log("Não foi possivel ter comunicação")
    }

    // callback de erro de conexão
    onConnectionLost = (err) => {
      console.log('Connection lost')
      console.log(err)
    }

    // callback de conexao
    onConnect = async() => {
      console.log("Connectado")
      client.subscribe(user + "/conectar/resposta")
      this.setState({conected: true})
      sendMessage(JSON.stringify({APPID: user, MSG: user}))
    }

    // publisher
    sendMessage = (message) => {
      message = new Paho.MQTT.Message(message)
      message.destinationName = aquario + "/conectar"
      client.send(message)
    }

    // instancia da conexao
    while(this.state.conected === false) {
      client.onMessageArrived = onMessageArrived
      client.onConnectionLost = onConnectionLost
      client.connect({
        onSuccess: onConnect,
        useSSL: false,
        cleanSession: false,
        userName: '',
        password: '',
        onFailure: (e) => (console.log("Erro ", e))
      })
      this.setState({loading: true})
      await sleep(1000)
      this.setState({loading: false})
      break
    }

    if (this.state.conected === true) {
      this.setState({
        addCard: false,
        conexao: false,
        aquario: '',
        loading: false,
        conected: false
      })
      // this.props.navigation.navigate('Apres')
    } else {
      console.log('erro de conexao')
      this.setState({
        addCard: false,
        conexao: false,
        aquarioid: '',
        aquarioname: '',
        loading: false,
        conected: false
      })
    }
    
  }

  render(){
    return (
        <View style={styles.container}>
          
            <PaperProvider theme={theme} >
            
                
                <View style={{justifyContent: 'flex-start', height: '100%'}}>
                <HeaderInicio></HeaderInicio>
                  <ScrollView>
                      { this.state.cards.length === 0
                        ? 
                        <View style={ styles.viewNotAquariums}>
                          <Image source={notAquariums} style={{ width: '55%', height: 60 }} resizeMode="contain"/>
                          <Text style={ styles.textNotAquariums}>Sem aquarios cadastrados</Text>
                        </View>
                        : (
                          <FlatList
                            keyboardShouldPersistTaps="handled"
                            data={this.state.cards}
                            keyExtractor={item => String(item.id)}
                            renderItem={({ item }) => (
                              <Card style={{ marginTop: 120 }} data={item}>
                                <Card.Title title={item.nome}/>
                                
                                <Card.Cover source={{ uri: 'https://i1.wp.com/www.antenacritica.com.br/wp-content/uploads/2019/09/aquario-1.jpg?resize=600%2C400&ssl=1' }} />
                                <Card.Actions>
                                    <Button icon="delete" onPress={() => this.deleteCard(item.id)}></Button>
                                    <Button icon="tablet" onPress={() => this.openCard(item.id)}></Button>
                                </Card.Actions>
                            </Card>          
                            )}
                          >
                            
                          </FlatList>
                        )
                      }    
                    {/* <Card style={{ marginTop: 120 }}>
                        <Card.Title title="Aquário 01"/>
                        
                        <Card.Cover source={{ uri: 'https://i1.wp.com/www.antenacritica.com.br/wp-content/uploads/2019/09/aquario-1.jpg?resize=600%2C400&ssl=1' }} />
                        <Card.Actions>
                            <Button icon="camera"></Button>
                            <Button icon="thermometer"></Button>
                            <Button icon="cogs"></Button>
                            <Button icon="delete"></Button>
                        </Card.Actions>
                    </Card> */}
                  </ScrollView>
                </View>
                
{/* 
              <FAB
                  styles={styles.fab}
                  small
                  icon="plus"
                  onPress={() => this.handleAddCard()}
              ></FAB> */}
            
          
            {/* botão para adicionar um card */}
                <View style={styles.addButton}>
                        <TouchableOpacity onPress={() => this.handleAddCard()}>
                            <Icon name="add" mode="contained" size={30} color={ theme.colors.plusIcon }/>
                        </TouchableOpacity>
                </View>
                
            {/* Alert pra conectar com um aquario */}
            { this.state.addCard &&  
            <View style={styles.addCardContainer}>
              <View style={styles.addCardView}>
                <View style={styles.addCardHeader}>
                  <Text style={styles.addCardLabel}>Digite o código do aquario</Text>
                </View>
                
                
                <TextInput 
                  style={styles.addCardInput}
                  mode='outlined'
                  value={this.state.aquarioid}
                  onChangeText={text => this.setState({ aquarioid: text })}
                />
              

                <View style={styles.addCardHeader}>
                  <Text style={styles.addCardLabel}>Digite o nome do aquario</Text>
                </View>

                
                <TextInput 
                  style={styles.addCardInput}
                  mode='outlined'
                  value={this.state.aquarioname}
                  onChangeText={text => this.setState({ aquarioname: text })}
                />
                

                <View style={styles.btnView}>
                  <TouchableOpacity onPress={() => this.handleConnect(this.state.aquarioid)} style={styles.btnAddCard}>
                    <Text style={{ paddingVertical: 5, paddingHorizontal: 10, color: '#fff'}} >Conectar</Text>
                  </TouchableOpacity>
                  <TouchableOpacity onPress={() => this.closeAddCard()} style={styles.btnCancelCard}>
                    <Text style={{ paddingVertical: 5, paddingHorizontal: 10, color: '#fff'}} >Cancelar</Text>
                  </TouchableOpacity>
                </View>
                
              </View>
            </View>
            }
            </PaperProvider>
        </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex:1,
    alignSelf: 'stretch',
    justifyContent: 'flex-start',
  },
  fab:{
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    width: 40,
    height: 40
  },
  addButton: {
    position: 'absolute',
    top: '90%',
    left: '80%',
    zIndex: 2,
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: "center",
    backgroundColor: '#019DDE',
    borderRadius: 25
  },
  addCardContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'center',
    alignItems: 'center'
  },
  addCardView: {
    flexDirection: 'column',
    width: '60%',
    backgroundColor: '#fff',
    alignSelf: 'auto',
    margin: 5,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 10,
    padding: 5,
    borderRadius: 5
  },
  addCardHeader: {
    justifyContent: 'flex-start',
    alignItems: 'center',
    alignSelf: 'flex-start'
  },
  addCardLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#019DDE'
  },
  addCardInput: {
    backgroundColor: '#fff',
    height: 30,
    padding: 10,
    alignSelf: 'stretch',
    borderColor: '#333',
    marginBottom: 5
  },
  btnView: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    alignContent: 'space-around'
  },
  btnAddCard: {
    backgroundColor: '#30a930',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 5,
    borderRadius: 5,
    marginRight: 5
  },
  btnCancelCard: {
    backgroundColor: '#ad3035',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 5,
    borderRadius: 5,
    marginLeft: 5
  },
  textNotAquariums:{
    justifyContent:'center',
    fontSize: 20,
    marginTop: 20,
    fontWeight: 'bold',
    color: '#019dde',
  },
  viewNotAquariums:{
    alignItems: 'center',
    justifyContent:'center',
  }
});

