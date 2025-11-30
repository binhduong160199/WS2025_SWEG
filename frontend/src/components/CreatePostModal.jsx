import React, { useState } from 'react';
import { X, Send, Image as ImageIcon, CheckCircle } from 'lucide-react';
import { usePosts } from '../contexts/PostContext';

const initialPostState = {
  user: '',
  text: '',
  image: null,
};

const CreatePostModal = ({ onClose }) => {
  const { addPost } = usePosts();
  const [newPost, setNewPost] = useState(initialPostState);
  const [preview, setPreview] = useState(null);

  const [successMessage, setSuccessMessage] = useState("");

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result.split(',')[1];
        setNewPost(prev => ({ ...prev, image: base64String }));
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewPost(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!newPost.user.trim() || !newPost.text.trim()) {
      setSuccessMessage("Please fill in all required fields.");
      setTimeout(() => setSuccessMessage(""), 3000); 
      return;
    }

    await addPost(newPost);

    setNewPost(initialPostState);
    setPreview(null);
    setSuccessMessage("Post created successfully!");
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-2xl border border-purple-500/30 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-purple-500/20 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white">Create New Post</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {successMessage && (
          <div className="mx-6 mt-4 mb-2 flex items-center gap-2 bg-green-600/20 border border-green-500/40 text-green-300 px-4 py-3 rounded-xl animate-fadeIn">
            <CheckCircle className="w-5 h-5" />
            <span>{successMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Username *
            </label>
            <input
              name="user"
              type="text"
              value={newPost.user}
              onChange={handleChange}
              className="w-full bg-white/5 border border-purple-500/30 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
              placeholder="Enter your username"
              maxLength={50}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              What's on your mind? *
            </label>
            <textarea
              name="text"
              value={newPost.text}
              onChange={handleChange}
              className="w-full bg-white/5 border border-purple-500/30 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 resize-none"
              placeholder="Share your thoughts..."
              rows={4}
              maxLength={500}
              required
            />
            <div className="text-right text-sm text-gray-400 mt-1">
              {newPost.text.length}/500
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Add Image (Optional)
            </label>
            <div className="relative">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="flex items-center justify-center w-full bg-white/5 border border-purple-500/30 rounded-xl px-4 py-8 text-gray-400 hover:border-purple-500 cursor-pointer transition-all"
              >
                <div className="text-center">
                  {preview ? (
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-h-40 mx-auto mb-2 rounded"
                    />
                  ) : (
                    <ImageIcon className="w-12 h-12 mx-auto mb-2" />
                  )}
                  <span className="text-sm">
                    {preview ? 'Image selected ✓' : 'Click to upload image'}
                  </span>
                </div>
              </label>
            </div>
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 rounded-xl border border-purple-500/30 text-gray-300 font-semibold hover:bg-white/5 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all flex items-center justify-center space-x-2"
            >
              <Send className="w-5 h-5" />
              <span>Post</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreatePostModal;