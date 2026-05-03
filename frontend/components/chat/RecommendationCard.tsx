'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Send, Footprints, Sparkles, Check, Copy, ExternalLink, Youtube, Music, Podcast, Newspaper, GraduationCap, Heart, Brain, Lightbulb, MessageCircle } from 'lucide-react';

interface RecommendationCardProps {
  emotion: string;
  color: string;
  recommendations: any;
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
  const [copiedId, setCopiedId] = useState<number | null>(null);

  // Debug logging
  useEffect(() => {
    console.log('=== RecommendationCard Debug ===');
    console.log('emotion:', emotion);
    console.log('multi_source:', multi_source);
    console.log('external_resources:', external_resources);
    if (external_resources) {
      console.log('external_resources.sources:', external_resources.sources);
    }
  }, [emotion, multi_source, external_resources]);

  const handleCopy = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(index);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const openLink = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  // Get embed URL for YouTube
  const getYouTubeEmbed = (url: string) => {
    const videoId = url.match(/(?:youtu\.be\/|youtube\.com\/watch\?v=)([a-zA-Z0-9_-]+)/)?.[1];
    return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
  };

  // Get embed URL for Spotify
  const getSpotifyEmbed = (url: string) => {
    return url.replace('open.spotify.com/playlist', 'open.spotify.com/embed/playlist')
      .replace('open.spotify.com/track', 'open.spotify.com/embed/track');
  };

  // Combine all sources
  const allSources = {
    ...multi_source?.sources,
    ...external_resources?.sources
  };

  console.log('Combined allSources:', allSources);
  console.log('Source keys:', Object.keys(allSources));

