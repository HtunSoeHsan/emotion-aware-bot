'use client';

import { motion } from 'framer-motion';
import { format } from 'date-fns';

export interface Message {
  id: string;
  type: 'user' | 'bot' | 'error' | 'recommendation';
  text?: string;
  emotion?: string;
  confidence?: number;
  emoji?: string;
  color?: string;
  recommendations?: {
    type: string;
    label: string;
    text: string;
  }[];
  source?: 'ai' | 'rules';
  count?: number;
  timestamp: Date;
}

interface MessageBubbleProps {
  message: Message;
}

const emotionColors: Record<string, string> = {
  joy: 'from-green-400 to-emerald-500',
  anger: 'from-red-400 to-rose-500',
  sadness: 'from-blue-400 to-sky-500',
  fear: 'from-purple-400 to-violet-500',
  neutral: 'from-gray-400 to-slate-500',
};

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.type === 'user';
  const isError = message.type === 'error';

  if (isError) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-center my-4"
      >
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm shadow-sm">
          <span className="flex items-center gap-2">
            <span>⚠️</span>
            <span className="font-medium">{message.text}</span>
          </span>
        </div>
      </motion.div>
    );
  }

  if (isUser) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex justify-end my-4"
      >
        <div className="flex items-end gap-3 max-w-[85%] flex-row-reverse">
          {/* User Avatar */}
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center text-white text-xs font-bold shadow-md">
            U
          </div>
          
          {/* Message Bubble */}
          <div className="bg-slate-900 text-white px-5 py-3.5 rounded-2xl rounded-br-sm shadow-lg">
            <p className="text-sm leading-relaxed">{message.text}</p>
            <p className="text-xs text-slate-400 mt-1.5">
              {format(new Date(message.timestamp), 'HH:mm')}
            </p>
          </div>
        </div>
      </motion.div>
    );
  }

  // Bot message with emotion
  const gradientClass = message.color
    ? emotionColors[message.emotion!] || emotionColors.neutral
    : 'from-gray-400 to-slate-500';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex justify-start my-4"
    >
      <div className="flex items-end gap-3 max-w-[85%]">
        {/* Bot Avatar */}
        <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-xs shadow-md flex-shrink-0">
          🧠
        </div>
        
        {/* Message Content */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-sm font-semibold text-slate-800">EmotionBot</span>
          </div>
          
          <div className="bg-slate-50 border border-slate-200 px-5 py-3.5 rounded-2xl rounded-tl-sm shadow-sm">
            {message.text && (
              <p className="text-slate-800 text-sm mb-3 leading-relaxed">{message.text}</p>
            )}

            {message.emotion && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r ${gradientClass} text-white text-xs font-semibold shadow-md`}
              >
                <span>{message.emoji}</span>
                <span className="capitalize">{message.emotion}</span>
                {message.confidence && (
                  <span className="opacity-90 text-[10px]">
                    ({Math.round(message.confidence * 100)}% match)
                  </span>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
