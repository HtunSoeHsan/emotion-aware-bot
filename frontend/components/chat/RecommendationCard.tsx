'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Send, Footprints, Lightbulb, Sparkles, Check, Copy, ExternalLink, Youtube, Music, Podcast, Newspaper, GraduationCap } from 'lucide-react';

interface RecommendationCardProps {
  emotion: string;
  color: string;
  recommendations: any; // Can be dict (multi-source) or list (dev branch)
  source?: 'ai' | 'rules';
  count?: number;
  multi_source?: any;
  external_resources?: any;
}

const emotionIcons: Record<string, string> = {
  joy: '😊',
  anger: '😠',
  sadness: '😢',
  fear: '😨',
  neutral: '😐',
};

const colorClasses: Record<string, any> = {
  green: { gradient: 'from-green-500 to-emerald-600', border: 'border-green-200', bg: 'bg-green-50', text: 'text-green-700', light: 'bg-green-100' },
  red: { gradient: 'from-red-500 to-rose-600', border: 'border-red-200', bg: 'bg-red-50', text: 'text-red-700', light: 'bg-red-100' },
  blue: { gradient: 'from-blue-500 to-sky-600', border: 'border-blue-200', bg: 'bg-blue-50', text: 'text-blue-700', light: 'bg-blue-100' },
  purple: { gradient: 'from-purple-500 to-violet-600', border: 'border-purple-200', bg: 'bg-purple-50', text: 'text-purple-700', light: 'bg-purple-100' },
  gray: { gradient: 'from-gray-500 to-slate-600', border: 'border-gray-200', bg: 'bg-gray-50', text: 'text-gray-700', light: 'bg-gray-100' },
};

const sourceIcons: Record<string, any> = {
  youtube: Youtube,
  spotify: Music,
  podcast: Podcast,
  news: Newspaper,
  ted: GraduationCap,
};

