// // screens/HomeScreen.js
// import React, { useState } from 'react';
// import { View, StyleSheet } from 'react-native';
// import { TextInput, Button, Title } from 'react-native-paper';

// export default function HomeScreen({ navigation }) {
//   const [dateOfBirth, setDateOfBirth] = useState('');
//   const [timeOfBirth, setTimeOfBirth] = useState('');
//   const [placeOfBirth, setPlaceOfBirth] = useState('');

//   const handleCalculateKundali = () => {
//     navigation.navigate('Kundali', {
//       dateOfBirth,
//       timeOfBirth,
//       placeOfBirth,
//     });
//   };

//   return (
//     <View style={styles.container}>
//       <Title style={styles.title}>Enter Your Birth Details</Title>
//       <TextInput
//         label="Date of Birth (YYYY-MM-DD)"
//         value={dateOfBirth}
//         onChangeText={setDateOfBirth}
//         mode="outlined"
//         style={styles.input}
//       />
//       <TextInput
//         label="Time of Birth (HH:MM)"
//         value={timeOfBirth}
//         onChangeText={setTimeOfBirth}
//         mode="outlined"
//         style={styles.input}
//       />
//       <TextInput
//         label="Place of Birth"
//         value={placeOfBirth}
//         onChangeText={setPlaceOfBirth}
//         mode="outlined"
//         style={styles.input}
//       />
//       <Button mode="contained" onPress={handleCalculateKundali} style={styles.button}>
//         Calculate Kundali
//       </Button>
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     padding: 20,
//     backgroundColor: '#fff',
//   },
//   title: {
//     marginVertical: 20,
//     textAlign: 'center',
//   },
//   input: {
//     marginBottom: 15,
//   },
//   button: {
//     marginTop: 20,
//   },
// });
// app/index.js
import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { TextInput, Button, Title } from 'react-native-paper';
import { useRouter } from 'expo-router';


export default function HomeScreen() {
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [timeOfBirth, setTimeOfBirth] = useState('');
  const [placeOfBirth, setPlaceOfBirth] = useState('');

  const router = useRouter();

  const handleCalculateKundali = () => {
    router.push({
      pathname: '/KundaliScreen',
      params: {
        dateOfBirth,
        timeOfBirth,
        placeOfBirth,
      },
    });
  };

  return (
    <View style={styles.container}>
      <Title style={styles.title}>Enter Your Birth Details</Title>
      <TextInput
        label="Date of Birth (YYYY-MM-DD)"
        value={dateOfBirth}
        onChangeText={setDateOfBirth}
        mode="outlined"
        style={styles.input}
      />
      <TextInput
        label="Time of Birth (HH:MM)(24H)"
        value={timeOfBirth}
        onChangeText={setTimeOfBirth}
        mode="outlined"
        style={styles.input}
      />
      <TextInput
        label="Place of Birth"
        value={placeOfBirth}
        onChangeText={setPlaceOfBirth}
        mode="outlined"
        style={styles.input}
      />
      <Button mode="contained" onPress={handleCalculateKundali} style={styles.button}>
        Calculate Kundali
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#F3F4F6', // Light gray background for a clean, neutral look
  },
  title: {
    marginVertical: 20,
    textAlign: 'center',
    fontSize: 28,
    fontWeight: 'bold',
    color: '#4A4A4A', // Darker shade for the title
  },
  input: {
    marginBottom: 15,
    padding: 15,
    borderRadius: 12, // Rounded corners for a softer appearance
    backgroundColor: '#FFFFFF', // White background for contrast
    shadowColor: '#000', // Light shadow for depth
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4, // Android shadow
    borderWidth: 1,
    borderColor: '#E0E0E0', // Border for subtle definition
  },
  button: {
    marginTop: 30,
    paddingVertical: 14,
    paddingHorizontal: 20,
    borderRadius: 10, // Rounded button with a medium radius
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#6A1B9A', // Bold gradient color for vibrance
    shadowColor: '#6A1B9A',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 6, // Higher elevation for standout effect
  },
  buttonGradient: {
    borderRadius: 10, // Match button radius for gradient styling
    paddingVertical: 14,
    paddingHorizontal: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#FFFFFF', // White text color for contrast
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 0.8, // Slight letter spacing for a polished look
  },
  subtitle: {
    fontSize: 16,
    color: '#7D7D7D', // Subtle color for less emphasis
    textAlign: 'center',
    marginBottom: 10,
  },
  card: {
    padding: 20,
    borderRadius: 16,
    backgroundColor: '#FFF',
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
});

