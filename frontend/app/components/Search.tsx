'use client';

import { useState } from 'react';
import { api, SearchResult } from '@/lib/api';

interface SearchProps {
  onSelectResult?: (result: SearchResult) => void;
}

export default function Search({ onSelectResult }: SearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isSearching) return;

    setIsSearching(true);
    setHasSearched(true);

    try {
      const searchResults = await api.search(query, 20);
      setResults(searchResults);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search code..."
          className="flex-1 bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={isSearching || !query.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded font-medium transition"
        >
          {isSearching ? '...' : 'Search'}
        </button>
      </form>

      {hasSearched && (
        <div className="space-y-2">
          {results.length === 0 ? (
            <p className="text-gray-400 text-center py-4">No results found</p>
          ) : (
            <>
              <p className="text-sm text-gray-400">{results.length} results</p>
              {results.map((result, index) => (
                <div
                  key={index}
                  onClick={() => onSelectResult?.(result)}
                  className="bg-gray-800 rounded p-3 border border-gray-700 hover:border-blue-500 cursor-pointer transition"
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-blue-400 text-sm font-mono">
                      {result.file_path}:{result.line_start}-{result.line_end}
                    </span>
                    <span className="text-xs px-2 py-0.5 bg-gray-700 rounded text-gray-300">
                      {result.language}
                    </span>
                  </div>
                  <pre className="text-xs text-gray-300 overflow-hidden whitespace-pre-wrap font-mono">
                    {result.preview}
                  </pre>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
