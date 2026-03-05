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
    send_message: string;
    action: string;
  };
  source?: 'ai' | 'rules';
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
        className="flex justify-center"
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
        initial={{ opacity: 0, x: 20, scale: 0.95 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="flex justify-end"
      >
        <div className="max-w-[80%] bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 text-white px-5 py-3.5 rounded-2xl rounded-br-sm shadow-lg shadow-indigo-200/50">
          <p className="text-sm leading-relaxed">{message.text}</p>
          <p className="text-xs text-indigo-100 mt-1.5 flex items-center gap-1">
            <span>{format(new Date(message.timestamp), 'HH:mm')}</span>
            <span>•</span>
            <span>Delivered</span>
          </p>
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
      initial={{ opacity: 0, x: -20, scale: 0.95 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="flex justify-start"
    >
      <div className="max-w-[85%]">
        <div className="flex items-center gap-2.5 mb-1.5">
          <motion.span
            className="text-3xl"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 500, delay: 0.1 }}
          >
            {message.emoji || '🤖'}
          </motion.span>
          <span className="text-sm font-semibold text-slate-700">EmotionBot</span>
        </div>
        <div className="bg-white border border-slate-200 px-5 py-3.5 rounded-2xl rounded-bl-sm shadow-md">
          {message.text && <p className="text-slate-800 text-sm mb-2.5 leading-relaxed">{message.text}</p>}

          {message.emotion && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-full bg-gradient-to-r ${gradientClass} text-white text-xs font-semibold shadow-md`}
            >
              <span>{message.emoji}</span>
              <span className="capitalize">{message.emotion}</span>
              {message.confidence && (
                <span className="opacity-90 text-[10px]">({Math.round(message.confidence * 100)}% match)</span>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
