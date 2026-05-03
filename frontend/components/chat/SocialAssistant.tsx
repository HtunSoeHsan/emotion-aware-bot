import React, { useState } from 'react';
import { Send, MessageSquare, Heart, Shield, RefreshCcw, ArrowLeft } from 'lucide-react';
import { analyzeSocialMessage } from '../../lib/api';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Textarea } from '../ui/textarea';

interface SocialAssistantProps {
  language: string;
  onBack: () => void;
}

const SocialAssistant: React.FC<SocialAssistantProps> = ({ language, onBack }) => {
  const [message, setMessage] = useState('');
  const [perspective, setPerspective] = useState<'receiver' | 'sender'>('receiver');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const isMyanmar = language === 'my';

  const handleAnalyze = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const data = await analyzeSocialMessage(message, perspective, language);
      setResult(data);
    } catch (error) {
      console.error(error);
      alert(isMyanmar ? 'ခွဲခြမ်းစိတ်ဖြာရန် အဆင်မပြေဖြစ်သွားပါသည်။' : 'Failed to analyze message.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setMessage('');
    setResult(null);
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 animate-in fade-in duration-300">
      <div className="p-4 flex items-center gap-3 bg-white border-b border-slate-200">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <div>
          <h2 className="font-bold text-slate-800">{isMyanmar ? 'လူမှုဆက်ဆံရေး အကူအညီပေးသူ' : 'Social Message Assistant'}</h2>
          <p className="text-xs text-slate-500">{isMyanmar ? 'စကားပြောဆိုမှုများကို ခွဲခြမ်းစိတ်ဖြာပေးသည်' : 'Analyze your relationship chats'}</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {!result ? (
          <Card className="border-none shadow-md">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">
                {isMyanmar ? 'စာသားကို ဒီမှာ ရိုက်ထည့်ပါ' : 'Enter Message to Analyze'}
              </CardTitle>
              <CardDescription>
                {isMyanmar ? 'ကောင်မလေး (သို့) တစ်စုံတစ်ယောက်ထံမှ စာ သို့မဟုတ် သင်ပို့လိုသောစာကို ထည့်ပါ' : 'Paste a message from someone or one you want to send'}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2 p-1 bg-slate-100 rounded-lg">
                <Button 
                  variant={perspective === 'receiver' ? 'default' : 'ghost'} 
                  className="flex-1 text-xs py-1 h-auto"
                  onClick={() => setPerspective('receiver')}
                >
                  <MessageSquare className="w-3 h-3 mr-1" />
                  {isMyanmar ? 'သူပို့လာသည့်စာ' : "From Someone"}
                </Button>
                <Button 
                  variant={perspective === 'sender' ? 'default' : 'ghost'} 
                  className="flex-1 text-xs py-1 h-auto"
                  onClick={() => setPerspective('sender')}
                >
                  <Send className="w-3 h-3 mr-1" />
                  {isMyanmar ? 'ငါပို့မည့်စာ' : "My Message"}
                </Button>
              </div>

              <Textarea 
                placeholder={isMyanmar ? 'ဒီမှာ ရေးပါ...' : 'Type or paste message here...'}
                className="min-h-[120px] bg-white border-slate-200 focus:ring-rose-500"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
            </CardContent>
            <CardFooter>
              <Button 
                className="w-full bg-rose-600 hover:bg-rose-700 text-white gap-2 py-6 rounded-xl text-lg font-bold shadow-lg"
                disabled={!message.trim() || loading}
                onClick={handleAnalyze}
              >
                {loading ? <RefreshCcw className="w-5 h-5 animate-spin" /> : <Shield className="w-5 h-5" />}
                {isMyanmar ? 'ခွဲခြမ်းစိတ်ဖြာမည်' : 'Analyze Now'}
              </Button>
            </CardFooter>
          </Card>
        ) : (
          <div className="space-y-4 pb-20 animate-in slide-in-from-bottom-4 duration-500">
            {/* Analysis Result */}
            <Card className="border-none shadow-md overflow-hidden bg-gradient-to-br from-white to-rose-50/30">
              <div className="h-1 bg-rose-500 w-full" />
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <Badge variant="outline" className="bg-rose-50 text-rose-700 border-rose-200">
                    {perspective === 'receiver' 
                      ? (isMyanmar ? 'ခံစားချက် ခန့်မှန်းချက်' : 'Sender Emotion') 
                      : (isMyanmar ? 'ဖြစ်လာနိုင်သော အကျိုးသက်ရောက်မှု' : 'Predicted Impact')}
                  </Badge>
                  <Button variant="ghost" size="sm" onClick={reset} className="h-8 text-xs">
                    {isMyanmar ? 'အသစ်ပြန်စရန်' : 'Try Another'}
                  </Button>
                </div>
                <CardTitle className="text-2xl mt-2 text-rose-900">
                  {result.detected_emotion || result.predicted_impact}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-white/60 p-3 rounded-lg border border-white">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
                    {isMyanmar ? 'ခွဲခြမ်းစိတ်ဖြာချက်' : 'Analysis'}
                  </h4>
                  <p className="text-slate-800 leading-relaxed">{result.analysis}</p>
                </div>

                <div className="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100">
                  <h4 className="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-1">
                    {isMyanmar ? 'အကြံပြုချက်' : 'Advice'}
                  </h4>
                  <p className="text-slate-800 leading-relaxed italic">"{result.advice}"</p>
                </div>
              </CardContent>
            </Card>

            {/* Suggested Replies */}
            <div className="space-y-3">
              <h3 className="font-bold text-slate-700 flex items-center gap-2 px-1">
                <Heart className="w-4 h-4 text-rose-500" />
                {isMyanmar ? 'ပို့သင့်သည့် ပြန်စာများ' : 'Suggested Replies'}
              </h3>
              
              {result.suggested_replies?.map((reply: string, i: number) => (
                <div 
                  key={i} 
                  className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-rose-300 hover:shadow-md transition-all cursor-pointer group"
                  onClick={() => {
                    navigator.clipboard.writeText(reply);
                    alert(isMyanmar ? 'ကူးယူပြီးပါပြီ' : 'Copied to clipboard');
                  }}
                >
                  <div className="flex justify-between items-start gap-3">
                    <p className="text-slate-800 font-medium leading-relaxed">{reply}</p>
                    <Badge variant="secondary" className="shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                      {isMyanmar ? 'Copy ကူးမည်' : 'Copy'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4 text-center text-[10px] text-slate-400">
        Powered by Groq AI Relationship Assistant
      </div>
    </div>
  );
};

export default SocialAssistant;
