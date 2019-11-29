import * as React from 'react';
import { useState, useEffect } from 'react';
import { StyleSheet, View, Dimensions, Image, AsyncStorage } from 'react-native';
import { withNavigation} from 'react-navigation';
import { Modal, Portal, DefaultTheme, Button, Provider as PaperProvider, Text, Provider} from 'react-native-paper';

import { LineChart, BarChart, PieChart, ProgressChart, ContributionGraph, StackedBarChart } from "react-native-chart-kit";

import init from 'react_native_mqtt';

import Header from '../Components/Header';
import { ScrollView } from 'react-native-gesture-handler';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#ffffff',
  },
};

const host = '44.227.11.98';
//const host = 'test.mosquitto.org'
const port = 9001;
const user = 'Lula';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// instancia do cliente
const clientRecebe = new Paho.MQTT.Client(host, port, user);
const clientEnvia = new Paho.MQTT.Client(host, port, 'App2');

init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  sync: {},
});



function Apres({ navigation, navigation: { goBack } }) {

  const [temp, setTemp] = useState('-');
  const [tempMax, setTempMax] = useState(0);
  const [tempMed, setTempMed] = useState(0);
  const [nivel, setNivel] = useState(true);
  const [modalVisibility, setModalVisibility] = useState(false); 
  const [modalFeedVisibility, setModalFeedVisibility] = useState(false);  
  const [dataTemp, setDataTemp] = useState({
    datasets: [{
      data: [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    }]
  });
  const [aquario, setAquario] = useState('')
  const [bomba, setBomba] = useState(false)

  useEffect(() => {
    async function recuperaUser() {
        AsyncStorage.getItem('AQUARIO_PASSADO').then(token => {
            if(token) {
                console.log(token)
                
                setAquario(token)

                // callback da messagem
                onMessageArrived = (entry) => {
                  console.log(entry.topic);
                  console.log(entry.payloadString); 
                  if(entry.topic == (token) + '/sensores/temperatura'){
                    let pldTemp = JSON.parse(entry.payloadString);
                    setTemp(Number(pldTemp.MSG).toFixed(2));
                  }
                  if(entry.topic == (token) + '/sensores/nivel'){
                    let pldNivel = JSON.parse(entry.payloadString);
                      if(pldNivel.MSG == "1"){
                        setNivel(true);
                      }
                      if(pldNivel.MSG == "0"){
                        setNivel(false);
                      }
                  }            
                }

                // callback de desconaxão
                onConnectionLost = (err) => {
                  console.log('Desconetado com o aquario!')
                  console.log(err)
                }

                // callback de conexão
                onConnect = () => {
                  console.log("Conectado com o aquario para envio do comando subs!!!!");
                  clientRecebe.subscribe(token + '/sensores/temperatura')
                  clientRecebe.subscribe(token + '/sensores/nivel')
                };

                // definindo os callbacks
                clientRecebe.onMessageArrived = onMessageArrived
                clientRecebe.onConnect = onConnect
                clientRecebe.onConnectionLost = onConnectionLost

                // estabelecimento da conexão
                clientRecebe.connect({
                  onSuccess: onConnect,
                  onFailure: (e) => {
                    console.log("here is the error", e);
                  }
                });
                
                
            } else {
              navigation.navigate('Inicio')
            }
        })
    }

    recuperaUser()
  }, [])
  
  async function enviaMessage(topico, mensagem) {


    // callback de desconaxão
    onConnectionLost = async (err) => {
      console.log('Desconetado com o aquario!')
      console.log(err)

      await sleep(5000)
    }

    // callback de conexão
    onConnect = () => {
      console.log('Temp' + temp)
      console.log('Nivel' + nivel)
      console.log("Conectado com o aquario para envio do comando!!!!");
      clientEnvia.subscribe(aquario + topico)
      // envio da mensagem
      message = new Paho.MQTT.Message(mensagem);
      message.destinationName = aquario + topico;
      clientEnvia.send(message);
    };

    // envio da mensagem

    // definindo os callbacks
    clientEnvia.onConnect = onConnect
    clientEnvia.onConnectionLost = onConnectionLost

    // estabelecimento da conexão
    clientEnvia.connect({
      onSuccess: onConnect,
      onFailure: (e) => {
        console.log("here is the error", e);
      }
    });

    await sleep(5000)

    // desconecta
    clientEnvia.disconnect({
      onSuccess: onConnectionLost,
      onFailure: (e) => {
        console.log("here is the error", e);
      }
    })

  }

  function renderizaTemp(temp){
    let newFirstElement = temp;
    dataAux = dataTemp.datasets[0].data;
    log('data aux 1' + dataAux);
    dataAux.pop();
    log('data aux 2 pop' + dataAux);
    dataAux = [newFirstElement].concat(dataAux);
    
    setDataTemp({
      datasets: [{
        data: dataAux,
      }]
    });
    
  }


  

  function gerenciaBomba() {
    if(!bomba){
      enviaMessage("/atuadores/bomba", '{"APPID":"'+user+'", "MSG": "ligar"}')
      setBomba(true)
    } else {
      enviaMessage("/atuadores/bomba", '{"APPID":"'+user+'", "MSG": "desligar"}')
      setBomba(false)
    }
  }


    return (

      
      <View style={styles.container}>
          <View style={styles.viewRow}>
            <Header></Header>
          </View>
        <ScrollView style={{ width: '100%'}}>

          <Text style={styles.large}>Temperatura</Text>
          {/* <LineChart
            data={dataTemp}
            width={(Dimensions.get("window").width - (Dimensions.get("window").width * 0.1))} 
            height={220}
            yAxisLabel={""}
            yAxisSuffix={"°C"}
            chartConfig={{
              backgroundColor: "red",
              backgroundGradientFrom: "#019DDE",
              backgroundGradientTo: "#019DDE",
              decimalPlaces: 0, // optional, defaults to 2dp
              color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              style: {
                borderRadius: 16
              },
              propsForDots: {
                r: "6",
                strokeWidth: "2",
                stroke: "#E77902"
              }
            }}
            bezier
            style={{
              marginVertical: 8,
              borderRadius: 16
            }}
          /> */}
          <Text style={styles.medium}>{temp}°C</Text>


          <Text style={ styles.large}>Nível de Água</Text>

          { !nivel &&  
            <Text style={styles.mediumSafe}>SEGURO</Text>
          }

          { nivel &&  
            <Text style={styles.mediumDanger}>BAIXO, REPONHA A ÁGUA</Text>
          }

          <View style={{ alignItems: 'center'}}>
            <Text style={styles.large}>Atuação</Text>
            <Button theme={theme} style={ styles.button } icon="fish" onPress={() => setModalFeedVisibility(true)} >ALIMENTAÇÃO</Button>
            <Button theme={theme} style={ styles.button } icon="power-plug" onPress={() => gerenciaBomba() }>BOMBA DE ÁGUA</Button>
            <Button theme={theme} style={ styles.button } icon="lightbulb-on" onPress={() => setModalVisibility(true)}>ILUMINAÇÃO</Button>
          </View>
        </ScrollView>
        
        

        <Provider>
          <Portal>
            <Modal visible={modalVisibility} onDismiss={() => setModalVisibility(false)}>
              <View  style={ styles.modalView }>
                <Text style={ styles.largeModal }>Selecione a cor:</Text>
                <View style={ styles.viewRow }>
                  <Button style={{ backgroundColor: "red", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "100", "G": "0", "B": "0"}' )} ></Button>
                  <Button style={{ backgroundColor: "green", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "0", "G": "100", "B": "0"}' )} ></Button>
                  <Button style={{ backgroundColor: "blue", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "0", "G": "0", "B": "100"}' )} ></Button>
                </View>

                <View style={ styles.viewRow }>
                  <Button style={{ backgroundColor: "white", borderWidth:1, borderColor: 'black', marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "100", "G": "100", "B": "100"}' )} ></Button>
                  <Button style={{ backgroundColor: "#00ffff", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "0", "G": "100", "B": "100"}' )} ></Button>
                  <Button style={{ backgroundColor: "#ff00ff", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "100", "G": "0", "B": "100"}' )} ></Button>
                </View>

                <View style={ styles.viewRow }>
                  <Button style={{ backgroundColor: "#ffff00", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "100", "G": "100", "B": "0"}' )} ></Button>
                  <Button theme={ theme } style={{ backgroundColor: '#019DDE',marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "especial", "TIPO": "transicao"}' )} >🦄</Button>
                  <Button theme={ theme } style={{ backgroundColor: "black", marginLeft: 5, marginRight: 5 }} onPress={() => enviaMessage("/atuadores/iluminacao", '{"APPID":"'+user+'", "MSG": "cor", "R": "0", "G": "0", "B": "0"}' )} >OFF</Button>
                </View>

              </View>
            </Modal>
          </Portal>
        </Provider>

        <Provider>
          <Portal>
            <Modal visible={modalFeedVisibility} onDismiss={() => setModalFeedVisibility(false)}>
              <View  style={ styles.modalViewFeed }>

                <View style={ styles.viewRow }>
                    <Button theme={theme} style={ styles.buttonOnOff } onPress={() => enviaMessage("/atuadores/alimentacao", '{"APPID":"'+user+'", "MSG": "P"}' )} >POUCO</Button>
                    <Button theme={theme} style={ styles.buttonOnOff } onPress={() => enviaMessage("/atuadores/alimentacao", '{"APPID":"'+user+'", "MSG": "M"}' )} >MÉDIO</Button>
                    <Button theme={theme} style={ styles.buttonOnOff } onPress={() => enviaMessage("/atuadores/alimentacao", '{"APPID":"'+user+'", "MSG": "G"}' )} >MUITO</Button>
                </View>

              </View>
            </Modal>
          </Portal>
        </Provider>

      </View>  
    );

  
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    
  },
  modalView:{
    borderRadius: 20,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
    alignContent: 'center',
    paddingTop: 20,
    paddingBottom: 30
  },
  modalViewFeed:{
    borderRadius: 20,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
    alignContent: 'center',
    paddingTop: 20,
    height: '40%',
  },
  large:{
    marginBottom: 10,
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'left',
    width: '100%',
    paddingHorizontal: 30
  },
  largeModal:{
    marginBottom: 30,
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    width: '100%',
  },
  medium:{
    marginBottom: 10,
    fontSize: 16,
    textAlign: 'left',
    width: '100%',
    paddingHorizontal: 30
  },
  mediumDanger:{
    marginBottom: 10,
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'left',
    width: '100%',
    paddingHorizontal: 30,
    color: 'red'
  },
  mediumSafe:{
    marginBottom: 10,
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'left',
    width: '100%',
    paddingHorizontal: 30,
    color: 'green'
  },
  viewRow:{
    flexDirection: 'row',
    marginBottom:10,
  },
  button:{
    backgroundColor: '#019DDE',
    width: '55%',
    marginBottom: 20,
  },
  buttonOnOff:{
    backgroundColor: '#019DDE',
    width: '25%',
    marginLeft: 5,
    marginRight: 5,
    marginBottom: 20,
  }
});

export default withNavigation(Apres);