export default function RecommendationCard({
  emotion,
  color,
  recommendations,
  source,
  count,
  multi_source,
  external_resources,
}: RecommendationCardProps) {
  const colors = colorClasses[color] || colorClasses.gray;
  const emoji = emotionIcons[emotion] || '🤔';
  const [copiedField, setCopiedField] = useState<'send' | 'action' | null>(null);
  const [showResources, setShowResources] = useState(false);

  const handleCopy = async (text: string, field: 'send' | 'action') => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const openLink = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  // Handle both formats
  const recsArray = Array.isArray(recommendations) ? recommendations : [];
  const isListFormat = Array.isArray(recommendations);
  
  // Extract from list format (dev branch)
  const messages = isListFormat ? recsArray.filter((r: any) => r.type === 'message') : [];
  const actions = isListFormat ? recsArray.filter((r: any) => r.type === 'action') : [];
  
  // Extract from dict format (our multi-source)
  const send_message = !isListFormat ? recommendations?.send_message : (messages[0]?.text || '');
  const action = !isListFormat ? recommendations?.action : (actions[0]?.text || '');
  const quick_action = recommendations?.quick_action;
  
  // Combine sources
  const allSources = { ...multi_source?.sources, ...external_resources?.sources };
  const quickPicks = external_resources?.quick_picks || multi_source?.quick_picks;
  const hasResources = !!(quickPicks || (allSources && Object.keys(allSources).length > 0));

  if (isListFormat) {
    // Dev branch list-based format
    return (
      <div className="flex justify-center my-4">
        <Card className={`w-full max-w-2xl border-2 ${colors.gradient} ${colors.border} ${colors.bg} shadow-xl hover:shadow-2xl transition-shadow duration-300`}>
          <CardHeader className="pb-3 border-b border-slate-200/50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="text-3xl">{emoji}</span>
                <div>
                  <h3 className="font-semibold text-slate-800 capitalize text-lg">{emotion} Detected</h3>
                  <p className="text-xs text-slate-600 flex items-center gap-1.5">
                    {source === 'ai' ? (
                      <>
                        <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                        <span className="font-medium">AI-Powered ({count || recommendations.length} suggestions)</span>
                      </>
                    ) : (
                      <>
                        <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
                        <span className="font-medium">Smart ({count || recommendations.length} suggestions)</span>
                      </>
                    )}
                  </p>
                </div>
              </div>
            </div>
          </CardHeader>

          <CardContent className="pt-4 space-y-4">
            {/* Messages */}
            {messages.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                  <Send className="w-4 h-4 text-indigo-600" />
                  Send to someone
                </h4>
                <div className="space-y-3">
                  {messages.map((rec: any, idx: number) => (
                    <div key={idx} className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/60">
                      <div className="flex items-start gap-3">
                        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-100 shrink-0">
                          <Send className="w-4 h-4 text-indigo-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-slate-800 italic leading-relaxed break-words mb-2">
                            "{rec.text}"
                          </p>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleCopy(rec.text, 'send')}
                            className={`h-8 text-xs font-medium ${copiedField === 'send' ? 'bg-green-100 text-green-700' : 'hover:bg-indigo-50 hover:text-indigo-700'}`}
                          >
                            {copiedField === 'send' ? (<><Check className="w-3.5 h-3.5 mr-1.5" />Copied!</>) : (<><Copy className="w-3.5 h-3.5 mr-1.5" />Copy</>)}
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions */}
            {actions.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                  <Footprints className="w-4 h-4 text-emerald-600" />
                  Self-care actions
                </h4>
                <div className="space-y-3">
                  {actions.map((rec: any, idx: number) => (
                    <div key={idx} className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/60">
                      <div className="flex items-start gap-3">
                        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-100 shrink-0">
                          <Footprints className="w-4 h-4 text-emerald-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-slate-800 leading-relaxed break-words mb-2">
                            {rec.text}
                          </p>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleCopy(rec.text, 'action')}
                            className={`h-8 text-xs font-medium ${copiedField === 'action' ? 'bg-green-100 text-green-700' : 'hover:bg-emerald-50 hover:text-emerald-700'}`}
                          >
                            {copiedField === 'action' ? (<><Check className="w-3.5 h-3.5 mr-1.5" />Copied!</>) : (<><Copy className="w-3.5 h-3.5 mr-1.5" />Copy</>)}
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  // Our multi-source format
  return (
    <div className="flex justify-center my-4">
      <Card className={`w-full max-w-4xl border-2 ${colors.border} ${colors.bg} shadow-xl`}>
        <CardHeader className="pb-3 border-b border-white/60">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">{emoji}</span>
              <div>
                <h3 className="font-bold text-slate-800 capitalize text-xl">{emotion} Detected</h3>
                <p className="text-xs text-slate-600 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-600" />
                  <span className="font-medium">{source === 'ai' ? 'AI-Powered' : 'Curated'} Recommendations</span>
                </p>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-4 space-y-6">
          {/* Quick Activity */}
          {quick_action && (
            <div>
              <h4 className="text-sm font-bold text-slate-700 mb-2 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-500" />
                Quick Activity
              </h4>
              <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-white/60 shadow-sm">
                <div className="flex items-start gap-3">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-lg ${colors.light} shrink-0`}>
                    <Footprints className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-slate-800 mb-1">{quick_action.title}</p>
                    <p className="text-sm text-slate-600 mb-2">{quick_action.description}</p>
                    <div className="flex gap-2">
                      {quick_action.duration && <Badge variant="secondary" className="text-xs">⏱ {quick_action.duration}</Badge>}
                      {quick_action.effort && <Badge variant="outline" className="text-xs">💪 {quick_action.effort}</Badge>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Primary Recommendations */}
          <div className="grid md:grid-cols-2 gap-4">
            {/* Send Message */}
            {send_message && (
              <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-white/60">
                <div className="flex items-start gap-3">
                  <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-indigo-100 shrink-0">
                    <Send className="w-5 h-5 text-indigo-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-slate-700 mb-2 uppercase tracking-wide">Send to someone</p>
                    <p className="text-sm text-slate-800 italic leading-relaxed break-words mb-3">"{send_message}"</p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCopy(send_message, 'send')}
                      className={`h-9 text-xs font-medium ${copiedField === 'send' ? 'bg-green-100 text-green-700 border-green-300' : 'hover:bg-indigo-50 hover:text-indigo-700'}`}
                    >
                      {copiedField === 'send' ? (<><Check className="w-3.5 h-3.5 mr-1.5" />Copied!</>) : (<><Copy className="w-3.5 h-3.5 mr-1.5" />Copy</>)}
                    </Button>
                  </div>
                </div>
              </div>
            )}

            {/* Action */}
            {action && (
              <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-white/60">
                <div className="flex items-start gap-3">
                  <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-emerald-100 shrink-0">
                    <Footprints className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-slate-700 mb-2 uppercase tracking-wide">Self-care action</p>
                    <p className="text-sm text-slate-800 leading-relaxed break-words mb-3">{action}</p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCopy(action, 'action')}
                      className={`h-9 text-xs font-medium ${copiedField === 'action' ? 'bg-green-100 text-green-700 border-green-300' : 'hover:bg-emerald-50 hover:text-emerald-700'}`}
                    >
                      {copiedField === 'action' ? (<><Check className="w-3.5 h-3.5 mr-1.5" />Copied!</>) : (<><Copy className="w-3.5 h-3.5 mr-1.5" />Copy</>)}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* External Resources */}
          {hasResources && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ExternalLink className="w-5 h-5 text-slate-600" />
                  <h4 className="text-lg font-bold text-slate-800">Recommended Resources</h4>
                  <Badge variant="secondary">Live Links</Badge>
                </div>
                <Button variant="outline" size="sm" onClick={() => setShowResources(!showResources)}>
                  {showResources ? 'Hide' : 'Show'} Resources
                </Button>
              </div>

              {/* Quick Picks */}
              {quickPicks && showResources && (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {Object.entries(quickPicks).map(([sourceType, item]: [string, any]) =>
                    item ? (
                      <div
                        key={sourceType}
                        className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-white/60 hover:shadow-lg transition-all cursor-pointer"
                        onClick={() => openLink(item.url)}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <div className={`p-2 rounded-lg ${colors.light}`}>
                            {sourceIcons[sourceType] ? <sourceIcons[sourceType] className={`w-4 h-4 ${colors.text}`} /> : <ExternalLink className={`w-4 h-4 ${colors.text}`} />}
                          </div>
                          <span className="text-xs font-semibold text-slate-600 uppercase">{sourceType}</span>
                        </div>
                        <p className="text-sm font-medium text-slate-800 line-clamp-2 mb-2">{item.title}</p>
                        {item.duration && <Badge variant="outline" className="text-xs">⏱ {item.duration}</Badge>}
                      </div>
                    ) : null
                  )}
                </div>
              )}

              {/* More Resources */}
              {allSources && showResources && (
                <div className="space-y-4">
                  {Object.entries(allSources).map(([sourceType, items]: [string, any]) =>
                    items && items.length > 0 ? (
                      <div key={sourceType} className="space-y-2">
                        <div className="flex items-center gap-2">
                          {sourceIcons[sourceType] ? <sourceIcons[sourceType] className={`w-4 h-4 ${colors.text}`} /> : <ExternalLink className={`w-4 h-4 ${colors.text}`} />}
                          <span className="text-sm font-semibold text-slate-700 capitalize">{sourceType.replace('_', ' ')}</span>
                        </div>
                        <div className="space-y-2 pl-6">
                          {items.slice(0, 3).map((item: any, idx: number) => (
                            <div
                              key={idx}
                              className="bg-white rounded-lg p-3 border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer"
                              onClick={() => openLink(item.url)}
                            >
                              <div className="flex items-start gap-3">
                                {item.thumbnail && <img src={item.thumbnail} alt={item.title} className="w-16 h-12 object-cover rounded-lg shrink-0" />}
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm font-medium text-slate-800 line-clamp-2">{item.title}</p>
                                  {item.description && <p className="text-xs text-slate-600 line-clamp-1 mt-1">{item.description}</p>}
                                </div>
                                <ExternalLink className="w-4 h-4 text-slate-400 shrink-0" />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : null
                  )}
                </div>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="flex items-center justify-center gap-2 pt-4 border-t border-white/60">
            <p className="text-xs text-slate-500 text-center">💙 Remember: It's okay to feel this way. Take it one step at a time.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
