import React from 'react';
import { Toaster } from 'react-hot-toast';
import ContentAnalyzer from './components/ContentAnalyzer';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900">🛡️ Nirabhi</h1>
          <p className="text-gray-600">Content Moderator</p>
        </header>

        <main>
          <ContentAnalyzer />
        </main>

        <footer className="mt-8 text-center text-sm text-gray-500">
          <p>Making digital spaces safer</p>
        </footer>
      </div>
      <Toaster position="bottom-right" />
    </div>
  );
}

export default App;
