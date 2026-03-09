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
    send_message: string;
    action: string;
  };
  source?: 'ai' | 'rules';
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
}: RecommendationCardProps) {
  const gradientClass = colorClasses[color] || colorClasses.gray;
  const emoji = emotionIcons[emotion] || '🤔';
  const [copiedField, setCopiedField] = useState<'send' | 'action' | null>(null);

  const handleCopy = async (text: string, field: 'send' | 'action') => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="flex justify-center my-4"
    >
      <Card className={`w-full max-w-lg border-2 ${gradientClass} shadow-xl hover:shadow-2xl transition-shadow duration-300`}>
        <CardHeader className="pb-3">
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
                      <span className="font-medium">AI-Powered Recommendations</span>
                    </>
                  ) : (
                    <>
                      <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
                      <span className="font-medium">Smart Recommendations</span>
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-3.5">
          {/* Send Message Recommendation */}
          <motion.div 
            className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/60 hover:border-indigo-200 transition-all duration-200"
            whileHover={{ scale: 1.01 }}
          >
            <div className="flex items-start gap-3">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-100 shrink-0">
                <Send className="w-4 h-4 text-indigo-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wide">
                  Send to someone
                </p>
                <p className="text-sm text-slate-800 italic leading-relaxed break-words">
                  "{recommendations.send_message}"
                </p>
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleCopy(recommendations.send_message, 'send')}
                    className={`h-8 mt-2 text-xs font-medium transition-all duration-200 ${
                      copiedField === 'send'
                        ? 'bg-green-100 text-green-700'
                        : 'hover:bg-indigo-50 hover:text-indigo-700'
                    }`}
                  >
                    {copiedField === 'send' ? (
                      <>
                        <Check className="w-3.5 h-3.5 mr-1.5" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5 mr-1.5" />
                        Copy
                      </>
                    )}
                  </Button>
                </motion.div>
              </div>
            </div>
          </motion.div>

          {/* Action Recommendation */}
          <motion.div 
            className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/60 hover:border-emerald-200 transition-all duration-200"
            whileHover={{ scale: 1.01 }}
          >
            <div className="flex items-start gap-3">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-100 shrink-0">
                <Footprints className="w-4 h-4 text-emerald-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wide">
                  Self-care action
                </p>
                <p className="text-sm text-slate-800 leading-relaxed break-words">
                  {recommendations.action}
                </p>
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleCopy(recommendations.action, 'action')}
                    className={`h-8 mt-2 text-xs font-medium transition-all duration-200 ${
                      copiedField === 'action'
                        ? 'bg-green-100 text-green-700'
                        : 'hover:bg-emerald-50 hover:text-emerald-700'
                    }`}
                  >
                    {copiedField === 'action' ? (
                      <>
                        <Check className="w-3.5 h-3.5 mr-1.5" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5 mr-1.5" />
                        Copy
                      </>
                    )}
                  </Button>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
