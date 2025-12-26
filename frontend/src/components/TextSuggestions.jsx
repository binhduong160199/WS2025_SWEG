import React, { useState } from 'react';
import '../styles/TextSuggestions.css';

/**
 * TextSuggestions Component
 * Displays generated text suggestions for a post
 */
const TextSuggestions = ({ generatedText, processingStatus }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!generatedText && processingStatus !== 'processing') {
    return null;
  }

  let suggestions = [];
  if (generatedText) {
    try {
      const parsed = JSON.parse(generatedText);
      suggestions = parsed.suggestions || [];
    } catch (e) {
      // If not valid JSON, treat as string
      suggestions = [generatedText];
    }
  }

  if (processingStatus === 'pending' || processingStatus === 'processing') {
    return (
      <div className="text-suggestions loading">
        <p className="suggestion-title">Generating suggestions...</p>
      </div>
    );
  }

  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  return (
    <div className="text-suggestions">
      <button
        className="suggestion-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        💡 Suggestions ({suggestions.length})
        <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
      </button>

      {isExpanded && (
        <div className="suggestions-list">
          {suggestions.map((suggestion, index) => (
            <div key={index} className="suggestion-item">
              <p className="suggestion-text">{suggestion}</p>
              <button
                className="suggestion-copy-btn"
                onClick={() => {
                  navigator.clipboard.writeText(suggestion);
                  alert('Suggestion copied to clipboard!');
                }}
              >
                Copy
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TextSuggestions;
