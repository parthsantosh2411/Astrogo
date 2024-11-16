// app/dasha.jsx

import React, { useState, useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button, Title, Paragraph } from 'react-native-paper';
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function DashaScreen() {
  const { dateOfBirth, timeOfBirth, placeOfBirth } = useLocalSearchParams();
  const router = useRouter();

  // Declare state variables
  const [data, setData] = useState(null);
  const [currentDasha, setCurrentDasha] = useState(null);
  const [currentAntardasha, setCurrentAntardasha] = useState(null);

  useEffect(() => {
    fetchKundaliData();
  }, []);

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
      const result = await response.json();
      console.log('API Response:', result);

      setData(result);
      setCurrentDasha(result.current_dasha);
      setCurrentAntardasha(result.current_antardasha);
    } catch (error) {
      console.error('Error fetching Kundali data:', error);
    }
  };

  if (!data) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading Dasha Data...</Text>
      </View>
    );
  }

  const handleGetPredictions = () => {
    router.push({
      pathname: '/ChatbotScreen',
      params: {
        dateOfBirth,
        timeOfBirth,
        placeOfBirth,
        kundaliData: JSON.stringify(data),
      },
    });
  };

  return (
    <View style={styles.container}>
      <Title>Current Mahadasha</Title>
      {currentDasha == null ? (
        <Paragraph>No Mahadasha Data Available</Paragraph>
      ) : typeof currentDasha === 'string' ? (
        <Paragraph>{currentDasha}</Paragraph>
      ) : (
        <>
          <Paragraph>Planet: {currentDasha.Planet}</Paragraph>
          <Paragraph>Start Date: {currentDasha['Start Date']}</Paragraph>
          <Paragraph>End Date: {currentDasha['End Date']}</Paragraph>
        </>
      )}

      <Title style={styles.sectionTitle}>Current Antardasha</Title>
      {currentAntardasha == null ? (
        <Paragraph>No Antardasha Data Available</Paragraph>
      ) : typeof currentAntardasha === 'string' ? (
        <Paragraph>{currentAntardasha}</Paragraph>
      ) : (
        <>
          <Paragraph>Planet: {currentAntardasha.Planet}</Paragraph>
          <Paragraph>Start Date: {currentAntardasha['Start Date']}</Paragraph>
          <Paragraph>End Date: {currentAntardasha['End Date']}</Paragraph>
        </>
      )}

      <Button
        mode="contained"
        onPress={handleGetPredictions}
        style={styles.button}
      >
        Get Predictions
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingVertical: 30,
    backgroundColor: '#F3F4F6', // Light gray background for a clean look
  },
  sectionTitle: {
    marginTop: 20,
    fontSize: 24,
    fontWeight: '700',
    color: '#4A4A4A', // Darker shade for section titles
    textAlign: 'left',
  },
  mahadashaText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4A4A4A', // Dark color for bold emphasis on Mahadasha
  },
  antardashaText: {
    fontSize: 18,
    fontWeight: '300', // Light font weight for Antardasha
    color: '#6A1B9A', // Purple to maintain theme consistency
  },
  button: {
    marginTop: 20,
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12, // Rounded corners for a polished look
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#6A1B9A', // Purple color for the button
    shadowColor: '#6A1B9A',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 6, // Elevated effect for standout appearance
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 0.8, // Slight letter spacing for readability
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 5, // Elevated look for visual depth
    margin: 20,
  },
});

