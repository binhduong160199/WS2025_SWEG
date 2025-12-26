import { API_BASE_URL } from '../utils/constants';

/**
 * Fetch posts for FEED
 * - Uses /posts
 * - Uses thumbnail ONLY
 * - DOES NOT fetch full image
 */
export const fetchPostsWithImages = async () => {
  const response = await fetch(`${API_BASE_URL}/posts`);
  if (!response.ok) {
    throw new Error('Failed to fetch posts');
  }

  const data = await response.json();

  // Backend already returns:
  // - thumbnail
  // - has_image
  // - has_thumbnail
  // - sentiment_label
  // - sentiment_score
  // - processing_status
  return {
    posts: data.posts || [],
  };
};

/**
 * Fetch a single post detail
 * - Uses /posts/:id
 * - Returns FULL image
 * - Used only when user clicks / opens detail
 */
export const fetchPostDetail = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/posts/${postId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch post detail');
  }

  return response.json();
};

/**
 * Fetch latest post
 * - Uses /posts/latest
 * - NO extra detail fetch
 * - Uses thumbnail only
 */
export const fetchLatestPostWithImage = async () => {
  const response = await fetch(`${API_BASE_URL}/posts/latest`);
  if (!response.ok) {
    throw new Error('Failed to fetch latest post');
  }

  return response.json();
};

/**
 * Search posts
 * - Uses /posts/search
 * - Uses thumbnail ONLY
 * - NO per-post detail requests
 */
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

/**
 * Create new post
 * - Backend will publish resize event if image exists
 * - Will also trigger sentiment analysis and text generation
 */
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

// ======================================================
// ML Features APIs
// ======================================================

/**
 * Fetch sentiment analysis for a post
 * - Returns sentiment_label and sentiment_score
 * - Returns processing_status
 */
export const fetchPostSentiment = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/posts/${postId}/sentiment`);
  if (!response.ok) {
    throw new Error('Failed to fetch post sentiment');
  }

  return response.json();
};

/**
 * Fetch generated text suggestions for a post
 * - Returns generated_text (JSON with suggestions array)
 * - Returns processing_status
 */
export const fetchGeneratedText = async (postId) => {
  const response = await fetch(
    `${API_BASE_URL}/posts/${postId}/generated-text`
  );
  if (!response.ok) {
    throw new Error('Failed to fetch generated text');
  }

  return response.json();
};

/**
 * Fetch all ML analysis for a post
 * - Returns combined sentiment and generated text
 * - Returns processing_status
 */
export const fetchMLAnalysis = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/posts/${postId}/ml-analysis`);
  if (!response.ok) {
    throw new Error('Failed to fetch ML analysis');
  }

  return response.json();
};

/**
 * Trigger re-analysis for a post
 * - Republishes sentiment analysis and text generation events
 * - Returns immediately with status
 */
export const reAnalyzePost = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/posts/${postId}/re-analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to trigger re-analysis');
  }

  return response.json();
};