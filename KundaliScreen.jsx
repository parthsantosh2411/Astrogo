// screens/KundaliScreen.js
import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet } from 'react-native';
import { Text, Button, Title, Paragraph } from 'react-native-paper';
import { router, useLocalSearchParams ,useRouter } from 'expo-router';

export default function KundaliScreen() {
  const [kundaliData, setKundaliData] = useState('');
  const { dateOfBirth, timeOfBirth, placeOfBirth } = useLocalSearchParams();
  useEffect(() => {
    fetchKundaliData();
  }, []);

  // const fetchKundaliData = async () => {
  //   try {
  //       const response = await fetch('http://127.0.0.1:5000/kundali', {
  //           method: 'POST',
  //           headers: { 'Content-Type': 'application/json' },
  //           body: JSON.stringify({
  //             "date_of_birth": dateOfBirth,
  //             "time_of_birth": timeOfBirth,
  //             "place_of_birth": placeOfBirth,
  //           }),
  //         });
  //     const data = await response.json();
  //     console.log(data);
      
  //     setKundaliData(data);
  //   } catch (error) {
  //     console.error(error);
  //   }
  // };
  const fetchKundaliData = async () => {
    try {
      const response = await fetch('http://192.168.210.8:5000/kundali', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date_of_birth: dateOfBirth,
          time_of_birth: timeOfBirth,
          place_of_birth: placeOfBirth,
        }),
      });
      const data = await response.json();
      console.log(data);
      setKundaliData(data);
      console.log(kundaliData);
      
    } catch (error) {
      console.error('Error fetching Kundali data:', error);
    }
  };
  const handleCalculateKundali = () => {
    router.push({
      pathname: '/PlanetsScreen',
      params: {
        dateOfBirth,timeOfBirth,placeOfBirth
      },
    });
  };

  if (!kundaliData) {
    return (
      <ScrollView contentContainerStyle={styles.loadingContainer}>
        <Text>Loading Kundali Data...</Text>
      </ScrollView>
    );
  }

  const { ascendant_info, planetary_info } = kundaliData;

  return (
    <ScrollView style={styles.container}>
      

      <Title style={styles.sectionTitle}>Planetary Positions</Title>
      {Object.entries(planetary_info).map(([planet, info]) => (
        <Paragraph key={planet}>
          <Text style={{ fontWeight: 'bold' }}>{planet}:</Text> {info.Position} in {info.Sign}
        </Paragraph>
      ))}

      <Button
        mode="contained"
        onPress={handleCalculateKundali}
        style={styles.button}
      >
        Next
      </Button>
    </ScrollView>
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

