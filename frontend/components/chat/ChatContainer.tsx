'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  Mic,
  MicOff,
  Loader2,
  Sparkles,
  Zap,
  MessageSquare,
  Plus,
  Trash2,
  Menu,
  X,
  MessageCircle,
  Smile,
  Frown,
  Meh,
  Heart,
  ThumbsUp,
  Languages,
  Camera
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import MessageBubble, { Message } from './MessageBubble';
import RecommendationCard from './RecommendationCard';
import FaceCapture from './FaceCapture';
import { analyzeText, checkHealth, analyzeImage } from '@/lib/api';

// Chat history item
interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [aiAvailable, setAiAvailable] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatHistory, setChatHistory] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  // Language toggle: 'en' = English, 'my' = Myanmar
  const [inputLanguage, setInputLanguage] = useState<'en' | 'my'>('en');
  // Detection method: 'vader', 'hmm', or 'lmm'
  const [detectionMethod, setDetectionMethod] = useState<'vader' | 'hmm' | 'lmm'>('vader');
  const [showCamera, setShowCamera] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom
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
      })
      .catch(() => {
        setAiAvailable(false);
      });

    // Setup speech recognition
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.lang = inputLanguage === 'my' ? 'my-MM' : 'en-US';
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

    // Create initial chat session
    createNewChat();
  }, []);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [inputText]);

  // Create new chat session
  const createNewChat = () => {
    const newChat: ChatSession = {
      id: Date.now().toString(),
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
    };
    setChatHistory((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
    setMessages([]);
  };

  // Delete chat session
  const deleteChat = (chatId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setChatHistory((prev) => prev.filter((chat) => chat.id !== chatId));
    if (currentChatId === chatId) {
      createNewChat();
    }
  };

  // Load chat session
  const loadChat = (chatId: string) => {
    const chat = chatHistory.find((c) => c.id === chatId);
    if (chat) {
      setCurrentChatId(chatId);
      setMessages(chat.messages);
    }
  };

  // Save current chat to history
  const saveChat = () => {
    if (!currentChatId) return;

    setChatHistory((prev) =>
      prev.map((chat) =>
        chat.id === currentChatId
          ? {
            ...chat,
            messages,
            title: messages[0]?.text?.slice(0, 30) + '...' || 'New Conversation',
          }
          : chat
      )
    );
  };

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
      // Call API with selected method
      const result = await analyzeText(
        messageText,
        true,
        inputLanguage === 'my' ? 'lmm' : detectionMethod
      );

      // Debug: Log the full API response
      console.log('=== API Response ===');
      console.log('result.multi_source:', result.multi_source);
      console.log('result.external_resources:', result.external_resources);

      // Add bot response with emotion
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: result.text,
        emotion: result.emotion,
        confidence: result.confidence,
        emoji: result.emoji,
        color: result.color,
        method: result.method,
        language: result.language,
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
          count: result.count,
          multi_source: result.multi_source,
          external_resources: result.external_resources,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, recMessage]);
      }

      // Save to history
      setTimeout(saveChat, 1000);
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

  // Handle facial emotion detection
  const handleCapture = async (imageBase64: string) => {
    setShowCamera(false);
    setIsLoading(true);

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputLanguage === 'my' ? "[ဓာတ်ပုံမှ တစ်ဆင့် ခံစားချက်ကို စစ်ဆေးနေသည်...]" : "[Analyzing emotion from photo...]",
      type: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const result = await analyzeImage(imageBase64, inputLanguage);

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: result.text,
        type: 'bot',
        timestamp: new Date(),
        emotion: result.emotion,
        confidence: result.confidence,
        emoji: result.emoji,
        color: result.color,
        method: result.method,
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
      console.error('Image analysis error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'error',
        text: inputLanguage === 'my'
          ? "မျက်နှာကို သေချာ မတွေ့ရပါဘူးဗျ။ ပြန်ရိုက်ကြည့်ပေးပါလား။"
          : "Could not detect a face clearly. Please try again with better lighting.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleListening = () => {
    if (recognitionRef.current) {
      // Update language before starting
      recognitionRef.current.lang = inputLanguage === 'my' ? 'my-MM' : 'en-US';
    }
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
  };

  // Toggle between English and Myanmar input language
  const toggleLanguage = () => {
    setInputLanguage((prev) => (prev === 'en' ? 'my' : 'en'));
    if (recognitionRef.current) {
      recognitionRef.current.lang = inputLanguage === 'en' ? 'my-MM' : 'en-US';
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-white">
      {/* Sidebar - ChatGPT Style */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 280, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="bg-slate-900 flex-shrink-0 overflow-hidden"
          >
            <div className="flex flex-col h-full p-3">
              {/* New Chat Button */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={createNewChat}
                className="flex items-center gap-3 px-4 py-3 mb-4 text-white border border-slate-700 rounded-xl hover:bg-slate-800 transition-colors"
              >
                <Plus className="w-5 h-5" />
                <span className="text-sm font-medium">New chat</span>
              </motion.button>

              {/* Chat History */}
              <div className="flex-1 overflow-y-auto space-y-2">
                <p className="text-xs text-slate-500 px-3 mb-2">Recent Conversations</p>
                {chatHistory.map((chat) => (
                  <motion.div
                    key={chat.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    whileHover={{ backgroundColor: 'rgba(255,255,255,0.1)' }}
                    onClick={() => loadChat(chat.id)}
                    className={`group flex items-center gap-3 px-3 py-3 rounded-xl cursor-pointer transition-colors ${currentChatId === chat.id ? 'bg-slate-800' : ''
                      }`}
                  >
                    <MessageSquare className="w-4 h-4 text-slate-400" />
                    <span className="text-sm text-slate-300 flex-1 truncate">
                      {chat.title}
                    </span>
                    <button
                      onClick={(e) => deleteChat(chat.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-slate-700 rounded transition-all"
                    >
                      <Trash2 className="w-4 h-4 text-slate-400" />
                    </button>
                  </motion.div>
                ))}
              </div>

              {/* User Profile */}
              <div className="pt-3 border-t border-slate-800">
                <div className="flex items-center gap-3 px-3 py-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    U
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white">User</p>
                    <p className="text-xs text-slate-500">Free Plan</p>
                  </div>
                </div>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="hover:bg-slate-100"
            >
              {sidebarOpen ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
            </Button>
            <div>
              <h2 className="text-lg font-semibold text-slate-800">Emotion-Aware AI</h2>
              {/* <p className="text-xs text-slate-500 flex items-center gap-1.5">
                <span className={`w-2 h-2 rounded-full ${aiAvailable ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'}`}></span>
                {aiAvailable ? 'Groq AI Powered' : 'Rule-based mode'}
              </p> */}
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Method Switcher - Only for English */}
            {inputLanguage === 'en' && (
              <div className="hidden md:flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 mr-2">
                {(['vader', 'hmm', 'lmm'] as const).map((m) => (
                  <button
                    key={m}
                    onClick={() => setDetectionMethod(m)}
                    className={`px-2 py-1 text-[10px] font-bold rounded-md transition-all ${detectionMethod === m
                      ? 'bg-white text-indigo-600 shadow-sm'
                      : 'text-slate-500 hover:text-slate-700'
                      }`}
                  >
                    {m.toUpperCase()}
                  </button>
                ))}
              </div>
            )}

            {/* Language Toggle Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleLanguage}
              title={inputLanguage === 'en' ? 'Switch to Myanmar' : 'Switch to English'}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border transition-all ${inputLanguage === 'my'
                ? 'bg-amber-50 border-amber-300 text-amber-700'
                : 'bg-slate-50 border-slate-300 text-slate-600 hover:bg-slate-100'
                }`}
            >
              <Languages className="w-4 h-4" />
              <span>{inputLanguage === 'my' ? '🇲🇲 မြန်မာ' : '🇺🇸 English'}</span>
            </motion.button>



          </div>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto bg-white">
          <div className="p-6 h-full">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center">
                {/* ChatGPT-style Welcome */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center max-w-2xl"
                >
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-xl">
                    <MessageCircle className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-3">
                    How can I help you today?
                  </h3>
                  <p className="text-slate-600 mb-8 leading-relaxed">
                    I can detect your emotions and provide personalized recommendations.
                    Try sharing how you're feeling!
                  </p>

                  {/* Example Prompts Grid — language-aware */}
                  {inputLanguage === 'my' ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {[
                        { emoji: '😊', text: 'ဒီနေ့ တော်တော် ပျော်တယ်!', emotion: 'ပျော်ရွှင်မှု' },
                        { emoji: '😠', text: 'ဒေါသ တော်တော် ဖြစ်နေတယ်', emotion: 'ဒေါသ' },
                        { emoji: '😢', text: 'ဝမ်းနည်းနေတယ်...', emotion: 'ဝမ်းနည်းမှု' },
                        { emoji: '😨', text: 'ကြောက်နေမိတယ်', emotion: 'ကြောက်ရွံ့မှု' },
                      ].map((example, index) => (
                        <motion.button
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          whileHover={{ scale: 1.02, y: -2 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => handleSend(example.text)}
                          className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-left hover:border-amber-400 hover:bg-amber-100 hover:shadow-md transition-all duration-200 group"
                        >
                          <div className="flex items-start gap-3">
                            <span className="text-2xl">{example.emoji}</span>
                            <div>
                              <p className="text-sm font-medium text-slate-700 group-hover:text-amber-700">
                                {example.text}
                              </p>
                              <p className="text-xs text-slate-500 mt-1">{example.emotion}</p>
                            </div>
                          </div>
                        </motion.button>
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {[
                        { emoji: '😊', text: "I just got amazing news!", emotion: 'Share joy' },
                        { emoji: '😠', text: "This is so frustrating!", emotion: 'Express anger' },
                        { emoji: '😢', text: "I'm feeling down today", emotion: 'Need support' },
                        { emoji: '😨', text: "I'm worried about something", emotion: 'Share fear' },
                      ].map((example, index) => (
                        <motion.button
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          whileHover={{ scale: 1.02, y: -2 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => handleSend(example.text)}
                          className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-left hover:border-indigo-300 hover:bg-indigo-50 hover:shadow-md transition-all duration-200 group"
                        >
                          <div className="flex items-start gap-3">
                            <span className="text-2xl">{example.emoji}</span>
                            <div>
                              <p className="text-sm font-medium text-slate-700 group-hover:text-indigo-600">
                                {example.text}
                              </p>
                              <p className="text-xs text-slate-500 mt-1">{example.emotion}</p>
                            </div>
                          </div>
                        </motion.button>
                      ))}
                    </div>
                  )}
                </motion.div>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto space-y-6">
                <AnimatePresence>
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      {message.type === 'recommendation' ? (
                        <RecommendationCard
                          emotion={message.emotion!}
                          color={message.color!}
                          recommendations={message.recommendations!}
                          source={message.source}
                          multi_source={message.multi_source}
                          external_resources={message.external_resources}
                        />
                      ) : (
                        <MessageBubble message={message} />
                      )}
                    </motion.div>
                  ))}
                </AnimatePresence>

                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center gap-3"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
                      <Loader2 className="w-4 h-4 text-white animate-spin" />
                    </div>
                    <div className="flex items-center gap-1">
                      <span className="text-sm text-slate-600">Analyzing</span>
                      <span className="flex gap-1">
                        <motion.span
                          animate={{ opacity: [0.3, 1, 0.3] }}
                          transition={{ duration: 1.5, repeat: Infinity }}
                          className="w-1.5 h-1.5 bg-indigo-600 rounded-full"
                        ></motion.span>
                        <motion.span
                          animate={{ opacity: [0.3, 1, 0.3] }}
                          transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
                          className="w-1.5 h-1.5 bg-indigo-600 rounded-full"
                        ></motion.span>
                        <motion.span
                          animate={{ opacity: [0.3, 1, 0.3] }}
                          transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
                          className="w-1.5 h-1.5 bg-indigo-600 rounded-full"
                        ></motion.span>
                      </span>
                    </div>
                  </motion.div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-slate-200 p-4 bg-white">
          <div className="max-w-3xl mx-auto">
            <div className="relative flex items-end gap-2 bg-slate-50 border border-slate-300 rounded-2xl p-2 shadow-sm focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-200 transition-all">
              <Button
                onClick={() => setShowCamera(true)}
                className="w-12 h-12 rounded-2xl bg-white border-gray-200 text-gray-500 hover:text-indigo-500 hover:bg-indigo-50 transition-all shadow-sm flex items-center justify-center p-0"
              >
                <Camera className="w-6 h-6" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleListening}
                className={`shrink-0 rounded-xl ${isListening
                  ? 'bg-red-100 hover:bg-red-200 text-red-600'
                  : 'hover:bg-slate-200'
                  }`}
                disabled={isLoading}
              >
                {isListening ? (
                  <MicOff className="w-5 h-5" />
                ) : (
                  <Mic className="w-5 h-5" />
                )}
              </Button>

              <textarea
                ref={textareaRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                  inputLanguage === 'my'
                    ? 'ခံစားချက်တွေ ပြောပြပါ... (မြန်မာဘာသာ)'
                    : "Share how you're feeling..."
                }
                disabled={isLoading || isListening}
                rows={1}
                className="flex-1 bg-transparent border-0 focus:ring-0 resize-none py-3 px-2 text-slate-800 placeholder:text-slate-400 max-h-[200px]"
                style={{ minHeight: '44px' }}
              />

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  onClick={() => handleSend()}
                  disabled={isLoading || !inputText.trim()}
                  className={`shrink-0 rounded-xl h-11 w-11 p-0 ${inputText.trim()
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg'
                    : 'bg-slate-300'
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
                  <span className="text-sm text-red-700 font-medium">
                    Listening... Click mic to stop
                  </span>
                </div>
              </motion.div>
            )}

            <p className="text-xs text-center text-slate-500 mt-3">
              {inputLanguage === 'my'
                ? 'မြန်မာဘာသာ ✦ English — ကြွေးကြော်ဖော်ပြချက်များ မှားနိုင်ပါသည်'
                : 'Emotion-Aware AI can make mistakes. Consider checking important information.'}
            </p>
          </div>
        </div>
      </main>

      {/* Camera Modal */}
      {showCamera && (
        <FaceCapture
          onCapture={handleCapture}
          onClose={() => setShowCamera(false)}
          language={inputLanguage}
        />
      )}
    </div>
  );
}
