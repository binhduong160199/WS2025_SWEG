/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TextSuggestions from '../TextSuggestions';

describe('TextSuggestions Component', () => {
  test('renders suggestions when provided', () => {
    const generatedText = JSON.stringify({
      suggestions: ['Great post!', 'Well said!']
    });
    
    render(
      <TextSuggestions 
        generatedText={generatedText} 
        processingStatus="completed"
      />
    );
    
    const toggleBtn = screen.getByText(/Suggestions/i);
    expect(toggleBtn).toBeInTheDocument();
  });

  test('expands and collapses suggestions', () => {
    const generatedText = JSON.stringify({
      suggestions: ['Suggestion 1', 'Suggestion 2']
    });
    
    render(
      <TextSuggestions 
        generatedText={generatedText} 
        processingStatus="completed"
      />
    );
    
    const toggleBtn = screen.getByText(/Suggestions/i);
    
    // Initially collapsed
    expect(screen.queryByText('Suggestion 1')).not.toBeInTheDocument();
    
    // Click to expand
    fireEvent.click(toggleBtn);
    expect(screen.getByText('Suggestion 1')).toBeInTheDocument();
    expect(screen.getByText('Suggestion 2')).toBeInTheDocument();
    
    // Click to collapse
    fireEvent.click(toggleBtn);
    expect(screen.queryByText('Suggestion 1')).not.toBeInTheDocument();
  });

  test('renders loading state during processing', () => {
    render(
      <TextSuggestions 
        generatedText={null} 
        processingStatus="processing"
      />
    );
    
    expect(screen.getByText(/Generating suggestions/i)).toBeInTheDocument();
  });

  test('returns null when no suggestions and not processing', () => {
    const { container } = render(
      <TextSuggestions 
        generatedText={null} 
        processingStatus="completed"
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  test('handles copy button click', async () => {
    const generatedText = JSON.stringify({
      suggestions: ['Copy me!']
    });
    
    // Mock clipboard API
    Object.assign(navigator, {
      clipboard: {
        writeText: jest.fn(() => Promise.resolve()),
      },
    });
    
    render(
      <TextSuggestions 
        generatedText={generatedText} 
        processingStatus="completed"
      />
    );
    
    const toggleBtn = screen.getByText(/Suggestions/i);
    fireEvent.click(toggleBtn);
    
    const copyBtn = screen.getByText('Copy');
    fireEvent.click(copyBtn);
    
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Copy me!');
  });

  test('handles JSON parsing of generated text', () => {
    const generatedText = JSON.stringify({
      suggestions: ['First', 'Second', 'Third']
    });
    
    render(
      <TextSuggestions 
        generatedText={generatedText} 
        processingStatus="completed"
      />
    );
    
    const toggleBtn = screen.getByText(/Suggestions \(3\)/i);
    expect(toggleBtn).toBeInTheDocument();
  });
});
