import ChatContainer from '@/components/chat/ChatContainer'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 blur-xl opacity-30 animate-pulse"></div>
              <div className="relative text-5xl">🧠</div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Emotion-Aware AI
            </h1>
          </div>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Detect emotions from text or speech and get{" "}
            <span className="font-semibold text-indigo-600">personalized recommendations</span>{" "}
            powered by advanced AI
          </p>
          
          {/* Feature Badges */}
          <div className="flex flex-wrap justify-center gap-2 mt-4">
            <span className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded-full">
              ⚡ NLTK Emotion Detection
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full">
              🤖 Groq AI Powered
            </span>
            <span className="px-3 py-1 bg-pink-100 text-pink-700 text-xs font-medium rounded-full">
              🎤 Voice Support
            </span>
          </div>
        </header>

        {/* Chat Container */}
        <ChatContainer />

        {/* Footer */}
        <footer className="text-center mt-8 text-sm text-slate-500">
          <p>NLP University Project • Powered by NLTK + Groq AI</p>
        </footer>
      </div>
    </main>
  )
}
