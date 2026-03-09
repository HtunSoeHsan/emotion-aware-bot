"use client";
import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Loader2, Sparkles, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import MessageBubble, { Message } from './MessageBubble';
import RecommendationCard from './RecommendationCard';
import { analyzeText, checkHealth } from '@/lib/api';

export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [aiAvailable, setAiAvailable] = useState(true);
  const [useAI, setUseAI] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check API health on mount
  useEffect(() => {
    checkHealth()
      .then((health) => {
        setAiAvailable(health.ai_available);
        setUseAI(health.ai_available);
      })
      .catch(() => {
        setAiAvailable(false);
        setUseAI(false);
      });

    // Setup speech recognition
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.lang = 'en-US';
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onstart = () => setIsListening(true);
      recognitionRef.current.onend = () => setIsListening(false);
      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        handleSend(transcript);
      };
      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
    }
  }, []);

  const handleSend = async (text?: string) => {
    const messageText = text || inputText.trim();
    if (!messageText || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      text: messageText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call API
      const result = await analyzeText(messageText, useAI);

      // Add bot response with emotion
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: result.text,
        emotion: result.emotion,
        confidence: result.confidence,
        emoji: result.emoji,
        color: result.color,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);

      // Add recommendation card
      if (result.recommendations) {
        const recMessage: Message = {
          id: (Date.now() + 2).toString(),
          type: 'recommendation',
          emotion: result.emotion,
          color: result.color,
          recommendations: result.recommendations,
          source: result.source,
          multi_source: result.multi_source,
          external_resources: result.external_resources,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, recMessage]);
      }
    } catch (error) {
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'error',
        text: error instanceof Error ? error.message : 'Failed to analyze emotion',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-200"
    >
      {/* Chat Header - Enhanced with glassmorphism */}
      <div className="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 px-6 py-4 overflow-hidden">
        {/* Animated background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-40 h-40 bg-white rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>
          <div className="absolute bottom-0 right-0 w-40 h-40 bg-white rounded-full blur-3xl translate-x-1/2 translate-y-1/2 animate-pulse delay-1000"></div>
        </div>
        
        <div className="relative flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-white/20 backdrop-blur-sm rounded-xl">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-white font-semibold text-lg">EmotionBot</h2>
              <p className="text-indigo-100 text-xs flex items-center gap-1.5">
                <span className={`w-2 h-2 rounded-full ${aiAvailable ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'}`}></span>
                {aiAvailable ? 'AI-powered recommendations active' : 'Rule-based mode'}
              </p>
            </div>
          </div>
          
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setUseAI(!useAI)}
              className="text-white hover:bg-white/20 backdrop-blur-sm border border-white/20"
              disabled={!aiAvailable}
            >
              {useAI ? (
                <>
                  <Sparkles className="w-4 h-4 mr-1.5" />
                  <span className="hidden sm:inline">AI On</span>
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 mr-1.5" />
                  <span className="hidden sm:inline">Rules</span>
                </>
              )}
            </Button>
          </motion.div>
        </div>
      </div>

      {/* Messages Area - Enhanced */}
      <div className="h-[550px] overflow-y-auto p-6 space-y-4 bg-gradient-to-br from-slate-50 via-white to-indigo-50/30">
        <AnimatePresence mode="wait">
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="text-center py-20"
            >
              {/* Animated Hero Illustration */}
              <div className="relative inline-block mb-6">
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 blur-2xl rounded-full"></div>
                <motion.div 
                  className="relative text-7xl"
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                >
                  🧠
                </motion.div>
              </div>
              
              <h3 className="text-xl font-semibold text-slate-800 mb-3">
                Welcome to Emotion-Aware AI
              </h3>
              <p className="text-slate-600 max-w-md mx-auto mb-8 leading-relaxed">
                I can detect your emotions from text or voice and provide personalized recommendations.
              </p>
              
              {/* Example Prompts */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {[
                  { emoji: '😊', text: "I just got promoted!", emotion: 'Joy' },
                  { emoji: '😠', text: "This is so frustrating!", emotion: 'Anger' },
                  { emoji: '😢', text: "I feel really lonely", emotion: 'Sadness' },
                  { emoji: '😨', text: "I'm worried about tomorrow", emotion: 'Fear' },
                ].map((example, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleSend(example.text)}
                    className="p-4 bg-white border border-slate-200 rounded-xl text-left hover:border-indigo-300 hover:shadow-md transition-all duration-200 group"
                  >
                    <span className="text-2xl mb-1 block">{example.emoji}</span>
                    <p className="text-sm font-medium text-slate-700 group-hover:text-indigo-600">
                      {example.text}
                    </p>
                    <p className="text-xs text-slate-500 mt-1">{example.emotion}</p>
                  </motion.button>
                ))}
              </div>
              
              {/* Voice Input CTA */}
              <div className="mt-8">
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  className="inline-flex items-center gap-2 text-slate-500 text-sm"
                >
                  <Mic className="w-4 h-4" />
                  <span>Or click the microphone to speak</span>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Messages with animations */}
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
            >
              {message.type === 'recommendation' ? (
                <RecommendationCard
                  emotion={message.emotion!}
                  color={message.color!}
                  recommendations={message.recommendations!}
                  multi_source={message.multi_source}
                  external_resources={message.external_resources}
                  source={message.source}
                />
              ) : (
                <MessageBubble message={message} />
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Enhanced Loading State */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-3 text-slate-600"
          >
            <div className="relative">
              <Loader2 className="w-5 h-5 animate-spin text-indigo-600" />
              <div className="absolute inset-0 bg-indigo-600/20 rounded-full animate-ping"></div>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-sm font-medium">Analyzing emotion</span>
              <span className="flex gap-1">
                <motion.span
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="w-1 h-1 bg-indigo-600 rounded-full"
                ></motion.span>
                <motion.span
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
                  className="w-1 h-1 bg-indigo-600 rounded-full"
                ></motion.span>
                <motion.span
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
                  className="w-1 h-1 bg-indigo-600 rounded-full"
                ></motion.span>
              </span>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - Enhanced */}
      <div className="border-t border-slate-200 p-4 bg-white/80 backdrop-blur-sm">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              variant="outline"
              size="icon"
              onClick={toggleListening}
              className={`shrink-0 transition-all duration-300 ${
                isListening 
                  ? 'animate-pulse bg-red-50 border-red-300 shadow-lg shadow-red-200' 
                  : 'hover:bg-slate-50'
              }`}
              disabled={isLoading}
            >
              {isListening ? (
                <MicOff className="w-5 h-5 text-red-500" />
              ) : (
                <Mic className="w-5 h-5 text-slate-600" />
              )}
            </Button>
          </motion.div>

          <div className="flex-1 relative">
            <Input
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isListening ? 'Listening...' : 'Type a message or speak...'}
              disabled={isLoading || isListening}
              className="flex-1 pr-12 transition-all duration-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            {inputText.trim() && (
              <motion.button
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                onClick={() => setInputText('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <span className="text-xs font-medium">✕</span>
              </motion.button>
            )}
          </div>

          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              onClick={() => handleSend()}
              disabled={isLoading || !inputText.trim()}
              className={`shrink-0 transition-all duration-300 ${
                inputText.trim()
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-200'
                  : ''
              }`}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </motion.div>
        </div>
        
        {/* Voice Recording Indicator */}
        {isListening && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-3 text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-red-50 border border-red-200 rounded-full">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-red-700 font-medium">Recording... Click mic to stop</span>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
