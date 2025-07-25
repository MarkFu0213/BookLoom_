import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#FAEBD7", // AntiqueWhite
    },
    keyboardAvoidingView: {
      flex: 1,
    },
    welcomeText: {
      fontSize: 24,
      fontWeight: "bold",
      color: "#8B4513", // SaddleBrown
      textAlign: "center",
      marginTop: 40,
      marginBottom: 20,
    },
    tabContainer: {
      flexDirection: "row",
      marginVertical: 20,
      paddingHorizontal: 20,
    },
    tabButton: {
      flex: 1,
      marginHorizontal: 5,
      borderRadius: 20,
    },
    formContainer: {
      padding: 20,
    },
    pickerContainer: {
      marginBottom: 15,
      paddingHorizontal: 10,
    },
    label: {
      fontSize: 16,
      color: "#8B4513", // SaddleBrown
      fontWeight: "bold",
      marginBottom: 5,
    },
    picker: {
      backgroundColor: "#FAEBD7", // AntiqueWhite
      borderWidth: 1,
      borderColor: "#8B4513", // SaddleBrown
      borderRadius: 5,
    },
    // Add the missing styles for the forgot password modal
    forgotPasswordLink: {
      marginTop: 10,
      alignSelf: 'center',
    },
    forgotPasswordText: {
      color: "#8B4513", // SaddleBrown
      fontSize: 14,
    },
    modalContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: 'rgba(0,0,0,0.5)',
    },
    modalContent: {
      width: '80%',
      backgroundColor: 'white',
      borderRadius: 10,
      padding: 20,
      alignItems: 'center',
    },
    modalTitle: {
      fontSize: 18,
      fontWeight: 'bold',
      marginBottom: 10,
      color: "#8B4513", // SaddleBrown
    },
    modalText: {
      textAlign: 'center',
      marginBottom: 20,
      color: "#666", // Dark gray
    },
    modalButtons: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: '100%',
    },
    modalCancelButton: {
      backgroundColor: '#999',
      borderRadius: 20,
    },
    modalResetButton: {
      borderRadius: 20,
      backgroundColor: "#8B4513", // SaddleBrown
    },
})
  
  