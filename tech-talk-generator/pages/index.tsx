"use client"

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';

export default function Home() {
    const [topic, setTopic] = useState<string>('');
    const [ideas, setIdeas] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const generateIdeas = () => {
        if (!topic.trim()) return;
        
        setIsLoading(true);
        setIdeas('');
        
        const evt = new EventSource(`/api?topic=${encodeURIComponent(topic)}`);
        let buffer = '';

        evt.onmessage = (e) => {
            buffer += e.data;
            setIdeas(buffer);
        };
        
        evt.onerror = () => {
            evt.close();
            setIsLoading(false);
        };
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            generateIdeas();
        }
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
            <div className="container mx-auto px-4 py-12">
                {/* Header */}
                <header className="text-center mb-12">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                        Tech Talk Idea Generator
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400 text-lg">
                        Enter a topic to get AI-powered tech talk ideas for your summit
                    </p>
                </header>

                {/* Input Section */}
                <div className="max-w-3xl mx-auto mb-8">
                    <div className="flex gap-4">
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Enter a topic (e.g., AI in DevOps, Cloud Security, MLOps)"
                            className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <button
                            onClick={generateIdeas}
                            disabled={isLoading || !topic.trim()}
                            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            {isLoading ? 'Generating...' : 'Generate Ideas'}
                        </button>
                    </div>
                </div>

                {/* Content Card */}
                <div className="max-w-3xl mx-auto">
                    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-lg bg-opacity-95">
                        {!ideas && !isLoading ? (
                            <div className="flex items-center justify-center py-12">
                                <div className="text-gray-400 text-center">
                                    <p className="text-lg">Enter a topic above to generate tech talk ideas</p>
                                    <p className="text-sm mt-2">Try: "AI in DevOps", "Kubernetes Best Practices", "GenAI for Developers"</p>
                                </div>
                            </div>
                        ) : isLoading && !ideas ? (
                            <div className="flex items-center justify-center py-12">
                                <div className="animate-pulse text-gray-400">
                                    Generating tech talk ideas...
                                </div>
                            </div>
                        ) : (
                            <div className="markdown-content text-gray-700 dark:text-gray-300">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm, remarkBreaks]}
                                >
                                    {ideas}
                                </ReactMarkdown>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
}
