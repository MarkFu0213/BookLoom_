import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MainPage from '../../components/MainPage';
import AuthScreen from '@/components/auth/AuthScreen';
import ProfileScreen from '@/components/profile/ProfileScreen';
import { RootStackParamList } from '../../types/navigation';

const Stack = createNativeStackNavigator<RootStackParamList>();

export const options = {
  headerShown: false,
};

export default function HomeScreen() {
  return (
    <Stack.Navigator screenOptions={options} initialRouteName="Auth">
      <Stack.Screen name="Main" component={MainPage} />
      <Stack.Screen name="Auth" component={AuthScreen} /> 
      <Stack.Screen name="Profile" component={ProfileScreen} />
    </Stack.Navigator>
  );
}