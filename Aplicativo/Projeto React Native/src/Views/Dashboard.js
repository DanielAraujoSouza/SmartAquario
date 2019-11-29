import * as React from 'react';
import { StyleSheet, View, Dimensions } from 'react-native';
import { DefaultTheme, Provider as PaperProvider, Text} from 'react-native-paper';
import { LineChart, BarChart, PieChart, ProgressChart, ContributionGraph, StackedBarChart } from "react-native-chart-kit";

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#019DDE',
  },
};

export default class Dashboard extends React.Component {

  render(){
    return (
      <PaperProvider theme={theme} >
        <View style={styles.container}>
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
            width={(Dimensions.get("window").width - 40 )} 
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

