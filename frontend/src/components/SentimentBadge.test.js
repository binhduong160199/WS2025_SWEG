/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SentimentBadge from '../SentimentBadge';

describe('SentimentBadge Component', () => {
  test('renders sentiment badge with positive sentiment', () => {
    render(
      <SentimentBadge 
        sentiment="POSITIVE" 
        score={0.85} 
        processingStatus="completed"
      />
    );
    
    const badge = screen.getByText(/POSITIVE/i);
    expect(badge).toBeInTheDocument();
    expect(screen.getByText(/85%/)).toBeInTheDocument();
  });

  test('renders sentiment badge with negative sentiment', () => {
    render(
      <SentimentBadge 
        sentiment="NEGATIVE" 
        score={0.65} 
        processingStatus="completed"
      />
    );
    
    expect(screen.getByText(/NEGATIVE/i)).toBeInTheDocument();
    expect(screen.getByText(/65%/)).toBeInTheDocument();
  });

  test('renders loading state during processing', () => {
    render(
      <SentimentBadge 
        sentiment={null} 
        score={null} 
        processingStatus="processing"
      />
    );
    
    expect(screen.getByText(/Analyzing/i)).toBeInTheDocument();
  });

  test('returns null when no sentiment data', () => {
    const { container } = render(
      <SentimentBadge 
        sentiment={null} 
        score={null} 
        processingStatus="completed"
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  test('displays score as percentage', () => {
    render(
      <SentimentBadge 
        sentiment="POSITIVE" 
        score={0.9} 
        processingStatus="completed"
      />
    );
    
    expect(screen.getByText(/90%/)).toBeInTheDocument();
  });
});
