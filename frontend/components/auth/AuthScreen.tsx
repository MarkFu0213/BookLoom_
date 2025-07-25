"use client"

import { useState } from "react"
import { View, Text, StyleSheet, ScrollView, KeyboardAvoidingView, Platform, SafeAreaView, Alert, Modal, TouchableOpacity } from "react-native"
import { Button, Input, ThemeProvider, createTheme } from "@rneui/themed"
import { Picker } from "@react-native-picker/picker"
import { styles } from "./styles"
import { useNavigation } from '@react-navigation/native'
import { RootStackParamList } from '@/types/navigation'
import { NativeStackNavigationProp } from '@react-navigation/native-stack'

type AuthMode = "login" | "register"

type ProfileScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Profile'>

const theme = createTheme({
  lightColors: {
    primary: "#8B4513", // SaddleBrown
    secondary: "#D2691E", // Chocolate
    background: "#FAEBD7", // AntiqueWhite
  },
})

export default function Auth() {
  const [mode, setMode] = useState<AuthMode>("login")
  const [loading, setLoading] = useState(false)
  const navigation = useNavigation<ProfileScreenNavigationProp>()

  // Login form state
  const [loginUsername, setLoginUsername] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  // Registration form state
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [age, setAge] = useState("")
  const [gender, setGender] = useState("")
  const [favoriteBook, setFavoriteBook] = useState("")
  const [favoriteAuthor, setFavoriteAuthor] = useState("")
  const [preferredGenre, setPreferredGenre] = useState("fiction")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [passwordError, setPasswordError] = useState("")
  const [emailError, setEmailError] = useState("")

  // Add state for forgot password functionality
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [resetEmail, setResetEmail] = useState("");

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5001/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: loginUsername,
          password: loginPassword
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        // Display alert for login failures
        Alert.alert(
          "Login Failed", 
          data.error || "Username or password is incorrect",
          [{ text: "OK" }]
        );
        throw new Error(data.error || 'Login failed');
      }

      // Log the response to verify the structure
      console.log('Login response:', data);

      // Use data.userId (camelCase) from the API response
      // but pass it as user_id (snake_case) to match your navigation types
      navigation.navigate('Main', { 
        user_id: data.userId  // Pass API's userId as user_id to match navigation types
      });

    } catch (error: any) {
      setEmailError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // Add function to handle password reset
  const handleResetPassword = async () => {
    if (!resetEmail) {
      Alert.alert("Error", "Please enter your email address");
      return;
    }

    if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(resetEmail)) {
      Alert.alert("Error", "Please enter a valid email address");
      return;
    }

    setLoading(true);
    try {
      // You'll need to implement this endpoint in your backend
      const response = await fetch('http://localhost:5001/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: resetEmail }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Password reset failed');
      }

      Alert.alert(
        "Success", 
        "If an account with that email exists, you will receive password reset instructions.",
        [{ text: "OK" }]
      );
      setShowForgotPassword(false);
    } catch (error: any) {
      Alert.alert("Error", error.message);
    } finally {
      setLoading(false);
    }
  }

  const handleRegister = async () => {
    // Validate all fields
    if (!username || !email || !password || !age || !gender || !favoriteBook || !favoriteAuthor || !preferredGenre) {
      setEmailError('All fields are required');
      return;
    }

    if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
      setEmailError('Invalid email format');
      return;
    }

    if (password !== confirmPassword) {
      setPasswordError('Passwords do not match');
      return;
    }

    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5001/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          age: Number(age),
          gender,
          favoriteBook,
          favoriteAuthor,
          preferredGenre
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }

      // Log the response to verify the structure
      console.log('Register response:', data);

      // Use data.userId (camelCase) from the API response
      // but pass it as user_id (snake_case) to match your navigation types
      navigation.navigate('Main', { 
        user_id: data.userId  // Pass API's userId as user_id to match navigation types
      });
    } catch (error: any) {
      setEmailError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const renderLogin = () => (
    <View style={styles.formContainer}>
      <Input
        placeholder="Username"
        value={loginUsername}
        onChangeText={setLoginUsername}
        autoCapitalize="none"
        disabled={loading}
      />
      <Input
        placeholder="Password"
        value={loginPassword}
        onChangeText={setLoginPassword}
        secureTextEntry
        disabled={loading}
      />
      <Button 
        title="Login" 
        onPress={handleLogin} 
        loading={loading} 
        disabled={loading}
        buttonStyle={{ borderRadius: 20 }}
      />
      <TouchableOpacity 
        onPress={() => setShowForgotPassword(true)}
        style={styles.forgotPasswordLink}
      >
        <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
      </TouchableOpacity>
      
      {/* Forgot Password Modal */}
      <Modal
        visible={showForgotPassword}
        transparent={true}
        animationType="slide"
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Reset Password</Text>
            <Text style={styles.modalText}>
              Enter your email address to receive a password reset link.
            </Text>
            <Input
              placeholder="Email"
              value={resetEmail}
              onChangeText={setResetEmail}
              autoCapitalize="none"
              keyboardType="email-address"
            />
            <View style={styles.modalButtons}>
              <Button
                title="Cancel"
                onPress={() => setShowForgotPassword(false)}
                buttonStyle={styles.modalCancelButton}
              />
              <Button
                title="Reset"
                onPress={handleResetPassword}
                loading={loading}
                disabled={loading}
                buttonStyle={styles.modalResetButton}
              />
            </View>
          </View>
        </View>
      </Modal>
    </View>
  )

  const renderRegister = () => (
    <ScrollView style={styles.formContainer}>
      <Input
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
        disabled={loading}
      />
      <Input
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
        disabled={loading}
        errorMessage={emailError}
      />
      <Input 
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        disabled={loading}
        autoCapitalize="none"
        autoCorrect={false}
        textContentType="oneTimeCode"
        autoComplete="off"
      />
      <Input
        placeholder="Confirm Password"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
        disabled={loading}
        errorMessage={passwordError}
        autoCapitalize="none"
        autoCorrect={false}
        textContentType="oneTimeCode"  // 👈 important
        autoComplete="off"
      />
      <Input placeholder="Age" value={age} onChangeText={setAge} keyboardType="numeric" disabled={loading} />

      <View style={styles.pickerContainer}>
        <Text style={styles.label}>Gender</Text>
        <Picker selectedValue={gender} onValueChange={setGender} enabled={!loading} style={styles.picker}>
          <Picker.Item label="Select gender" value="" />
          <Picker.Item label="Male" value="male" />
          <Picker.Item label="Female" value="female" />
          <Picker.Item label="Other" value="other" />
          <Picker.Item label="Prefer not to say" value="not_specified" />
        </Picker>
      </View>

      <Input placeholder="Favorite Book" value={favoriteBook} onChangeText={setFavoriteBook} disabled={loading} />
      <Input placeholder="Favorite Author" value={favoriteAuthor} onChangeText={setFavoriteAuthor} disabled={loading} />

      <View style={styles.pickerContainer}>
        <Text style={styles.label}>Preferred Genre</Text>
        <Picker
          selectedValue={preferredGenre}
          onValueChange={setPreferredGenre}
          enabled={!loading}
          style={styles.picker}
        >
          <Picker.Item label="Fiction" value="fiction" />
          <Picker.Item label="Non-fiction" value="nonfiction" />
        </Picker>
      </View>

      <Button 
        title="Register" 
        onPress={handleRegister} 
        loading={loading} 
        disabled={loading}
        buttonStyle={{ borderRadius: 20 }}
      />
    </ScrollView>
  )

  return (
    <ThemeProvider theme={theme}>
      <SafeAreaView style={styles.container}>
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : "height"}
          style={styles.keyboardAvoidingView}
        >
          <Text style={styles.welcomeText}>Welcome to BookLoom</Text>
          <View style={styles.tabContainer}>
            <Button
              title="Login"
              type={mode === "login" ? "solid" : "outline"}
              onPress={() => setMode("login")}
              containerStyle={styles.tabButton}
            />
            <Button
              title="Register"
              type={mode === "register" ? "solid" : "outline"}
              onPress={() => setMode("register")}
              containerStyle={styles.tabButton}
            />
          </View>
          {mode === "login" ? renderLogin() : renderRegister()}
        </KeyboardAvoidingView>
      </SafeAreaView>
    </ThemeProvider>
  )
}

