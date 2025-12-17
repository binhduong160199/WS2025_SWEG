import React, { useState } from 'react';
import { API_BASE_URL } from '../utils/constants';

const LazyImage = ({ post }) => {
  const [fullImage, setFullImage] = useState(post.image || null);
  const [loading, setLoading] = useState(false);

  const handleLoadFull = async () => {
    if (fullImage) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/posts/${post.id}`);
      if (res.ok) {
        const data = await res.json();
        setFullImage(data.image || null);
      }
    } catch (e) {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  const displaySrc = fullImage
    ? `data:image/jpeg;base64,${fullImage}`
    : (post.thumbnail ? `data:image/jpeg;base64,${post.thumbnail}` : null);

  return (
    <div className="relative">
      {displaySrc ? (
        <img
          src={displaySrc}
          alt="Post"
          className="w-full h-auto object-cover transition-transform duration-300 group-hover:scale-105 cursor-pointer"
          onClick={handleLoadFull}
        />
      ) : null}
      {!fullImage && post.thumbnail && (
        <button onClick={handleLoadFull} className="absolute bottom-2 right-2 bg-black/50 text-white px-3 py-1 rounded-md text-sm">{loading ? 'Loading...' : 'View full'}</button>
      )}
    </div>
  );
};

export default LazyImage;
