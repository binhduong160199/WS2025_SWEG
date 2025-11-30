import React from 'react';
import { PostsProvider } from './contexts/PostContext';
import MainPage from './components/MainPage';

const App = () => (
  <PostsProvider>
    <MainPage />
  </PostsProvider>
);

export default App;