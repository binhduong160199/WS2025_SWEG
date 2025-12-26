import React from 'react';
import '../styles/SentimentBadge.css';

/**
 * SentimentBadge Component
 * Displays sentiment analysis result with color-coded badge
 */
const SentimentBadge = ({ sentiment, score, processingStatus }) => {
  if (!sentiment || !score) {
    return null;
  }

  const sentimentClass = sentiment === 'POSITIVE' ? 'positive' : 'negative';
  const displayScore = (score * 100).toFixed(0);

  if (processingStatus === 'pending' || processingStatus === 'processing') {
    return (
      <div className="sentiment-badge loading">
        <span className="sentiment-label">Analyzing...</span>
      </div>
    );
  }

  return (
    <div className={`sentiment-badge ${sentimentClass}`}>
      <span className="sentiment-label">{sentiment}</span>
      <span className="sentiment-score">{displayScore}%</span>
    </div>
  );
};

export default SentimentBadge;
