'use client';

import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Send, Footprints, Lightbulb, Sparkles, Check, Copy } from 'lucide-react';
import { useState } from 'react';

interface RecommendationCardProps {
  emotion: string;
  color: string;
  recommendations: {
    type: string;
    label: string;
    text: string;
  }[];
  source?: 'ai' | 'rules';
  count?: number;
}

const emotionIcons: Record<string, string> = {
  joy: '😊',
  anger: '😠',
  sadness: '😢',
  fear: '😨',
  neutral: '😐',
};

const colorClasses: Record<string, string> = {
  green: 'from-green-500 to-emerald-600 border-green-200 bg-green-50',
  red: 'from-red-500 to-rose-600 border-red-200 bg-red-50',
  blue: 'from-blue-500 to-sky-600 border-blue-200 bg-blue-50',
  purple: 'from-purple-500 to-violet-600 border-purple-200 bg-purple-50',
  gray: 'from-gray-500 to-slate-600 border-gray-200 bg-gray-50',
};

export default function RecommendationCard({
  emotion,
  color,
  recommendations,
  source,
  count,
}: RecommendationCardProps) {
  const gradientClass = colorClasses[color] || colorClasses.gray;
  const emoji = emotionIcons[emotion] || '🤔';
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const handleCopy = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(index);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Handle both old and new format
  const recsArray = Array.isArray(recommendations) ? recommendations : [];
  
  // Separate messages and actions
  const messages = recsArray.filter((r: any) => r.type === 'message');
  const actions = recsArray.filter((r: any) => r.type === 'action');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="flex justify-center my-4"
    >
      <Card className={`w-full max-w-2xl border-2 ${gradientClass} shadow-xl hover:shadow-2xl transition-shadow duration-300`}>
        <CardHeader className="pb-3 border-b border-slate-200/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <motion.span 
                className="text-3xl"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                {emoji}
              </motion.span>
              <div>
                <h3 className="font-semibold text-slate-800 capitalize text-lg">
                  {emotion} Detected
                </h3>
                <p className="text-xs text-slate-600 flex items-center gap-1.5">
                  {source === 'ai' ? (
                    <>
                      <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                      <span className="font-medium">AI-Powered Recommendations ({count || recommendations.length} suggestions)</span>
                    </>
                  ) : (
                    <>
                      <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
                      <span className="font-medium">Smart Recommendations ({count || recommendations.length} suggestions)</span>
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-4">
          {/* Messages Section */}
          {messages.length > 0 && (
            <div className="mb-4">
              <h4 className="text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wide flex items-center gap-2">
                <Send className="w-3.5 h-3.5 text-indigo-600" />
                Messages to Send ({messages.length})
              </h4>
              <div className="grid gap-2">
                {messages.map((rec, index) => (
                  <motion.div
                    key={`msg-${index}`}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-indigo-50/80 backdrop-blur-sm rounded-xl p-3 border border-indigo-100 hover:border-indigo-300 transition-all duration-200"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-indigo-700 mb-1">
                          {rec.label}
                        </p>
                        <p className="text-sm text-slate-800 italic leading-relaxed">
                          "{rec.text}"
                        </p>
                      </div>
                      <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCopy(rec.text, index)}
                          className={`h-8 text-xs font-medium transition-all duration-200 ${
                            copiedId === index
                              ? 'bg-green-100 text-green-700'
                              : 'hover:bg-indigo-100 hover:text-indigo-700'
                          }`}
                        >
                          {copiedId === index ? (
                            <>
                              <Check className="w-3.5 h-3.5 mr-1" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-3.5 h-3.5 mr-1" />
                              Copy
                            </>
                          )}
                        </Button>
                      </motion.div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Actions Section */}
          {actions.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wide flex items-center gap-2">
                <Footprints className="w-3.5 h-3.5 text-emerald-600" />
                Self-Care Actions ({actions.length})
              </h4>
              <div className="grid gap-2">
                {actions.map((rec, index) => (
                  <motion.div
                    key={`act-${index}`}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: (messages.length + index) * 0.1 }}
                    className="bg-emerald-50/80 backdrop-blur-sm rounded-xl p-3 border border-emerald-100 hover:border-emerald-300 transition-all duration-200"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-100 shrink-0">
                        <Footprints className="w-4 h-4 text-emerald-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-emerald-700 mb-1">
                          {rec.label}
                        </p>
                        <p className="text-sm text-slate-800 leading-relaxed">
                          {rec.text}
                        </p>
                      </div>
                      <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCopy(rec.text, messages.length + index)}
                          className={`h-8 text-xs font-medium transition-all duration-200 ${
                            copiedId === messages.length + index
                              ? 'bg-green-100 text-green-700'
                              : 'hover:bg-emerald-100 hover:text-emerald-700'
                          }`}
                        >
                          {copiedId === messages.length + index ? (
                            <>
                              <Check className="w-3.5 h-3.5 mr-1" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-3.5 h-3.5 mr-1" />
                              Copy
                            </>
                          )}
                        </Button>
                      </motion.div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
