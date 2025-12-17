import { API_BASE_URL } from '../utils/constants';

export const fetchPostsWithImages = async () => {
  const response = await fetch(`${API_BASE_URL}/posts`);
  if (!response.ok) throw new Error('Failed to fetch posts');
  const data = await response.json();
  let posts = data.posts || [];

  // The backend now provides `thumbnail` (base64) in list responses.
  // Keep `image` empty until a detailed fetch is requested (lazy-load).
  return { posts };
};

export const fetchLatestPostWithImage = async () => {
  const response = await fetch(`${API_BASE_URL}/posts/latest`);
  if (!response.ok) throw new Error('Failed to fetch latest post');
  const post = await response.json();
  return post;
};

export const searchPostsWithImages = async (query) => {
  const response = await fetch(`${API_BASE_URL}/posts/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Failed to search posts');
  const data = await response.json();
  let posts = data.posts || [];

  // thumbnails are included in list responses; do not fetch full images here.
  return { posts };
};

export const createPost = async (newPost) => {
  const response = await fetch(`${API_BASE_URL}/posts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newPost),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to create post');
  }
  return response.json();
};