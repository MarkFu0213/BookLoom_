export type RootStackParamList = {
  Main: { user_id: string };
  Auth: undefined;
  Profile: {
    user_id: string;
    username?: string;
    email?: string;
    age?: string;
    gender?: string;
    favoriteBook?: string;
    favoriteAuthor?: string;
    preferredGenre?: string;
  };
};