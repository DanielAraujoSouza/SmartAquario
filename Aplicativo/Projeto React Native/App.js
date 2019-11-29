import React from 'react';
import Routes from './src/routes';
import { YellowBox } from 'react-native'


YellowBox.ignoreWarnings(['Acessing view manager'])
console.disableYellowBox = true
export default function App() {
  return (
    <Routes></Routes>
  );
}