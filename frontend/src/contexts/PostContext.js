import React, { createContext, useState, useEffect, useContext } from 'react';
import {
  fetchPostsWithImages,
  createPost,
  searchPostsWithImages,
  generateText,
  getLatestGeneratedText,
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

  const requestGeneratedText = async (prompt) => {
    // Start the async generation (the backend will queue the job)
    await generateText(prompt);

    // Now poll for the result
    let retries = 0;
    const maxRetries = 20; // ~20 seconds
    const interval = 1000; // 1 second

    while (retries < maxRetries) {
      const { generated_text } = await getLatestGeneratedText();
      if (generated_text && generated_text.trim() !== "") {
        return generated_text;
      }
      await new Promise((res) => setTimeout(res, interval));
      retries++;
    }
    throw new Error("Timeout: No generated text found. Please try again.");
  };

  const getGeneratedText = async () => {
    const data = await getLatestGeneratedText();
    return data.generated_text || "";
  };

  return (
    <PostsContext.Provider value={{
      posts,
      setPosts,
      loading,
      error,
      addPost,
      doSearch,
      requestGeneratedText,
      getGeneratedText,
    }}>
      {children}
    </PostsContext.Provider>
  );
};

export const usePosts = () => useContext(PostsContext);