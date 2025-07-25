import { useState, useEffect } from "react"
import { View, Text, StyleSheet, ScrollView, TextInput, Alert, ActivityIndicator, TouchableOpacity } from "react-native"
import { ThemeProvider, createTheme, Button, Card, Icon } from "@rneui/themed"
import { RouteProp, useNavigation } from "@react-navigation/native"
import { RootStackParamList } from "@/types/navigation"
import { styles } from "./styles"

const theme = createTheme({
  lightColors: {
    primary: "#8B4513", // SaddleBrown
    secondary: "#D2691E", // Chocolate
    background: "#FAEBD7", // AntiqueWhite
    white: "#FFFFFF",
    grey0: "#F5DEB3", // Wheat
    grey1: "#DEB887", // BurlyWood
  },
})

type ProfileScreenRouteProp = RouteProp<RootStackParamList, "Profile">

type ProfileProps = {
  route: ProfileScreenRouteProp
}

export default function ProfileScreen({ route }: ProfileProps) {
  const { user_id } = route.params || {}
  
  // Add debug log
  console.log('Profile screen user_id:', user_id);
  
  if (!user_id) {
    return (
      <View style={styles.container}>
        <Text>Error: No user specified</Text>
      </View>
    )
  }
  const navigation = useNavigation()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  
  // State for editable fields
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    age: '',
    gender: '',
    favoriteBook: '',
    favoriteAuthor: '',
    preferredGenre: 'fiction'
  })

  // Fetch user data on mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:5001/users/${user_id}/profile`)
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to fetch profile')
        }
        
        const data = await response.json()
        
        setProfile({
          username: data.username || '',
          email: data.email || '',
          age: data.age?.toString() || '',
          gender: data.gender || '',
          favoriteBook: data.favoriteBook || '',
          favoriteAuthor: data.favoriteAuthor || '',
          preferredGenre: data.preferredGenre || 'fiction'
        })
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
        Alert.alert('Error', errorMessage);
      } finally {
        setIsLoading(false)
      }
    }
    fetchProfile()
  }, [user_id])

  const handleUpdate = async () => {
    try {
      const updateData = {
        username: profile.username,
        email: profile.email,
        age: Number(profile.age),
        gender: profile.gender,
        favoriteBook: profile.favoriteBook,
        favoriteAuthor: profile.favoriteAuthor,
        preferredGenre: profile.preferredGenre
      };

      const response = await fetch(`http://localhost:5001/users/${user_id}/profile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData)
      });

      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Update failed');
      
      setIsEditing(false);
      Alert.alert('Success', 'Profile updated successfully');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
      Alert.alert('Error', errorMessage);
    }
  }

  const handleDelete = async () => {
    Alert.alert(
      'Confirm Deletion',
      'All your data will be permanently deleted. Continue?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              const response = await fetch(`http://localhost:5001/users/${user_id}`, {
                method: 'DELETE'
              });
              
              if (!response.ok) {
                const errorData = await response.json();
                const message = errorData.error instanceof Error ? errorData.error.message : 'Unknown error occurred';
                throw new Error(message);
              }
              
              navigation.navigate('Auth');
            } catch (error) {
              const message = error instanceof Error ? error.message : 'Unknown error occurred';
              Alert.alert('Deletion Error', message);
            }
          }
        }
      ]
    );
  }

  // Add logout handler function
  const handleLogout = () => {
    Alert.alert(
      'Confirm Logout',
      'Are you sure you want to log out?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          onPress: () => {
            // Navigate back to the Auth screen
            navigation.navigate('Auth');
          }
        }
      ]
    );
  }

  // Show loading indicator while the profile is being fetched
  if (isLoading) {
    return (
      <ThemeProvider theme={theme}>
        <View style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
          <ActivityIndicator size="large" color={theme.lightColors.primary} />
          <Text style={{ marginTop: 10 }}>Loading Profile...</Text>
        </View>
      </ThemeProvider>
    )
  }

  return (
    <ThemeProvider theme={theme}>
      <View style={styles.container}>
        {/* Header with back button and logout button */}
        <View style={styles.header}>
          <TouchableOpacity 
            style={styles.backButton} 
            onPress={() => navigation.goBack()}
          >
            <Icon name="arrow-back" type="material" color="#FAEBD7" size={28} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>My Profile</Text>
          
          {/* Replace the headerSpacer with logout button */}
          <TouchableOpacity 
            style={styles.headerLogoutButton} 
            onPress={handleLogout}
          >
            <Icon name="logout" type="material" color="#FAEBD7" size={22} />
            <Text style={styles.headerLogoutText}>Logout</Text>
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.scrollContent}>
          <Card containerStyle={styles.card}>
            <Card.Title style={styles.cardTitle}>Personal Information</Card.Title>
            <Card.Divider />
            
            <View style={styles.infoRow}>
              <Icon name="person" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.username}
                onChangeText={(text) => setProfile({...profile, username: text})}
                editable={isEditing}
              />
            </View>
            <View style={styles.infoRow}>
              <Icon name="email" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.email}
                onChangeText={(text) => setProfile({...profile, email: text})}
                editable={isEditing}
                keyboardType="email-address"
              />
            </View>
            <View style={styles.infoRow}>
              <Icon name="cake" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.age}
                onChangeText={(text) => setProfile({...profile, age: text.replace(/[^0-9]/g, '')})}
                editable={isEditing}
                keyboardType="numeric"
              />
            </View>
            <View style={styles.infoRow}>
              <Icon name="person" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.gender}
                onChangeText={(text) => setProfile({...profile, gender: text})}
                editable={isEditing}
              />
            </View>
          </Card>

          <Card containerStyle={styles.card}>
            <Card.Title style={styles.cardTitle}>Reading Preferences</Card.Title>
            <Card.Divider />
            <View style={styles.infoRow}>
              <Icon name="book" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.favoriteBook}
                onChangeText={(text) => setProfile({...profile, favoriteBook: text})}
                editable={isEditing}
              />
            </View>
            <View style={styles.infoRow}>
              <Icon name="person" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.favoriteAuthor}
                onChangeText={(text) => setProfile({...profile, favoriteAuthor: text})}
                editable={isEditing}
              />
            </View>
            <View style={styles.infoRow}>
              <Icon name="category" type="material" color={theme.lightColors.primary} />
              <TextInput
                style={[styles.input, { borderBottomWidth: isEditing ? 1 : 0 }]}
                value={profile.preferredGenre}
                onChangeText={(text) => setProfile({...profile, preferredGenre: text})}
                editable={isEditing}
              />
            </View>
          </Card>
        </ScrollView>
        
        {/* Bottom action buttons */}
        <View style={styles.bottomActions}>
          <Button
            title={isEditing ? "Save Changes" : "Edit Profile"}
            onPress={isEditing ? handleUpdate : () => setIsEditing(true)}
            buttonStyle={styles.editButton}
            icon={
              <Icon 
                name={isEditing ? "save" : "edit"} 
                type="material" 
                color="white" 
                size={18} 
                style={{marginRight: 5}}
              />
            }
          />
          
          <Button
            title="Delete Account"
            onPress={handleDelete}
            buttonStyle={styles.deleteButton}
            titleStyle={styles.deleteButtonText}
            icon={
              <Icon 
                name="delete" 
                type="material" 
                color="white" 
                size={18} 
                style={{marginRight: 5}}
              />
            }
          />
        </View>
      </View>
    </ThemeProvider>
  )
}
