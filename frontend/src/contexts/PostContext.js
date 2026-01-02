import React, { createContext, useState, useEffect, useContext } from 'react';
import {
  fetchPostsWithImages,
  createPost,
  searchPostsWithImages,
  getGeneratedTextForPost,
} from '../services/api';

const PostsContext = createContext();

export const PostsProvider = ({ children }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load all posts (with images) on mount
  useEffect(() => {
    setLoading(true);
    fetchPostsWithImages()
      .then(data => setPosts(data.posts || []))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  // Add post and reload feed (with images)
  const addPost = async (newPost) => {
    await createPost(newPost);
    const data = await fetchPostsWithImages();
    setPosts(data.posts || []);
  };

  // Search posts (with images)
  const doSearch = async (query) => {
    const data = await searchPostsWithImages(query);
    return data.posts || [];
  };

  const getText = async (query) => {
    const data = await getGeneratedTextForPost(query);
    return data.json() || [];
  };

  return (
    <PostsContext.Provider value={{
      posts,
      setPosts,
      loading,
      error,
      addPost,
      doSearch,
      getText,
    }}>
      {children}
    </PostsContext.Provider>
  );
};

export const usePosts = () => useContext(PostsContext);