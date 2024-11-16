// App.js
import 'react-native-gesture-handler';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import HomeScreen from './index'
import KundaliScreen from './KundaliScreen';
import PlanetsScreen from './PlanetsScreen';
import DashaScreen from './DashaScreen';
import ChatbotScreen from './ChatbotScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Kundali" component={KundaliScreen} />
        <Stack.Screen name="Planets" component={PlanetsScreen} />
        <Stack.Screen name="Dasha" component={DashaScreen} />
        <Stack.Screen name="Chatbot" component={ChatbotScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
