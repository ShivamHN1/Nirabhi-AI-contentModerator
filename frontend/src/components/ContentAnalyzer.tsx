/**
 * Content Analyzer Component
 * 
 * This is the main interface where users input text for analysis.
 * It provides real-time feedback, educational insights, and helpful suggestions.
 * 
 * Features:
 * - Real-time text analysis
 * - Beautiful, responsive design
 * - Educational explanations
 * - Supportive suggestions
 * - Accessibility features
 */

import React, { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Loader2, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  Heart,
  Lightbulb,
  Shield,
  Clock,
  BarChart3
} from 'lucide-react';
import axios from 'axios';

interface AnalysisResult {
  text: string;
  toxicity_score: number;
  is_toxic: boolean;
  category: string;
  severity: string;
  sentiment_score: number;
  confidence: number;
  explanation: string;
  suggestions: string[];
  support_resources?: Array<{
    name: string;
    description: string;
    contact: string;
    url: string;
  }>;
  analysis_timestamp: string;
  processing_time_ms: number;
}

interface ContentAnalyzerProps {
  onAnalysisComplete: (result: AnalysisResult) => void;
  darkMode: boolean;
}

const ContentAnalyzer: React.FC<ContentAnalyzerProps> = ({ 
  onAnalysisComplete, 
  darkMode 
}) => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Real-time character count and validation
  const maxLength = 10000;
  const charCount = text.length;
  const isValid = text.trim().length > 0 && charCount <= maxLength;

  const analyzeContent = useCallback(async () => {
    if (!isValid) return;

    setIsAnalyzing(true);
    setError(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/analyze`, {
        text: text.trim(),
        context: 'user_interface',
        user_preferences: null
      });

      const result = response.data;
      setAnalysisResult(result);
      onAnalysisComplete(result);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to analyze content. Please try again.';
      setError(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  }, [text, isValid, onAnalysisComplete]);

  // Handle Enter key to submit
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      analyzeContent();
    }
  };

  // Get toxicity level color and info
  const getToxicityInfo = (score: number) => {
    if (score < 0.3) return { color: 'text-green-500', bg: 'bg-green-100', label: 'Safe', icon: CheckCircle };
    if (score < 0.5) return { color: 'text-yellow-500', bg: 'bg-yellow-100', label: 'Mild', icon: Info };
    if (score < 0.7) return { color: 'text-orange-500', bg: 'bg-orange-100', label: 'Moderate', icon: AlertTriangle };
    return { color: 'text-red-500', bg: 'bg-red-100', label: 'High', icon: AlertTriangle };
  };

  // Get sentiment emoji
  const getSentimentEmoji = (score: number) => {
    if (score > 0.3) return '😊';
    if (score > 0.1) return '😐';
    if (score > -0.3) return '😔';
    return '😢';
  };

  const cardClass = `rounded-xl shadow-lg backdrop-blur-sm transition-all duration-300 ${
    darkMode 
      ? 'bg-gray-800 bg-opacity-50 border border-gray-700' 
      : 'bg-white bg-opacity-70 border border-gray-200'
  }`;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Input Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cardClass}
      >
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-6 w-6 text-blue-500" />
            <h2 className="text-xl font-semibold">Content Analysis</h2>
          </div>
          
          <div className="space-y-4">
            {/* Text input area */}
            <div className="relative">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter the content you'd like to analyze for toxicity, sentiment, and safety..."
                className={`w-full h-32 p-4 rounded-lg border-2 transition-colors resize-none ${
                  darkMode
                    ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500'
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
                } focus:outline-none focus:ring-0`}
                maxLength={maxLength}
              />
              
              {/* Character counter */}
              <div className={`absolute bottom-2 right-2 text-xs ${
                charCount > maxLength * 0.9 ? 'text-red-500' : 'text-gray-400'
              }`}>
                {charCount}/{maxLength}
              </div>
            </div>

            {/* Action buttons */}
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                Press Ctrl+Enter to analyze quickly
              </div>
              
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={analyzeContent}
                disabled={!isValid || isAnalyzing}
                className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
                  isValid && !isAnalyzing
                    ? 'bg-blue-500 hover:bg-blue-600 text-white shadow-lg hover:shadow-xl'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    <span>Analyze Content</span>
                  </>
                )}
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg"
          >
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5" />
              <span>{error}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Analysis Results */}
      <AnimatePresence>
        {analysisResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* Main Results Card */}
            <div className={cardClass}>
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold">Analysis Results</h3>
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <Clock className="h-4 w-4" />
                    <span>{analysisResult.processing_time_ms.toFixed(0)}ms</span>
                  </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  {/* Toxicity Score */}
                  <div className="text-center">
                    <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${getToxicityInfo(analysisResult.toxicity_score).bg} mb-2`}>
                      {React.createElement(getToxicityInfo(analysisResult.toxicity_score).icon, {
                        className: `h-8 w-8 ${getToxicityInfo(analysisResult.toxicity_score).color}`
                      })}
                    </div>
                    <div className="text-2xl font-bold">{(analysisResult.toxicity_score * 100).toFixed(0)}%</div>
                    <div className="text-sm text-gray-500">Toxicity Level</div>
                    <div className={`text-sm font-medium ${getToxicityInfo(analysisResult.toxicity_score).color}`}>
                      {getToxicityInfo(analysisResult.toxicity_score).label}
                    </div>
                  </div>

                  {/* Sentiment */}
                  <div className="text-center">
                    <div className="text-4xl mb-2">{getSentimentEmoji(analysisResult.sentiment_score)}</div>
                    <div className="text-2xl font-bold">
                      {analysisResult.sentiment_score > 0 ? '+' : ''}{(analysisResult.sentiment_score * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-500">Sentiment</div>
                  </div>

                  {/* Confidence */}
                  <div className="text-center">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-2">
                      <BarChart3 className="h-8 w-8 text-blue-500" />
                    </div>
                    <div className="text-2xl font-bold">{(analysisResult.confidence * 100).toFixed(0)}%</div>
                    <div className="text-sm text-gray-500">Confidence</div>
                  </div>
                </div>

                {/* Category and Severity */}
                <div className="flex items-center justify-center space-x-4 mb-6">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    analysisResult.category === 'safe' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {analysisResult.category.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className="text-gray-300">•</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    analysisResult.severity === 'low' ? 'bg-yellow-100 text-yellow-800' :
                    analysisResult.severity === 'medium' ? 'bg-orange-100 text-orange-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {analysisResult.severity.toUpperCase()} SEVERITY
                  </span>
                </div>

                {/* Explanation */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-50'}`}>
                  <div className="flex items-start space-x-3">
                    <Info className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-medium mb-1">Why was this flagged?</h4>
                      <p className="text-sm leading-relaxed">{analysisResult.explanation}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Suggestions */}
            {analysisResult.suggestions.length > 0 && (
              <div className={cardClass}>
                <div className="p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Lightbulb className="h-6 w-6 text-yellow-500" />
                    <h3 className="text-lg font-semibold">Helpful Suggestions</h3>
                  </div>
                  <div className="space-y-3">
                    {analysisResult.suggestions.map((suggestion, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className={`p-3 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-green-50'} border-l-4 border-green-500`}
                      >
                        <p className="text-sm">{suggestion}</p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Support Resources */}
            {analysisResult.support_resources && analysisResult.support_resources.length > 0 && (
              <div className={cardClass}>
                <div className="p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Heart className="h-6 w-6 text-pink-500" />
                    <h3 className="text-lg font-semibold">Support Resources</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-4">
                    If you or someone you know needs support, these resources are available 24/7:
                  </p>
                  <div className="space-y-3">
                    {analysisResult.support_resources.map((resource, index) => (
                      <div key={index} className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-blue-50'}`}>
                        <h4 className="font-medium text-blue-700">{resource.name}</h4>
                        <p className="text-sm text-gray-600 mb-2">{resource.description}</p>
                        <div className="text-sm">
                          <span className="font-medium">Contact: </span>
                          <span>{resource.contact}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ContentAnalyzer;
