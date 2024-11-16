import React, { useState, useEffect } from 'react';
import { ScrollView, StyleSheet } from 'react-native';
import { Text, Button, Title, Card } from 'react-native-paper';
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function PlanetsScreen() {
  const { dateOfBirth, timeOfBirth, placeOfBirth } = useLocalSearchParams();
  const [planetary_info, setPlanetaryInfo] = useState(null);
  const router = useRouter();

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
      const data = await response.json();
      console.log(data);
      setPlanetaryInfo(data.planets_info); // Extract planets_info
    } catch (error) {
      console.error('Error fetching Kundali data:', error);
    }
  };

  if (!planetary_info) {
    return (
      <ScrollView contentContainerStyle={styles.loadingContainer}>
        <Text>Loading Planetary Info...</Text>
      </ScrollView>
    );
  }
  const handleCalculateKundali = () => {
    router.push({
      pathname: '/DashaScreen',
      params: {
        dateOfBirth,
        timeOfBirth,
        placeOfBirth,
      },
    });
  };


  return (
    <ScrollView style={styles.container}>
      <Title>Planets in Houses</Title>
      {Object.entries(planetary_info).map(([planet, info]) => (
        <Card key={planet} style={styles.card}>
          <Card.Title title={planet} />
          <Card.Content>
            <Text>House: {info.House}</Text>
            <Text>House Ruler: {info['House Ruler']}</Text>
            <Text>Strength: {info.Strength}</Text>
            <Text>Nature: {info.Nature}</Text>
            <Text>Sign: {info.Sign}</Text>
          </Card.Content>
        </Card>
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
    paddingHorizontal: 20,
    paddingVertical: 30,
    backgroundColor: '#F3F4F6', // Light gray background for a clean, neutral look
  },
  card: {
    padding: 20,
    marginBottom: 15,
    backgroundColor: '#FFFFFF', // White background for contrast
    borderRadius: 12, // Smooth rounded corners for a modern look
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 4, // Soft shadow for lifted effect
    borderWidth: 1,
    borderColor: '#E0E0E0', // Subtle border for definition
  },
  button: {
    marginTop: 20,
    marginBottom: 40, // Additional space from the bottom edge of the screen
    paddingVertical: 15,
    paddingHorizontal: 28,
    backgroundColor: '#6A1B9A', // Deep purple color for a vibrant, astrological theme
    borderRadius: 12, // Smooth rounded corners for an appealing look
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#6A1B9A',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 7, // Elevated effect for standout button appearance
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '700', // Bolder weight for emphasis
    letterSpacing: 1.2, // Slightly larger letter spacing for an elegant look
  },
  loadingContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 40, // Ensures extra padding at the bottom for spacing
  },
});

