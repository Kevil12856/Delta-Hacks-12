'use client';

import Link from 'next/link';
import { ArrowRight, Scale, Shield, Zap, Database, Terminal, Users, FileText, Gavel, BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white selection:bg-indigo-500 selection:text-white font-sans">
      {/* Navbar */}
      <nav className="border-b border-white/5 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-indigo-600 to-violet-700 p-2.5 rounded-xl shadow-lg shadow-indigo-500/20">
              <Scale className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-xl tracking-tight leading-none">Mike Ross AI</span>
              <span className="text-[10px] text-slate-400 font-medium tracking-widest uppercase mt-0.5">Pearson Specter Litt V2</span>
            </div>
          </div>
          <div className="flex items-center gap-6">
             <Link href="https://github.com/kianis4/Delta-Hacks-12" target="_blank" className="text-sm font-medium text-slate-400 hover:text-white transition-colors hidden md:block">
                View Source
             </Link>
             <Link 
                href="/chat" 
                className="px-5 py-2.5 bg-white text-slate-950 rounded-lg text-sm font-bold hover:bg-slate-200 transition-all shadow-xl shadow-white/5"
              >
                Launch Assistant
              </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-24 overflow-hidden border-b border-white/5">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-indigo-600/20 blur-[120px] rounded-full pointer-events-none opacity-50" />
        
        <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-widest mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Zap className="w-3 h-3" />
            <span>DeltaHacks 12 Winner - Best Use of Gemini</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-gradient-to-b from-white via-white to-slate-400 bg-clip-text text-transparent animate-in fade-in slide-in-from-bottom-8 duration-700 drop-shadow-sm">
            "I don't play the odds, <br/> I play the man."
          </h1>
          
          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-100 font-light">
            Meet the first AI Legal Associate that actually <i>thinks</i>. <br/>
            Ingesting <b>16,170</b> pages of Canadian Law to give you verified, cited, and tactical legal advice in seconds.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-16 duration-1000 delay-200">
            <Link 
              href="/chat"
              className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all hover:scale-105 shadow-2xl shadow-indigo-900/40 flex items-center gap-2"
            >
              Consult Mike Ross
              <ArrowRight className="w-4 h-4" />
            </Link>
            <div className="px-6 py-4 flex items-center gap-2 text-slate-400 text-sm font-medium">
                <div className="flex -space-x-2">
                    <div className="w-8 h-8 rounded-full bg-slate-800 border-2 border-slate-950 flex items-center justify-center text-[10px]">ON</div>
                    <div className="w-8 h-8 rounded-full bg-slate-800 border-2 border-slate-950 flex items-center justify-center text-[10px]">BC</div>
                    <div className="w-8 h-8 rounded-full bg-slate-800 border-2 border-slate-950 flex items-center justify-center text-[10px]">AB</div>
                </div>
                <span>+ Federal Law</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats/Credibility Bar */}
      <section className="py-10 border-b border-white/5 bg-white/[0.02]">
          <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x divide-white/5">
              <div>
                  <div className="text-3xl font-bold text-white mb-1">16,170</div>
                  <div className="text-xs text-slate-500 font-mono uppercase tracking-widest">Legal Docs Ingested</div>
              </div>
              <div>
                  <div className="text-3xl font-bold text-white mb-1">768</div>
                  <div className="text-xs text-slate-500 font-mono uppercase tracking-widest">Vector Dimensions</div>
              </div>
              <div>
                  <div className="text-3xl font-bold text-white mb-1">2.0</div>
                  <div className="text-xs text-slate-500 font-mono uppercase tracking-widest">Gemini Flash Model</div>
              </div>
              <div>
                  <div className="text-3xl font-bold text-white mb-1">0.4s</div>
                  <div className="text-xs text-slate-500 font-mono uppercase tracking-widest">Retrieval Latency</div>
              </div>
          </div>
      </section>

      {/* Practice Areas */}
      <section className="py-24 bg-slate-950 relative">
        <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
                <h2 className="text-3xl font-bold mb-4">Full Spectrum Legal Coverage</h2>
                <p className="text-slate-400 max-w-2xl mx-auto">
                    Mike Ross isn't limited to a single domain. Our RAG pipeline dynamically routes queries to the correct specialized index.
                </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <PracticeCard 
                    icon={<Gavel className="w-6 h-6 text-indigo-400" />}
                    title="Criminal Law"
                    sub="Criminal Code of Canada (C-46)"
                    desc="Defenses, sentencing guidelines, and arrest procedures."
                />
                <PracticeCard 
                    icon={<Users className="w-6 h-6 text-pink-400" />}
                    title="Family Law"
                    sub="Divorce Act (C-3)"
                    desc="Separation, custody, property division, and spousal support."
                />
                <PracticeCard 
                    icon={<FileText className="w-6 h-6 text-emerald-400" />}
                    title="Tax Law"
                    sub="Income Tax Act (R.S.C., 1985)"
                    desc="Tax evasion penalties, deductions, and CRA dispute resolution."
                />
                <PracticeCard 
                    icon={<BookOpen className="w-6 h-6 text-amber-400" />}
                    title="Tenancy Law"
                    sub="RTA (Ontario, BC, Alberta)"
                    desc="Evictions (N12/N5), rent control, and tenant rights."
                />
            </div>
        </div>
      </section>

      {/* Technical Architecture */}
      <section className="py-24 bg-slate-900/30 border-y border-white/5">
        <div className="max-w-7xl mx-auto px-6">
            <div className="grid md:grid-cols-2 gap-16 items-center">
                <div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-widest mb-6">
                        System Architecture
                    </div>
                    <h2 className="text-3xl font-bold mb-6">Built Different. <br/> Engineered to Win.</h2>
                    <div className="space-y-8">
                        <TechItem 
                            title="LangGraph Agentic Workflow"
                            desc="We moved beyond simple chatbots. Mike Ross uses a state graph (Router -> Research -> Explain/Form) to autonomously decide if it needs to query the vector DB, fetch a government form, or ask clarifying questions."
                        />
                        <TechItem 
                            title="MongoDB Atlas Vector Search"
                            desc="High-performance approximate nearest neighbor (ANN) search across 16k+ document chunks. We used Hierarchical Navigable Small World (HNSW) graphs index for sub-second retrieval accuracy."
                        />
                         <TechItem 
                            title="Google Gemini 2.0"
                            desc="Leveraging the massive 1M+ token context window and superior reasoning capabilities to synthesize complex legalese into plain English without hallucinating."
                        />
                    </div>
                </div>
                <div className="relative">
                    {/* Abstract Visualization of the Agent Graph */}
                    <div className="absolute inset-0 bg-indigo-500/20 blur-[100px] rounded-full" />
                    <div className="relative bg-slate-950 border border-slate-800 rounded-2xl p-6 shadow-2xl">
                        <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
                            <div className="text-xs font-mono text-slate-500">agent_graph.py</div>
                            <div className="flex gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/50" />
                                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 border border-yellow-500/50" />
                                <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 border border-green-500/50" />
                            </div>
                        </div>
                        <div className="font-mono text-xs md:text-sm text-slate-300 space-y-2">
                            <div className="text-violet-400">class AgentState(TypedDict):</div>
                            <div className="pl-4 text-slate-500">messages: Annotated[list, add_messages]</div>
                            <div className="pl-4 text-slate-500">jurisdiction: str</div>
                            <div className="pl-4 text-slate-500">documents: list[Document]</div>
                            
                            <div className="text-blue-400 mt-4">def router(state):</div>
                            <div className="pl-4">if "divorce" in query:</div>
                            <div className="pl-8 text-green-400">return "RESEARCH_FEDERAL"</div>
                            <div className="pl-4">elif "evict" in query:</div>
                            <div className="pl-8 text-green-400">return "RESEARCH_PROVINCIAL"</div>
                            
                            <div className="text-slate-600 mt-4"># Intelligent Routing Active...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-24 text-center border-t border-white/5">
        <div className="max-w-7xl mx-auto px-6">
            <h2 className="text-2xl font-bold mb-12">The Partners</h2>
            <div className="flex flex-col md:flex-row justify-center gap-12 md:gap-24">
                <a href="https://www.linkedin.com/in/suleymankiani/" target="_blank" className="group">
                    <div className="flex flex-col items-center gap-4">
                        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center border-2 border-slate-700 group-hover:border-indigo-500 transition-colors overflow-hidden">
                             {/* Placeholder for Suley's Pic or Initials */}
                             <span className="text-2xl font-bold text-slate-400 group-hover:text-white">SK</span>
                        </div>
                        <div>
                            <div className="font-bold text-lg group-hover:text-indigo-400 transition-colors">Suleyman Kiani</div>
                            <div className="text-sm text-slate-500 uppercase tracking-widest font-medium">Senior Partner / Full Stack</div>
                        </div>
                    </div>
                </a>
                <a href="https://www.linkedin.com/in/karim-elbasiouni/" target="_blank" className="group">
                    <div className="flex flex-col items-center gap-4">
                        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center border-2 border-slate-700 group-hover:border-indigo-500 transition-colors overflow-hidden">
                             {/* Placeholder for Karim's Pic or Initials */}
                             <span className="text-2xl font-bold text-slate-400 group-hover:text-white">KE</span>
                        </div>
                        <div>
                            <div className="font-bold text-lg group-hover:text-indigo-400 transition-colors">Karim Elbasiouni</div>
                            <div className="text-sm text-slate-500 uppercase tracking-widest font-medium">Name Partner / AI Engineer</div>
                        </div>
                    </div>
                </a>
            </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-slate-600 text-sm border-t border-white/5 bg-slate-950">
        <div className="flex items-center justify-center gap-2 mb-4">
            <Shield className="w-4 h-4" />
            <span>Built securely for the 2026 DeltaHacks Hackathon</span>
        </div>
        <p>© 2026 Mike Ross AI. We represent the best.</p>
      </footer>
    </main>
  );
}

function PracticeCard({ icon, title, sub, desc }: { icon: React.ReactNode, title: string, sub: string, desc: string }) {
    return (
        <div className="p-6 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 hover:border-indigo-500/30 transition-all group">
            <div className="mb-4 p-3 bg-white/5 rounded-lg w-fit group-hover:scale-110 transition-transform">{icon}</div>
            <h3 className="text-lg font-bold mb-1 group-hover:text-white transition-colors">{title}</h3>
            <div className="text-xs font-mono text-indigo-400 mb-3">{sub}</div>
            <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
        </div>
    )
}

function TechItem({ title, desc }: { title: string, desc: string }) {
    return (
        <div className="flex gap-4">
             <div className="mt-1">
                <div className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
             </div>
             <div>
                 <h4 className="font-bold text-lg text-white mb-2">{title}</h4>
                 <p className="text-slate-400 leading-relaxed text-sm">{desc}</p>
             </div>
        </div>
    )
}
