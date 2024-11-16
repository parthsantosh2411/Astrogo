// app/chatbot.jsx

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';
import { TextInput, Button, Text, List } from 'react-native-paper';
import { FlatList } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

export default function ChatbotScreen() {
  const { dateOfBirth, timeOfBirth, placeOfBirth, kundaliData } = useLocalSearchParams();

  const parsedKundaliData = kundaliData ? JSON.parse(kundaliData) : null;

  const [messages, setMessages] = useState([
    { sender: 'bot', text: "Welcome to AstroGo! 🌠 How can I assist you with your Kundali today?"},
  ]);
  const [inputText, setInputText] = useState('');

  const sendMessage = async () => {
    const userMessage = inputText.trim();
    if (userMessage === '') return;

    setMessages([...messages, { sender: 'user', text: userMessage }]);
    setInputText('');

    try {
      const response = await fetch('http://192.168.210.8:5000/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          kundaliData: parsedKundaliData,
        }),
      });
      const data = await response.json();
      const botMessage = data.response;
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: botMessage },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const renderItem = ({ item }) => (
    <List.Item
      title={item.text}
      titleNumberOfLines={null}
      style={{
        backgroundColor: item.sender === 'user' ? '#DCF8C6' : '#ECECEC',
        alignSelf: item.sender === 'user' ? 'flex-end' : 'flex-start',
        marginVertical: 5,
        maxWidth: '80%',
      }}
    />
  );

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.select({ ios: 'padding', android: null })}
      keyboardVerticalOffset={80}
    >
      <FlatList
        data={messages}
        renderItem={renderItem}
        keyExtractor={(item, index) => index.toString()}
        contentContainerStyle={styles.messagesContainer}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type your message"
          mode="outlined"
        />
        <Button onPress={sendMessage} mode="contained" style={styles.sendButton}>
          Send
        </Button>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  messagesContainer: {
    padding: 10,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    alignItems: 'center',
  },
  input: {
    flex: 1,
    marginRight: 10,
  },
  sendButton: {
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#6A1B9A', // Purple color for the button
    borderRadius: 8, // Slightly rounded corners
    marginTop: 10, // Margin from the top for spacing
    paddingHorizontal: 15,
  },
  sendButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

