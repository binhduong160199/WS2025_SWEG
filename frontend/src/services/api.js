import { API_BASE_URL } from '../utils/constants';

export const fetchPostsWithImages = async () => {
  const response = await fetch(`${API_BASE_URL}/posts`);
  if (!response.ok) throw new Error('Failed to fetch posts');
  const data = await response.json();
  let posts = data.posts || [];

  // Always fetch image if exists
  await Promise.all(posts.map(async (post, i) => {
    if (post.has_image) {
      const detailRes = await fetch(`${API_BASE_URL}/posts/${post.id}`);
      if (detailRes.ok) {
        const detailData = await detailRes.json();
        posts[i].image = detailData.image || null;
      }
    }
  }));
  return { posts };
};

export const fetchLatestPostWithImage = async () => {
  const response = await fetch(`${API_BASE_URL}/posts/latest`);
  if (!response.ok) throw new Error('Failed to fetch latest post');
  const post = await response.json();
  if (post && post.has_image) {
    const detailRes = await fetch(`${API_BASE_URL}/posts/${post.id}`);
    if (detailRes.ok) {
      const detailData = await detailRes.json();
      post.image = detailData.image || null;
    }
  }
  return post;
};

export const searchPostsWithImages = async (query) => {
  const response = await fetch(`${API_BASE_URL}/posts/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Failed to search posts');
  const data = await response.json();
  let posts = data.posts || [];

  await Promise.all(posts.map(async (post, i) => {
    if (post.has_image) {
      const detailRes = await fetch(`${API_BASE_URL}/posts/${post.id}`);
      if (detailRes.ok) {
        const detailData = await detailRes.json();
        posts[i].image = detailData.image || null;
      }
    }
  }));
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