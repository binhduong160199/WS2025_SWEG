import { API_BASE_URL } from '../utils/constants';

export const fetchPostsWithImages = async () => {
  const response = await fetch(`${API_BASE_URL}/posts`);
  if (!response.ok) {
    throw new Error('Failed to fetch posts');
  }

  const data = await response.json();
  return {
    posts: data.posts || [],
  };
};

export const fetchPostDetail = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/posts/${postId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch post detail');
  }

  return response.json();
};

export const fetchLatestPostWithImage = async () => {
  const response = await fetch(`${API_BASE_URL}/posts/latest`);
  if (!response.ok) {
    throw new Error('Failed to fetch latest post');
  }

  return response.json();
};

export const searchPostsWithImages = async (query) => {
  const response = await fetch(
    `${API_BASE_URL}/posts/search?q=${encodeURIComponent(query)}`
  );

  if (!response.ok) {
    throw new Error('Failed to search posts');
  }

  const data = await response.json();

  return {
    posts: data.posts || [],
  };
};

export const createPost = async (newPost) => {
  const response = await fetch(`${API_BASE_URL}/posts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newPost),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to create post');
  }

  return response.json();
};

export const generateText = async (prompt) => {
  const response = await fetch(`${API_BASE_URL}/posts/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to generate text');
  }

  return response.json();
};

export const getLatestGeneratedText = async () => {
  const response = await fetch(`${API_BASE_URL}/posts/generated-text`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to fetch generated text');
  }

  return response.json(); 
};

export const api = {
  fetchPostsWithImages,
  fetchPostDetail,
  fetchLatestPostWithImage,
  searchPostsWithImages,
  createPost,
  generateText,
  getLatestGeneratedText,
};