  return (
    <div className="flex justify-center my-4">
      <Card className={`w-full max-w-5xl border-2 ${colors.border} ${colors.bg} shadow-xl`}>
        <CardHeader className="pb-3 border-b">
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
          {/* AI or Primary Recommendations */}
          <div className="grid md:grid-cols-2 gap-4">
            {/* Handle AI Recommendations (Array format) */}
            {Array.isArray(recommendations) ? (
              recommendations.map((item: any, idx: number) => {
                let Icon = Sparkles;
                let bgColor = 'bg-slate-100';
                let iconColor = 'text-slate-600';

                if (item.type === 'message') { Icon = Send; bgColor = 'bg-indigo-100'; iconColor = 'text-indigo-600'; }
                if (item.type === 'action') { Icon = Footprints; bgColor = 'bg-emerald-100'; iconColor = 'text-emerald-600'; }
                if (item.type === 'impact') { Icon = Brain; bgColor = 'bg-purple-100'; iconColor = 'text-purple-600'; }
                if (item.type === 'reply_suggestion') { Icon = MessageCircle; bgColor = 'bg-blue-100'; iconColor = 'text-blue-600'; }

                return (
                  <div key={idx} className="bg-white/90 rounded-xl p-4 border hover:shadow-md transition-all">
                    <div className="flex items-start gap-3">
                      <div className={`w-9 h-9 rounded-lg ${bgColor} flex items-center justify-center shrink-0`}>
                        <Icon className={`w-5 h-5 ${iconColor}`} />
                      </div>
                      <div className="flex-1">
                        <p className="text-[10px] font-bold text-slate-500 mb-1 uppercase tracking-wider">{item.label}</p>
                        <p className="text-sm text-slate-800 font-medium mb-3">{item.text}</p>
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" onClick={() => handleCopy(item.text, idx)} className="h-8 text-[10px]">
                            {copiedId === idx ? <Check className="w-3 h-3 mr-1" /> : <Copy className="w-3 h-3 mr-1" />}
                            {copiedId === idx ? 'Copied' : 'Copy'}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              /* Handle Rule-based Recommendations (Object format) */
              <>
                {recommendations?.send_message && (
                  <div className="bg-white/90 rounded-xl p-4 border">
                    <div className="flex items-start gap-3">
                      <div className="w-9 h-9 rounded-lg bg-indigo-100 flex items-center justify-center shrink-0">
                        <Send className="w-5 h-5 text-indigo-600" />
                      </div>
                      <div className="flex-1">
                        <p className="text-xs font-bold text-slate-700 mb-2 uppercase">Send to someone</p>
                        <p className="text-sm text-slate-800 italic mb-3">"{recommendations.send_message}"</p>
                        <Button variant="outline" size="sm" onClick={() => handleCopy(recommendations.send_message, 0)} className="h-9 text-xs">
                          {copiedId === 0 ? <Check className="w-3.5 h-3.5 mr-1.5" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}
                          Copy
                        </Button>
                      </div>
                    </div>
                  </div>
                )}

                {recommendations?.action && (
                  <div className="bg-white/90 rounded-xl p-4 border">
                    <div className="flex items-start gap-3">
                      <div className="w-9 h-9 rounded-lg bg-emerald-100 flex items-center justify-center shrink-0">
                        <Footprints className="w-5 h-5 text-emerald-600" />
                      </div>
                      <div className="flex-1">
                        <p className="text-xs font-bold text-slate-700 mb-2 uppercase">Self-care action</p>
                        <p className="text-sm text-slate-800 mb-3">{recommendations.action}</p>
                        <Button variant="outline" size="sm" onClick={() => handleCopy(recommendations.action, 1)} className="h-9 text-xs">
                          {copiedId === 1 ? <Check className="w-3.5 h-3.5 mr-1.5" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}
                          Copy
                        </Button>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          {/* External Resources */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ExternalLink className="w-5 h-5 text-slate-600" />
                <h4 className="text-lg font-bold text-slate-800">Recommended Resources</h4>
                <Badge variant="secondary">Playable & Readable</Badge>
              </div>
            </div>

            {/* YouTube Videos */}
            {allSources.youtube && allSources.youtube.length > 0 && (
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${colors.light}`}>
                    <Youtube className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">Videos</p>
                    <p className="text-xs text-slate-500">{allSources.youtube.length} recommendations</p>
                  </div>
                </div>
                <div className="p-4 grid md:grid-cols-2 gap-4">
                  {allSources.youtube.slice(0, 4).map((item: any, idx: number) => {
                    const embedUrl = getYouTubeEmbed(item.url);
                    return (
                      <div key={idx} className="space-y-2">
                        {embedUrl ? (
                          <div className="aspect-video rounded-lg overflow-hidden bg-slate-900">
                            <iframe
                              src={embedUrl}
                              title={item.title}
                              className="w-full h-full"
                              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                              allowFullScreen
                            />
                          </div>
                        ) : (
                          <div
                            className="aspect-video rounded-lg bg-slate-100 flex items-center justify-center cursor-pointer hover:bg-slate-200"
                            onClick={() => openLink(item.url)}
                          >
                            <Youtube className={`w-12 h-12 ${colors.text}`} />
                          </div>
                        )}
                        <p className="text-sm font-medium text-slate-800 line-clamp-2">{item.title}</p>
                        <Button variant="outline" size="sm" onClick={() => openLink(item.url)} className="w-full">
                          <ExternalLink className="w-3.5 h-3.5 mr-1.5" />Open on YouTube
                        </Button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Spotify Music */}
            {allSources.spotify && allSources.spotify.length > 0 && (
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${colors.light}`}>
                    <Music className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">Music & Playlists</p>
                    <p className="text-xs text-slate-500">{allSources.spotify.length} recommendations</p>
                  </div>
                </div>
                <div className="p-4 space-y-4">
                  {allSources.spotify.map((item: any, idx: number) => {
                    const embedUrl = getSpotifyEmbed(item.url);
                    return (
                      <div key={idx} className="border border-slate-200 rounded-lg p-4">
                        {item.url.includes('spotify.com') ? (
                          <iframe
                            src={embedUrl}
                            title={item.title}
                            className="w-full rounded-lg"
                            style={{ height: '152px' }}
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                          />
                        ) : (
                          <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100" onClick={() => openLink(item.url)}>
                            <div className={`p-3 rounded-full ${colors.light}`}><Music className={`w-6 h-6 ${colors.text}`} /></div>
                            <div className="flex-1">
                              <p className="text-sm font-medium text-slate-800">{item.title}</p>
                              <p className="text-xs text-slate-600">{item.description}</p>
                            </div>
                            <ExternalLink className="w-4 h-4 text-slate-400" />
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Podcast Episodes */}
            {allSources.podcast && allSources.podcast.length > 0 && (
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${colors.light}`}>
                    <Podcast className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">Podcasts</p>
                    <p className="text-xs text-slate-500">{allSources.podcast.length} episodes</p>
                  </div>
                </div>
                <div className="p-4 space-y-3">
                  {allSources.podcast.map((item: any, idx: number) => (
                    <div key={idx} className="flex items-start gap-3 p-3 border border-slate-200 rounded-lg hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer" onClick={() => openLink(item.url)}>
                      {item.thumbnail && <img src={item.thumbnail} alt={item.title} className="w-16 h-16 object-cover rounded-lg shrink-0" />}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-800 line-clamp-2 mb-1">{item.title}</p>
                        {item.episode && <p className="text-xs text-slate-600 mb-1">{item.episode}</p>}
                        {item.artist && <p className="text-xs text-slate-500">🎙️ {item.artist}</p>}
                      </div>
                      <ExternalLink className="w-4 h-4 text-slate-400 shrink-0 mt-1" />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TED Talks */}
            {allSources.ted && allSources.ted.length > 0 && (
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${colors.light}`}>
                    <GraduationCap className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">TED Talks</p>
                    <p className="text-xs text-slate-500">{allSources.ted.length} talks</p>
                  </div>
                </div>
                <div className="p-4 grid md:grid-cols-2 gap-4">
                  {allSources.ted.map((item: any, idx: number) => (
                    <div key={idx} className="border border-slate-200 rounded-lg overflow-hidden hover:border-indigo-300 hover:shadow-md transition-all">
                      <div
                        className="aspect-video bg-gradient-to-br from-red-600 to-red-800 flex items-center justify-center cursor-pointer"
                        onClick={() => openLink(item.url)}
                      >
                        <div className="text-center text-white">
                          <GraduationCap className="w-12 h-12 mx-auto mb-2" />
                          <p className="text-sm font-semibold">Watch on TED</p>
                        </div>
                      </div>
                      <div className="p-3 space-y-2">
                        <p className="text-sm font-medium text-slate-800 line-clamp-2">{item.title}</p>
                        <p className="text-xs text-slate-600">🎤 {item.speaker}</p>
                        <div className="flex items-center justify-between">
                          {item.duration && <Badge variant="outline" className="text-xs">⏱ {item.duration}</Badge>}
                          <Button variant="outline" size="sm" onClick={() => openLink(item.url)}>
                            <ExternalLink className="w-3.5 h-3.5 mr-1.5" />Watch
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {/* Activities & Self-care */}
            {(allSources.activity || allSources.self_care) && (
              <div className="grid md:grid-cols-2 gap-6">
                {allSources.activity && allSources.activity.length > 0 && (
                  <div className="border border-slate-200 rounded-xl overflow-hidden bg-white">
                    <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                      <div className={`p-2 rounded-lg bg-orange-100`}>
                        <Lightbulb className={`w-5 h-5 text-orange-600`} />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-800">Suggested Activities</p>
                        <p className="text-xs text-slate-500">{allSources.activity.length} ideas</p>
                      </div>
                    </div>
                    <div className="p-4 space-y-3">
                      {allSources.activity.map((item: any, idx: number) => (
                        <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                          <p className="text-sm font-bold text-slate-800 mb-1">{item.title}</p>
                          <p className="text-xs text-slate-600 mb-2">{item.description}</p>
                          <div className="flex gap-2">
                            {item.duration && <Badge variant="outline" className="text-[10px]">{item.duration}</Badge>}
                            {item.effort && <Badge variant="outline" className="text-[10px] capitalize">Effort: {item.effort}</Badge>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {allSources.self_care && allSources.self_care.length > 0 && (
                  <div className="border border-slate-200 rounded-xl overflow-hidden bg-white">
                    <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                      <div className={`p-2 rounded-lg bg-pink-100`}>
                        <Heart className={`w-5 h-5 text-pink-600`} />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-800">Self-Care Tips</p>
                        <p className="text-xs text-slate-500">{allSources.self_care.length} tips</p>
                      </div>
                    </div>
                    <div className="p-4 space-y-2">
                      {allSources.self_care.map((tip: string, idx: number) => (
                        <div key={idx} className="flex items-start gap-2 p-2 bg-pink-50/30 rounded-lg">
                          <Check className="w-4 h-4 text-pink-500 mt-0.5 shrink-0" />
                          <p className="text-sm text-slate-700">{tip}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Social & Relationship Messages */}
            {allSources.social && allSources.social.length > 0 && (
              <div className="border border-slate-200 rounded-xl overflow-hidden bg-white">
                <div className="bg-slate-50 px-4 py-3 flex items-center gap-3">
                  <div className={`p-2 rounded-lg bg-blue-100`}>
                    <MessageCircle className={`w-5 h-5 text-blue-600`} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">Social & Relationship Replies</p>
                    <p className="text-xs text-slate-500">{allSources.social.length} suggested messages</p>
                  </div>
                </div>
                <div className="p-4 grid md:grid-cols-2 gap-3">
                  {allSources.social.map((msg: string, idx: number) => (
                    <div key={idx} className="p-3 bg-blue-50/50 rounded-lg border border-blue-100 group relative">
                      <p className="text-sm text-slate-800 italic pr-8">"{msg}"</p>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => handleCopy(msg, 1000 + idx)}
                      >
                        {copiedId === 1000 + idx ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-center gap-2 pt-4 border-t">
            <p className="text-xs text-slate-500 text-center">💙 Remember: It's okay to feel this way. Take it one step at a time.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
