import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#FAEBD7",
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: 15,
      backgroundColor: "#8B4513",
    },
    backButton: {
      padding: 5,
      marginTop: 10
    },
    headerTitle: {
      fontSize: 20,
      fontWeight: 'bold',
      color: "#FAEBD7",
      marginLeft: 30,
      marginTop: 10
    },
    headerSpacer: {
      width: 30, // To balance the layout with the back button
    },
    scrollContent: {
      flex: 1,
    },
    bottomActions: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      padding: 15,
      backgroundColor: '#FFF8DC',
      borderTopWidth: 1,
      borderTopColor: '#DEB887',

    },
    username: {
      fontSize: 24,
      fontWeight: "bold",
      color: "#FAEBD7",
    },
    card: {
      borderRadius: 10,
      marginHorizontal: 10,
      marginBottom: 15,
      backgroundColor: "#FFF8DC",
      shadowColor: "#8B4513",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    },
    cardTitle: {
      color: "#8B4513",
      fontSize: 18,
    },
    infoRow: {
      flexDirection: "row",
      alignItems: "center",
      marginBottom: 10,
    },
    infoText: {
      marginLeft: 10,
      fontSize: 16,
      color: "#D2691E",
    },
    profilePictureContainer: {
      width: 150,
      height: 150,
      borderRadius: 75,
      backgroundColor: "#FFF8DC",
      justifyContent: "center",
      alignItems: "center",
      borderWidth: 2,
      borderColor: "#8B4513",
    },
    input: {
      flex: 1,
      marginLeft: 10,
      color: '#000',
      borderColor: '#8B4513'
    },
    editButton: {
      backgroundColor: '#8B4513',
      paddingHorizontal: 20,
      minWidth: 150,
      borderRadius: 10,
    },
    deleteButton: {
      backgroundColor: '#FF4444',
      paddingHorizontal: 20,
      minWidth: 150,
      borderRadius: 10,
    },
    deleteButtonText: {
      color: '#FFFFFF',
    },

    headerLogoutButton: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
      paddingRight: -10,
      marginTop: 10
    },
    
    headerLogoutText: {
      color: '#FAEBD7',
      fontSize: 14,
      fontWeight: '600',
      marginLeft: 2,
    },
  })
  
  