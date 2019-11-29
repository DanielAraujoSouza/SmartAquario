import * as React from 'react';
import { StyleSheet, View, Dimensions, Image, AsyncStorage } from 'react-native';
import { DefaultTheme, Button, Provider as PaperProvider} from 'react-native-paper';

import { LineChart, BarChart, PieChart, ProgressChart, ContributionGraph, StackedBarChart } from "react-native-chart-kit";



import logo from '../assets/Logo.png'
import Header from '../Components/Header';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
  },
};

const host = '44.227.11.98';
const port = 1883;
const user = 'app';


init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  sync: {},
});


var mqtt = require('mqtt')
var client  = mqtt.connect(host)
 



export default function Apres2() {

    

    const test = () => {
      console.log('teste');
      client.on('connect', function () {
        client.subscribe('start/app', function (err) {
          if (!err) {
            client.publish('start/app', 'Hello mqtt')
          }
        })
      })
       
      client.on('message', function (topic, message) {
        console.log(message.toString())
        client.end()
      })
    }

    return (
      <View style={styles.container}>
        
        { test() }

        <Image source={logo} style={{ marginBottom: 40, width: '55%', height: 100 }} resizeMode="contain"/>

        <Button style={{ width: '100%', marginBottom: 40, backgroundColor: '#019DDE' }} icon="lightbulb" mode="contained" >

        </Button>

        <LineChart
            data={{
              labels: ["", "01:10", "", "01:30", "", "01:50", "", "02:10", "", "02:30"],
              datasets: [
                {
                  data: [
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100,
                    Math.random() * 100
                  ]
                }
              ]
            }}
            width={(Dimensions.get("window").width)} 
            height={220}
            yAxisLabel={""}
            yAxisSuffix={"cm³"}
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
          />

      </View>  
    );
  
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    
  },
});