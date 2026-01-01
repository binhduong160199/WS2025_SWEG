import React, { useState } from 'react';
import { X, Send, Image as ImageIcon, CheckCircle, Sparkles } from 'lucide-react';
import { usePosts } from '../contexts/PostContext';
import { api } from '../services/api';

const initialPostState = {
  user: '',
  text: '',
  image: null,
};

const CreatePostModal = ({ onClose }) => {
  const { addPost } = usePosts();
  const [newPost, setNewPost] = useState(initialPostState);
  const [preview, setPreview] = useState(null);

  const [successMessage, setSuccessMessage] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      const base64String = reader.result.split(',')[1];
      setNewPost((prev) => ({ ...prev, image: base64String }));
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewPost((prev) => ({ ...prev, [name]: value }));
  };

  const handleGenerateSuggestion = async () => {
    if (!newPost.text.trim()) {
      setSuccessMessage('Please enter some text first to generate suggestions.');
      setTimeout(() => setSuccessMessage(''), 3000);
      return;
    }

    setIsGenerating(true);
    try {
      const response = await api.generateText(newPost.text);
      if (response?.suggestions?.length) {
        setSuggestions(response.suggestions);
        setSuccessMessage('Suggestions generated! Click one to apply.');
        setTimeout(() => setSuccessMessage(''), 5000);
      }
    } catch (error) {
      setSuccessMessage('Failed to generate suggestions. Please try again.');
      setTimeout(() => setSuccessMessage(''), 3000);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleUseSuggestion = (suggestion) => {
    setNewPost((prev) => ({ ...prev, text: suggestion }));
    setSuggestions([]);
    setSuccessMessage('Suggestion applied!');
    setTimeout(() => setSuccessMessage(''), 2000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!newPost.user.trim() || !newPost.text.trim()) {
      setSuccessMessage('Please fill in all required fields.');
      setTimeout(() => setSuccessMessage(''), 3000);
      return;
    }

    await addPost(newPost);

    setNewPost(initialPostState);
    setPreview(null);
    setSuggestions([]);
    setSuccessMessage('Post created successfully!');
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-2xl border border-purple-500/30 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="p-6 border-b border-purple-500/20 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white">Create New Post</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Message */}
        {successMessage && (
          <div className="mx-6 mt-4 flex items-center gap-2 bg-green-600/20 border border-green-500/40 text-green-300 px-4 py-3 rounded-xl">
            <CheckCircle className="w-5 h-5" />
            <span>{successMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 p-6">
          {/* AI Suggestions */}
          <div>
            <div className="flex items-center justify-between">
              <button
                type="button"
                onClick={handleGenerateSuggestion}
                disabled={isGenerating || !newPost.text.trim()}
                className="text-sm text-purple-400 hover:text-purple-300 flex items-center gap-1 disabled:opacity-50"
              >
                <Sparkles className="w-4 h-4" />
                {isGenerating ? 'Generating...' : 'Generate Suggestions'}
              </button>
              <span className="text-sm text-gray-400">
                {newPost.text.length}/500
              </span>
            </div>

            {suggestions.length > 0 && (
              <div className="mt-3 space-y-2">
                <p className="text-sm font-medium text-gray-300">
                  AI Suggestions:
                </p>
                {suggestions.map((suggestion, index) => (
                  <div
                    key={index}
                    onClick={() => handleUseSuggestion(suggestion)}
                    className="bg-purple-500/10 border border-purple-500/30 rounded-lg px-3 py-2 text-sm text-gray-300 cursor-pointer hover:bg-purple-500/20"
                  >
                    {suggestion}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Username *
            </label>
            <input
              name="user"
              value={newPost.user}
              onChange={handleChange}
              maxLength={50}
              required
              className="w-full bg-white/5 border border-purple-500/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/20"
              placeholder="Enter your username"
            />
          </div>

          {/* Text */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              What's on your mind? *
            </label>
            <textarea
              name="text"
              value={newPost.text}
              onChange={handleChange}
              rows={4}
              maxLength={500}
              required
              className="w-full bg-white/5 border border-purple-500/30 rounded-xl px-4 py-3 text-white resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/20"
              placeholder="Share your thoughts..."
            />
          </div>

          {/* Image Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Add Image (Optional)
            </label>
            <input
              type="file"
              accept="image/*"
              id="image-upload"
              onChange={handleImageUpload}
              className="hidden"
            />
            <label
              htmlFor="image-upload"
              className="flex flex-col items-center justify-center bg-white/5 border border-purple-500/30 rounded-xl px-4 py-8 cursor-pointer"
            >
              {preview ? (
                <img src={preview} alt="Preview" className="max-h-40 rounded" />
              ) : (
                <ImageIcon className="w-12 h-12 text-gray-400" />
              )}
              <span className="text-sm text-gray-400 mt-2">
                {preview ? 'Image selected ✓' : 'Click to upload image'}
              </span>
            </label>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 rounded-xl border border-purple-500/30 text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 text-white flex items-center justify-center gap-2"
            >
              <Send className="w-5 h-5" />
              Post
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreatePostModal;