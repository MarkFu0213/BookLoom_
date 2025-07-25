import React, { useState, useEffect, useLayoutEffect } from 'react';
import { 
  View, 
  Text, 
  FlatList, 
  TouchableOpacity, 
  StyleSheet, 
  ScrollView, 
  Image, 
  ActivityIndicator, 
  Alert 
} from 'react-native';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Icon } from '@rneui/themed';

// Define your navigation parameter list
type RootStackParamList = {
  Main: { user_id: string };
  Profile: { user_id: string };
};

type MainPageRouteProp = RouteProp<RootStackParamList, 'Main'>;
type MainScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Main'>;

interface Book {
  id: string;
  title: string;
  author: string;
  cover: string;
  text?: string;
}

const editingOptions: string[] = ['Romantic', 'Explorative'];

const MainPage: React.FC = () => {
  const navigation = useNavigation<MainScreenNavigationProp>();
  const route = useRoute<MainPageRouteProp>();
  const { user_id } = route.params;

  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [booksData, setBooksData] = useState<Book[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  console.log('Main screen user_id:', user_id);

  // Set header options for Profile navigation
  useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <TouchableOpacity
          style={styles.profileButton}
          onPress={() => navigation.navigate('Profile', { user_id })}
        >
          <Icon name="person-outline" type="material" size={28} color="#fff" />
        </TouchableOpacity>
      ),
    });
  }, [navigation, user_id]);


  const coverURLs: string[] = [
    'https://m.media-amazon.com/images/M/MV5BMTA1NDQ3NTcyOTNeQTJeQWpwZ15BbWU3MDA0MzA4MzE@._V1_.jpg',
    'https://m.media-amazon.com/images/I/91GoCrV6emL.jpg',
    'https://lumiere-a.akamaihd.net/v1/images/p_thehunchbackofnotredame_19900_f53cfc42.jpeg?region=0%2C0%2C540%2C810',
  ];

  // Fetch books listing when component mounts
  useEffect(() => {
    const fetchBooks = async () => {
      setLoading(true);
      try {
        // GET /books returns list without the text field.
        const response = await fetch('http://localhost:5001/books');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const mappedData = data.map((book: any, index: number) => ({
          id: book.book_serial ? book.book_serial.toString() : book._id,
          title: book.title,
          author: book.author,
          cover: coverURLs[index % coverURLs.length],
        }));
        setBooksData(mappedData);
      } catch (err) {
        console.error('Error fetching books:', err);
        setError('Failed to fetch books');
      } finally {
        setLoading(false);
      }
    };
    fetchBooks();
  }, []);

  // Fetch full details (including text) for a specific book
  const fetchBookDetails = async (book_serial: number) => {
    try {
      const response = await fetch(`http://localhost:5001/books/${book_serial}`);
      if (!response.ok) {
        throw new Error('Failed to fetch book details');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching book details:', error);
      return null;
    }
  };

  // Send a PUT request to update the chapter, then poll until the text changes
  const updateChapter = async (option: string) => {
    if (!selectedBook) {
      Alert.alert("No book selected", "Please select a book first.");
      return;
    }
    try {
      const bookSerial = parseInt(selectedBook.id, 10);
      // Initiate the asynchronous update on the backend.
      const response = await fetch(`http://localhost:5001/books/${bookSerial}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ editingOption: option }),
      });
      if (!response.ok) {
        throw new Error('Failed to update chapter');
      }
      const data = await response.json();
      console.log('Update initiated:', data);

      // Poll for the updated book details every 2 seconds.
      const pollInterval = 2000; // 2 seconds interval
      const maxAttempts = 15;    // e.g., poll up to 30 seconds
      let attempts = 0;

      const pollForUpdate = async () => {
        attempts++;
        const details = await fetchBookDetails(bookSerial);
        if (details && details.text && details.text !== selectedBook?.text) {
          // Once updated text is detected, update the state.
          setSelectedBook({ ...selectedBook, text: details.text });
          clearInterval(polling);
        } else if (attempts >= maxAttempts) {
          clearInterval(polling);
          Alert.alert('Notice', 'The chapter update is taking longer than expected.');
        }
      };

      const polling = setInterval(pollForUpdate, pollInterval);
    } catch (error) {
      console.error('Error updating chapter:', error);
      Alert.alert("Update Error", "Failed to update chapter.");
    }
  };

  // When a book is selected, fetch its full details (with text) and update state
  const onSelectBook = async (book: Book) => {
    const bookSerial = parseInt(book.id, 10);
    const details = await fetchBookDetails(bookSerial);
    if (details) {
      setSelectedBook({
        ...book,
        text: details.text,
      });
    }
  };

  const renderBookItem = ({ item }: { item: Book }) => (
    <TouchableOpacity
      style={[
        styles.bookItem,
        selectedBook?.id === item.id && styles.selectedBookItem,
      ]}
      onPress={() => onSelectBook(item)}
    >
      <Image source={{ uri: item.cover }} style={styles.bookCover} />
      <Text style={styles.bookTitle}>{item.title}</Text>
      <Text style={styles.bookAuthor}>{item.author}</Text>
    </TouchableOpacity>
  );

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>BookLoom</Text>
        <TouchableOpacity
          style={styles.profileButton}
          onPress={() => navigation.navigate('Profile', { user_id })}
        >
          <Text style={styles.profileButtonText}>Profile</Text>
        </TouchableOpacity>
      </View>

      {loading && <ActivityIndicator size="large" color="#fff" />}
      {error && <Text style={{ color: 'red' }}>{error}</Text>}

      <Text style={styles.sectionTitle}>Library</Text>
      <FlatList
        data={booksData}
        renderItem={renderBookItem}
        keyExtractor={(item) => item.id}
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.bookList}
      />

      <Text style={styles.sectionTitle}>Editing Options</Text>
      <View style={styles.optionsContainer}>
        {editingOptions.map((option) => (
          <TouchableOpacity
            key={option}
            style={[
              styles.optionButton,
              selectedOption === option && styles.selectedOptionButton,
            ]}
            onPress={() => {
              setSelectedOption(option);
              updateChapter(option);
            }}
          >
            <Text style={styles.optionText}>{option}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle}>Generated Story</Text>
      <View style={styles.storyContainer}>
        <Text style={styles.storyText}>
          {selectedBook && selectedOption
            ? selectedBook.text
              ? selectedBook.text
              : `Displaying a ${selectedOption} version of ${selectedBook.title} by ${selectedBook.author}. (This is a placeholder until the update completes.)`
            : 'Select a book and an editing option to see the generated story.'}
        </Text>
      </View>

      <TouchableOpacity
        style={styles.goToProfileButton}
        onPress={() => navigation.navigate('Profile', { user_id })}
      >
        <Text style={styles.goToProfileButtonText}>Go to Profile</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#8B4513', // SaddleBrown background
    flexGrow: 1,
    alignItems: 'center',
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '100%',
    marginBottom: 20,
    marginTop: 70,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
    marginLeft: 95,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#fff',
    marginVertical: 10,
    textAlign: 'center',
  },
  bookList: {
    paddingVertical: 10,
    alignItems: 'center',
  },
  bookItem: {
    padding: 10,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#fff',
    borderRadius: 10,
    alignItems: 'center',
    backgroundColor: '#fffaf0',
  },
  selectedBookItem: {
    borderColor: '#deb887',
    backgroundColor: '#d2b48c',
  },
  bookCover: {
    width: 100,
    height: 150,
    resizeMode: 'cover',
    marginBottom: 5,
    borderRadius: 5,
  },
  bookTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#000',
    textAlign: 'center',
  },
  bookAuthor: {
    fontSize: 14,
    color: '#555',
    textAlign: 'center',
  },
  optionsContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    justifyContent: 'center',
  },
  optionButton: {
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderWidth: 1,
    borderColor: '#fff',
    borderRadius: 20,
    marginRight: 10,
    backgroundColor: '#fffaf0',
  },
  selectedOptionButton: {
    backgroundColor: '#deb887',
    borderColor: '#fff',
  },
  optionText: {
    color: '#000',
    textAlign: 'center',
  },
  storyContainer: {
    padding: 15,
    borderWidth: 1,
    borderColor: '#fff',
    borderRadius: 10,
    minHeight: 100,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff8e1',
  },
  storyText: {
    fontSize: 16,
    color: '#000',
    textAlign: 'center',
  },
  profileButton: {
    padding: 8,
    marginLeft: 10,
  },
  profileButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  goToProfileButton: {
    padding: 12,
    marginTop: 20,
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  goToProfileButtonText: {
    fontSize: 16,
    color: '#000',
    textAlign: 'center',
    fontWeight: '600',
  },
});

export default MainPage;
