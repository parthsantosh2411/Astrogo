// import "../global.css";
// import { Slot } from "expo-router";

// export default function Layout() {
//   return <Slot />;
// }
// app/_layout.jsx

import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
      }}
      >
      <Stack.Screen  name='KundaliScreen'  options={{headerShown:false}} />
      <Stack.Screen  name='PlanetsScreen'  options={{headerShown:false}} />
      <Stack.Screen  name='DashaScreen'  options={{headerShown:false}} />
      <Stack.Screen  name='ChatbotScreen'  options={{headerShown:false}} />

      </Stack>
  );
}
