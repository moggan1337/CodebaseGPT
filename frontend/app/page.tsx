'use client';

import { useState, useRef, useEffect } from 'react';
import { api, QueryResponse, Citation } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  thinking?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [indexStatus, setIndexStatus] = useState<string>('');
  const [codebasePath, setCodebasePath] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleIndex = async () => {
    if (!codebasePath.trim()) return;
    
    setIsLoading(true);
    setIndexStatus('Indexing...');
    
    try {
      const result = await api.indexLocal(codebasePath);
      setIndexStatus(`✅ Indexed ${result.chunks_indexed} chunks from ${result.files_processed} files`);
    } catch (error) {
      setIndexStatus(`❌ Error: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const question = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setIsLoading(true);

    try {
      const response = await api.query(question, true);
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        thinking: response.thinking
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-white">🤖 CodebaseGPT</h1>
          <p className="text-gray-400 text-sm mt-1">
            Chat with your codebase - Ask questions, get answers with citations
          </p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6">
        {/* Index Section */}
        <div className="mb-6 bg-gray-800 rounded-lg p-4 border border-gray-700">
          <h2 className="text-lg font-semibold mb-3">📂 Index Codebase</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={codebasePath}
              onChange={(e) => setCodebasePath(e.target.value)}
              placeholder="/path/to/your/codebase"
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleIndex}
              disabled={isLoading || !codebasePath.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-2 rounded font-medium transition"
            >
              {isLoading ? 'Indexing...' : 'Index'}
            </button>
          </div>
          {indexStatus && (
            <p className="mt-2 text-sm text-gray-400">{indexStatus}</p>
          )}
        </div>

        {/* Chat Messages */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 mb-6">
          <div className="h-96 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-20">
                <p className="text-4xl mb-4">💬</p>
                <p>Ask me anything about your codebase!</p>
                <p className="text-sm mt-2">
                  Example: &quot;How does authentication work?&quot; or &quot;Where is the user model?&quot;
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-100'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  
                  {/* Citations */}
                  {message.citations && message.citations.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-600">
                      <p className="text-xs font-semibold text-gray-300 mb-2">📚 Citations:</p>
                      {message.citations.slice(0, 5).map((citation, i) => (
                        <div key={i} className="text-xs bg-gray-800 rounded p-2 mt-1">
                          <span className="text-blue-400">{citation.file_path}:{citation.line_number}</span>
                          <code className="block text-gray-400 mt-1 truncate">
                            {citation.snippet.slice(0, 100)}...
                          </code>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {/* Thinking */}
                  {message.thinking && (
                    <details className="mt-2">
                      <summary className="text-xs cursor-pointer text-gray-400 hover:text-gray-300">
                        🤔 View thinking
                      </summary>
                      <pre className="mt-2 text-xs bg-gray-900 p-2 rounded overflow-x-auto text-gray-400">
                        {message.thinking.slice(0, 500)}...
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-700 rounded-lg px-4 py-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about your codebase..."
                disabled={isLoading}
                className="flex-1 bg-gray-700 border border-gray-600 rounded px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded font-medium transition"
              >
                Send
              </button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <footer className="text-center text-gray-500 text-sm">
          <p>
            Built with MiniMax M2.7 • Source on{' '}
            <a href="https://github.com/moggan1337/CodebaseGPT" className="text-blue-400 hover:underline">
              GitHub
            </a>
          </p>
        </footer>
      </main>
    </div>
  );
}
