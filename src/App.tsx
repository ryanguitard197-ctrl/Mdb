import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Monitor, 
  Terminal, 
  FileText, 
  Folder, 
  Settings, 
  Shield, 
  Layout, 
  Globe, 
  Music, 
  Play, 
  Image as ImageIcon,
  Calculator,
  Calendar,
  Camera,
  Layers,
  Cpu,
  Wifi,
  Volume2,
  Battery,
  Search,
  X,
  Minus,
  Maximize2,
  Trash2,
  HardDrive,
  Box,
  Scaling,
  Activity,
  ShoppingBag,
  Download,
  Info,
  CheckCircle,
  RotateCcw,
  ArrowLeft,
  ArrowRight,
  Code as FileCode,
  GitBranch,
  Gamepad2,
  Lock,
  Mail
} from 'lucide-react';
import { calculateCoordinates, MDBCoordinates, fold, FoldedLayer, SuperBit } from './services/mdbCore';
import { analyzeThreat, ThreatAnalysis } from './services/geminiService';

// Types
interface WindowProps {
  id: string;
  title: string;
  mode?: string;
  icon: React.ReactNode;
  content: React.ReactNode;
  isOpen: boolean;
  isMaximized: boolean;
  zIndex: number;
  onClose: (id: string) => void;
  onMinimize: (id: string) => void;
  onFocus: (id: string) => void;
}

// Components
const Window: React.FC<WindowProps> = ({ 
  id, title, mode, icon, content, isMaximized, zIndex, onClose, onMinimize, onFocus 
}) => {
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  const effectiveMaximized = isMaximized || isMobile;

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ 
        scale: 1, 
        opacity: 1, 
        x: 0, 
        y: 0,
        width: effectiveMaximized ? '100%' : '850px',
        height: effectiveMaximized ? '100%' : '550px',
        top: effectiveMaximized ? 0 : '40px',
        left: effectiveMaximized ? 0 : '40px',
      }}
      exit={{ scale: 0.9, opacity: 0 }}
      drag={!effectiveMaximized}
      dragMomentum={false}
      onMouseDown={() => onFocus(id)}
      style={{ zIndex }}
      className={`absolute glass-morphism window-shadow flex flex-col overflow-hidden border border-white/10 ${
        effectiveMaximized ? 'rounded-none' : 'rounded-xl'
      }`}
    >
      {/* Title Bar - Height increased for touch */}
      <div className="h-14 md:h-12 bg-white/5 flex items-center justify-between px-4 cursor-grab active:cursor-grabbing border-b border-white/5 shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-blue-400">{icon}</span>
          <div className="flex items-baseline gap-2">
            <span className="text-xs font-bold tracking-widest uppercase opacity-80">{title}</span>
            <span className={`hidden md:inline-block text-[8px] px-1.5 py-0.5 rounded border font-mono font-bold ${mode === 'Dimensional' ? 'bg-purple-500/20 border-purple-500/40 text-purple-300' : 'bg-blue-500/20 border-blue-500/40 text-blue-300'}`}>
              {mode === 'Dimensional' ? 'Δ CORE' : 'CLASSIC'}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {!isMobile && (
            <>
              <button onClick={() => onMinimize(id)} className="p-2 hover:bg-white/10 rounded-md transition-colors min-w-[36px]">
                <Minus size={16} />
              </button>
              <button className="p-2 hover:bg-white/10 rounded-md transition-colors min-w-[36px]">
                <Maximize2 size={16} />
              </button>
            </>
          )}
          <button onClick={() => onClose(id)} className="p-3 md:p-2 hover:bg-red-500/80 rounded-md transition-colors min-w-[44px]">
            <X size={20} />
          </button>
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 overflow-auto bg-black/60">
        {content}
      </div>
    </motion.div>
  );
};

const MDBInstaller: React.FC = () => {
  const [step, setStep] = useState(0);
  const [progress, setProgress] = useState(0);

  const startInstall = () => {
    setStep(1);
    let p = 0;
    const interval = setInterval(() => {
      p += 1;
      setProgress(p);
      if (p >= 100) {
        clearInterval(interval);
        setStep(2);
      }
    }, 50);
  };

  return (
    <div className="p-8 h-full flex flex-col items-center justify-center max-w-2xl mx-auto">
      {step === 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center space-y-6">
          <div className="w-24 h-24 bg-blue-500/10 rounded-3xl flex items-center justify-center mx-auto mb-8 border border-blue-500/30">
            <HardDrive size={48} className="text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold tracking-tighter">MDB OS INSTALLER</h1>
          <p className="text-white/40 text-sm">
            This will format the target drive into Multidimensional Binary space (D3-D100).
            WARNING: All existing data on this partition will be folded and compressed.
          </p>
          <div className="bg-white/5 p-4 rounded-xl text-left text-xs font-mono space-y-2 border border-white/5">
            <div className="text-blue-400 font-bold">INSTALLER DIRECTIVES:</div>
            <div>• Target: Physical Disk 0 (MDB Kernel)</div>
            <div>• Filesystem: mdbfs (Dimensional Mapping)</div>
            <div>• Security: Hardware-Authoritative Agent v1.1</div>
          </div>
          <button onClick={startInstall} className="mdb-button bg-blue-600 w-full py-4 text-lg font-bold tracking-widest hover:bg-blue-700 mt-6 shadow-[0_0_20px_rgba(59,130,246,0.3)]">
            BEGIN FOLDING INSTALL
          </button>
        </motion.div>
      )}

      {step === 1 && (
        <div className="w-full space-y-8 text-center">
          <motion.div 
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            className="w-16 h-16 border-t-2 border-blue-500 rounded-full mx-auto"
          />
          <div className="space-y-2">
            <div className="text-sm font-bold tracking-widest text-blue-400 uppercase">
              {progress < 30 ? "Initializing D3 Layer..." : progress < 60 ? "Squeezing Dimensional Space..." : "Locking PHI Coordinates..."}
            </div>
            <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
              <motion.div animate={{ width: `${progress}%` }} className="h-full bg-blue-500" />
            </div>
            <div className="text-[10px] font-mono opacity-40">PROGRESS: {progress}% // SECTOR_MAP_DIM_{Math.floor(progress/5)}</div>
          </div>
        </div>
      )}

      {step === 2 && (
        <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }} className="text-center space-y-6">
          <CheckCircle size={64} className="text-green-500 mx-auto" />
          <h2 className="text-2xl font-bold">INSTALLATION COMPLETE</h2>
          <p className="text-white/40">MDB OS has been successfully deployed to the dimensional grain.</p>
          <button onClick={() => window.location.reload()} className="mdb-button bg-white/10 hover:bg-white/20 w-full py-3">REBOOT SYSTEM</button>
        </motion.div>
      )}
    </div>
  );
};

// Apps
const MDBTerminal: React.FC = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<string[]>(['MDB OS v1.1.0 Kernel (x86_64)', 'Dimensional Index: Status OK', 'All SuperBits stable.', 'Type "help" for a list of commands.']);
  
  const handleCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newHistory = [...history, `> ${input}`];
    const cmdInput = input.trim();
    const cmd = cmdInput.toLowerCase();

    if (cmd === 'help') {
      newHistory.push('Available commands:', 'fold [data] - Execute MDB dimensional fold', 'unfold - Reconstruct data from coordinates', 'coords [bits] - View D3/D4/D5/PHI coordinates', 'superbit - Inspect local SuperBit registry', 'clear - Clear terminal');
    } else if (cmd.startsWith('coords ')) {
      const data = cmdInput.slice(7);
      const c = calculateCoordinates(data);
      newHistory.push(`D3 (Temporal): ${c.d3}`, `D4 (Density): ${c.d4}`, `D5 (Gravity): ${c.d5}`, `PHI (Weighted): ${c.phi}`);
    } else if (cmd.startsWith('fold ')) {
      const data = cmdInput.slice(5);
      const layers = fold(data);
      newHistory.push(`Folding complete: ${layers.length} dimensions compressed.`, `Final size: ${layers[layers.length-1].residual.length} bits.`);
    } else if (cmd === 'superbit') {
       newHistory.push('Local Registry:', '- Node alpha-1: Stable', '- Node alpha-2: Synchronizing', '- Superposition locked.');
    } else if (cmd === 'clear') {
      setHistory([]);
      setInput('');
      return;
    } else {
      newHistory.push(`Command not found: ${cmd}`);
    }

    setHistory(newHistory);
    setInput('');
  };

  return (
    <div className="font-mono text-sm h-full flex flex-col">
      <div className="flex-1 overflow-auto space-y-1">
        {history.map((line, i) => (
          <div key={i} className={line.startsWith('>') ? 'text-blue-400' : 'text-green-500/80'}>{line}</div>
        ))}
      </div>
      <form onSubmit={handleCommand} className="mt-2 flex">
        <span className="text-blue-400 mr-2">$</span>
        <input 
          autoFocus
          className="flex-1 bg-transparent border-none outline-none text-white italic"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </form>
    </div>
  );
};

const SecurityAgent: React.FC = () => {
  const [analysis, setAnalysis] = useState<ThreatAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [logs, setLogs] = useState<string[]>(['[INF] MDB Security Agent Initialized', '[INF] Live Threat Intel Sync: Connected', '[INF] Watching /dev/mdb for unauthorized access.']);

  const runAnalysis = async () => {
    setIsAnalyzing(true);
    setLogs(prev => [...prev, '[WRN] Initiating deep scan...']);
    const mockLog = logs.join('\n');
    const result = await analyzeThreat(mockLog);
    setAnalysis(result);
    setLogs(prev => [...prev, `[INF] Analysis complete. Threat level: ${result.threatLevel}%`]);
    setIsAnalyzing(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Shield className={analysis && analysis.threatLevel > 30 ? "text-red-500" : "text-green-500"} size={32} />
            <motion.div 
              animate={{ scale: [1, 1.2, 1] }} 
              transition={{ repeat: Infinity, duration: 2 }} 
              className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${analysis && analysis.threatLevel > 30 ? "bg-red-500" : "bg-green-500"}`}
            />
          </div>
          <div>
            <div className="font-bold">Dimensional Integrity: {isAnalyzing ? "SCANNING..." : (analysis?.threatLevel || 0) > 30 ? "VULNERABLE" : "LOCKED"}</div>
            <div className="text-xs opacity-50">Global Intelligence Sharing: ENABLED</div>
          </div>
        </div>
        <button 
          onClick={runAnalysis}
          disabled={isAnalyzing}
          className="mdb-button bg-blue-600 text-sm hover:bg-blue-700 disabled:opacity-30"
        >
          {isAnalyzing ? "Processing..." : "Deep Scan"}
        </button>
      </div>

      <AnimatePresence>
        {analysis && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20 space-y-2"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-blue-400 flex items-center gap-2"><Activity size={12}/> THREAT ANALYSIS</span>
              <span className="text-sm font-mono">{analysis.threatLevel}%</span>
            </div>
            <p className="text-sm italic text-white/80">"{analysis.analysis}"</p>
            <div className="text-[10px] uppercase font-bold text-white/40">Recommendation: <span className="text-white/60">{analysis.recommendation}</span></div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Integrity', value: '100%', icon: Shield },
          { label: 'SuperBits', value: 'Stable', icon: Layers },
          { label: 'Intelligence', value: 'Live', icon: Globe }
        ].map((stat, i) => (
          <div key={i} className="p-3 bg-white/5 rounded-lg border border-white/5 flex flex-col items-center gap-1">
            <stat.icon size={16} className="text-blue-400" />
            <div className="text-[10px] uppercase opacity-50 tracking-widest">{stat.label}</div>
            <div className="text-sm font-bold">{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="bg-black/40 rounded-xl p-4 font-mono text-xs overflow-auto h-40 border border-white/5">
        <div className="opacity-40 mb-2 border-b border-white/10 pb-1 uppercase tracking-widest">Live Security Intelligence</div>
        {logs.map((log, i) => (
          <div key={i} className="mb-1">{log}</div>
        ))}
      </div>
    </div>
  );
};

const FileExplorer: React.FC = () => {
  const [files, setFiles] = useState([
    { name: 'kernel_core.md', size: '2KB', type: 'doc' },
    { name: 'dimensional_map.bin', size: '1.4MB', type: 'bin' },
    { name: 'phi_constant.txt', size: '128B', type: 'doc' },
    { name: 'superbit_registry', size: 'dir', type: 'dir' },
    { name: 'fold_engine.sys', size: '44KB', type: 'bin' },
    { name: 'unfold_map.mdb', size: '8KB', type: 'doc' }
  ]);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-4 mb-4 text-xs opacity-60">
        <div className="flex items-center gap-1 px-3 py-1 bg-white/5 rounded-md border border-white/10">
          <HardDrive size={12} /> mdbfs://root/
        </div>
        <div className="flex-1 border-b border-white/10 h-px" />
      </div>
      <div className="grid grid-cols-4 gap-4">
        {files.map((file, i) => (
          <motion.div 
            whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.05)' }}
            key={i} 
            className="flex flex-col items-center p-4 rounded-xl cursor-pointer group border border-transparent hover:border-white/5"
          >
            <div className="text-blue-400 group-hover:text-blue-300 transition-colors">
              {file.type === 'dir' ? <Folder size={48} /> : <FileText size={48} />}
            </div>
            <div className="text-xs mt-2 font-medium truncate w-full text-center">{file.name}</div>
            <div className="text-[10px] opacity-40 uppercase">{file.size}</div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

const DimensionalFoldTool: React.FC = () => {
  const [data, setData] = useState('');
  const [folded, setFolded] = useState<FoldedLayer[]>([]);
  
  const handleFold = () => {
    if (!data) return;
    const result = fold(data);
    setFolded(result);
  };

  return (
    <div className="grid grid-cols-2 h-full gap-4">
      <div className="flex flex-col gap-4">
        <div className="text-xs uppercase font-bold opacity-40 tracking-widest flex items-center gap-2"><Scaling size={12}/> Input Data Buffer</div>
        <textarea 
          className="flex-1 bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-sm outline-none focus:border-blue-500/50 transition-colors"
          placeholder="Paste binary or text to fold..."
          value={data}
          onChange={(e) => setData(e.target.value)}
        />
        <button onClick={handleFold} className="mdb-button bg-blue-600 hover:bg-blue-700">Execute Fold</button>
      </div>
      <div className="flex flex-col gap-4">
        <div className="text-xs uppercase font-bold opacity-40 tracking-widest flex items-center gap-2"><Layers size={12}/> Dimensional Layers</div>
        <div className="flex-1 bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-xs overflow-auto space-y-2">
          {folded.length === 0 ? (
            <div className="h-full flex items-center justify-center opacity-20 italic">No active fold</div>
          ) : (
            folded.map((layer, i) => (
              <div key={i} className="p-2 bg-white/5 rounded-lg border border-white/5">
                <div className="text-blue-400 font-bold mb-1">Dimension {i + 1}</div>
                <div className="grid grid-cols-2 gap-1 text-[10px] opacity-60">
                  <div>D3: {layer.coords.d3}</div>
                  <div>D4: {layer.coords.d4}</div>
                  <div>D5: {layer.coords.d5}</div>
                  <div>PHI: {layer.coords.phi}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

interface AppEntry {
  id: string;
  name: string;
  description: string;
  version: string;
  icon: string;
  size: string;
  category: string;
}

const AppStore: React.FC<{ installed: string[], onInstall: (id: string) => void, onUninstall: (id: string) => void }> = ({ installed, onInstall, onUninstall }) => {
  const [apps, setApps] = useState<AppEntry[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const fetchApps = useCallback(async (query: string = '') => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/apps${query ? `?q=${query}` : ''}`);
      const data = await res.json();
      setApps(data);
    } catch (e) {
      console.error("Failed to fetch apps", e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchApps();
  }, [fetchApps]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchApps(search);
  };

  const getIcon = (name: string) => {
    switch (name) {
      case 'Music': return <Music size={24} />;
      case 'ImageIcon': return <ImageIcon size={24} />;
      case 'FileText': return <FileText size={24} />;
      case 'Globe': return <Globe size={24} />;
      case 'Camera': return <Camera size={24} />;
      default: return <Box size={24} />;
    }
  };

  return (
    <div className="flex flex-col h-full gap-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-widest text-blue-400 flex items-center gap-2">
          <ShoppingBag size={24} /> MDB PACKAGE REPOSITORY
        </h2>
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 opacity-40" size={16} />
            <input 
              className="bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm focus:border-blue-500/50 outline-none transition-all w-64"
              placeholder="Search dimensional apps..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <button type="submit" className="mdb-button bg-blue-600 px-6">Search</button>
        </form>
      </div>

      {isLoading ? (
        <div className="flex-1 flex items-center justify-center opacity-30 italic">Syncing with remote repository...</div>
      ) : (
        <div className="grid grid-cols-2 gap-4 overflow-auto pb-4">
          {apps.map(app => (
            <div key={app.id} className="glass-morphism p-4 rounded-xl border border-white/10 flex gap-4 hover:border-blue-500/30 transition-all">
              <div className="w-16 h-16 bg-blue-500/10 rounded-xl flex items-center justify-center text-blue-400">
                {getIcon(app.icon)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <h3 className="font-bold truncate">{app.name}</h3>
                  <span className="text-[10px] bg-white/5 px-2 py-0.5 rounded border border-white/10 opacity-60">v{app.version}</span>
                </div>
                <p className="text-xs opacity-50 line-clamp-2 mt-1">{app.description}</p>
                <div className="flex items-center justify-between mt-3">
                  <span className="text-[10px] opacity-40 uppercase tracking-tighter">{app.category} • {app.size}</span>
                  {installed.includes(app.id) ? (
                    <div className="flex gap-2">
                      <button 
                        onClick={() => onUninstall(app.id)}
                        className="text-[10px] font-bold text-red-400 hover:text-red-300 transition-colors uppercase tracking-widest"
                      >
                        Uninstall
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={() => onInstall(app.id)}
                      className="mdb-button bg-blue-600 py-1 text-[10px] uppercase font-bold tracking-widest"
                    >
                      Install
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-auto p-4 bg-white/5 rounded-xl border border-white/10 flex items-center justify-between">
        <div className="text-xs opacity-50 flex items-center gap-2">
          <Info size={14} /> System status: Secure // All packages verified by Security Agent
        </div>
        <div className="flex gap-4">
          <button onClick={() => fetchApps()} className="text-xs text-blue-400 hover:underline flex items-center gap-1">
            <RotateCcw size={12} /> Refresh
          </button>
        </div>
      </div>
    </div>
  );
};

const QuantumLab: React.FC = () => {
  const [isSimulating, setIsSimulating] = useState(false);
  const [stableNodes, setStableNodes] = useState(0);

  const startSimulation = () => {
    setIsSimulating(true);
    let count = 0;
    const interval = setInterval(() => {
      count++;
      setStableNodes(count);
      if (count >= 100) {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 50);
  };

  return (
    <div className="flex flex-col h-full gap-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="glass-morphism p-4 rounded-xl border border-white/10">
          <div className="text-[10px] uppercase font-bold text-blue-400 mb-2">Bridge Stability</div>
          <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
            <motion.div 
              animate={{ width: `${stableNodes}%` }}
              className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
            />
          </div>
          <div className="mt-2 text-xs font-mono opacity-60">Phase Lock: {stableNodes}%</div>
        </div>
        <div className="glass-morphism p-4 rounded-xl border border-white/10">
          <div className="text-[10px] uppercase font-bold text-blue-400 mb-2">Sim Node Affinity</div>
          <div className="text-xl font-mono">0.1618 PHI</div>
        </div>
      </div>
      <div className="flex-1 bg-black/40 border border-white/10 rounded-xl p-6 relative overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div 
            animate={isSimulating ? { rotate: 360, scale: [1, 1.2, 1] } : {}}
            transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            className="w-48 h-48 border-2 border-blue-500/20 rounded-full border-dashed"
          />
          <div className="absolute w-24 h-24 bg-blue-500/10 blur-3xl rounded-full" />
          <Cpu className={`text-blue-400 ${isSimulating ? 'animate-pulse' : ''}`} size={48} />
        </div>
        <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end">
          <div className="text-[10px] font-mono opacity-30">
            STRAT: MDB_QUANTUM_RECON_V1<br/>
            TARGET: SUBSPACE_COLLAPSE_VERIFY
          </div>
          <button 
            onClick={startSimulation}
            disabled={isSimulating}
            className="mdb-button bg-blue-600 px-8 py-2 disabled:opacity-30"
          >
            {isSimulating ? 'RUNNING BRIDGE...' : 'START SIMULATION'}
          </button>
        </div>
      </div>
    </div>
  );
};

const FirefoxApp: React.FC = () => (
  <div className="flex flex-col h-full">
    <div className="h-10 bg-[#2b2a33] border-b border-white/5 flex items-center px-4 gap-2 shrink-0">
      <div className="flex gap-2">
        <ArrowLeft size={14} className="text-white/40" />
        <ArrowRight size={14} className="text-white/40" />
        <RotateCcw size={14} className="text-white/40" />
      </div>
      <div className="flex-1 bg-[#1c1b22] rounded-md px-3 py-1 text-[11px] text-white/60 flex items-center justify-between border border-white/10">
        <span>https://www.mozilla.org/firefox</span>
        <Shield size={10} className="text-blue-400" />
      </div>
    </div>
    <div className="flex-1 p-8 text-center space-y-6 overflow-auto bg-[#1c1b22]">
      <div className="w-20 h-20 bg-gradient-to-tr from-orange-600 to-yellow-400 rounded-full mx-auto flex items-center justify-center p-4">
        <Globe size={48} className="text-white shadow-lg" />
      </div>
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Mozilla Firefox</h2>
        <p className="text-[10px] text-white/30 uppercase tracking-[0.3em] font-mono mt-2">CLASSIC BINARY / x64 KERNEL BRIDGE</p>
      </div>
      <div className="w-full max-w-2xl mx-auto p-4 bg-white/5 rounded-lg text-left space-y-2 border border-white/5 font-sans">
        <div className="h-4 w-3/4 bg-white/10 rounded animate-pulse" />
        <div className="h-4 w-1/2 bg-white/10 rounded animate-pulse" />
        <div className="h-20 w-full bg-white/5 rounded mt-4 flex items-center justify-center text-[10px] text-white/20 italic">
          High Performance Rendering Engine Active
        </div>
      </div>
    </div>
  </div>
);

const LibreOfficeApp: React.FC = () => (
  <div className="flex flex-col h-full bg-[#f0f0f0] text-gray-800">
    <div className="h-8 bg-gray-200 border-b border-gray-300 flex items-center px-4 gap-4 text-[11px] shrink-0">
      <span className="font-bold">File</span>
      <span>Edit</span>
      <span>View</span>
      <span>Insert</span>
      <span>Format</span>
      <span>Tools</span>
    </div>
    <div className="h-10 bg-gray-100 border-b border-gray-300 flex items-center px-4 gap-2 shrink-0">
      <FileText size={16} className="text-blue-600" />
      <div className="h-6 w-32 bg-white border border-gray-300 rounded px-2 flex items-center text-[10px]">Liberation Sans</div>
      <div className="h-6 w-12 bg-white border border-gray-300 rounded px-2 flex items-center text-[10px]">12</div>
    </div>
    <div className="flex-1 p-12 overflow-auto flex justify-center bg-gray-300 shadow-inner">
      <div className="w-[595px] h-[842px] bg-white shadow-2xl p-20 relative">
        <div className="absolute top-10 left-10 text-[10px] text-blue-500/50 uppercase font-mono">Classic Application Runner</div>
        <div className="space-y-4">
          <div className="h-2 w-full bg-gray-100 rounded" />
          <div className="h-2 w-full bg-gray-100 rounded" />
          <div className="h-2 w-3/4 bg-gray-100 rounded" />
          <div className="h-2 w-full bg-gray-100 rounded" />
          <div className="h-32 w-full bg-gray-50 rounded border border-dashed border-gray-200 flex items-center justify-center text-xs text-gray-400">
            LibreOffice Writer v7.6
          </div>
        </div>
      </div>
    </div>
  </div>
);

const VLCApp: React.FC = () => (
  <div className="flex flex-col h-full bg-black">
    <div className="flex-1 flex items-center justify-center relative group">
      <div className="w-32 h-32 text-orange-500 opacity-20 group-hover:opacity-40 transition-opacity">
        <Music size={128} />
      </div>
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-6 text-white/50">
        <Play size={24} className="hover:text-white cursor-pointer" />
        <div className="w-64 h-1 bg-white/20 rounded-full relative">
          <div className="absolute inset-y-0 left-0 w-1/3 bg-orange-500 rounded-full" />
        </div>
        <span className="text-[10px] font-mono tracking-tighter">04:20 / 12:45</span>
      </div>
    </div>
    <div className="h-10 bg-[#212121] flex items-center justify-between px-4 text-[10px] text-white/40 uppercase tracking-widest font-mono border-t border-white/5">
      <span>VLC Media Player</span>
      <div className="flex gap-4">
        <span>Classic Mode</span>
        <span className="text-orange-500/50">HW: ACCEL</span>
      </div>
    </div>
  </div>
);

const SystemInformation: React.FC = () => {
  const [cpuUsage, setCpuUsage] = useState(12);
  const [ramUsage, setRamUsage] = useState(4.2);

  useEffect(() => {
    const interval = setInterval(() => {
      setCpuUsage(prev => Math.max(5, Math.min(95, prev + (Math.random() * 10 - 5))));
      setRamUsage(prev => Math.max(2, Math.min(16, prev + (Math.random() * 0.1 - 0.05))));
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 space-y-6 overflow-auto h-full">
      <div className="flex items-center gap-4 border-b border-white/10 pb-6">
        <div className="w-16 h-16 bg-blue-500/20 rounded-2xl flex items-center justify-center border border-blue-500/30">
          <Activity size={32} className="text-blue-400" />
        </div>
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white uppercase">System Information</h2>
          <p className="text-[10px] text-white/30 font-mono tracking-widest">MDB-OS Kernel v1.2.0-STABLE (x86_64/Δ)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Hardware Specs */}
        <div className="glass-morphism p-4 rounded-xl border border-white/10 space-y-4">
          <div className="text-[10px] uppercase font-bold text-blue-400 tracking-widest border-b border-white/5 pb-2">Hardware Specs</div>
          <div className="space-y-3">
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">CPU</span>
              <span className="font-mono">Intel(R) Core(TM) MDB-Hybrid @ 4.2GHz (16 Cores)</span>
            </div>
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">RAM</span>
              <span className="font-mono">32.0 GB DDR5 (Dimensional Buffer Enabled)</span>
            </div>
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">GPU</span>
              <span className="font-mono">MDB Vision Engine G3 (Vulkan 1.3)</span>
            </div>
          </div>
        </div>

        {/* Runtime Metrics */}
        <div className="glass-morphism p-4 rounded-xl border border-white/10 space-y-4">
          <div className="text-[10px] uppercase font-bold text-purple-400 tracking-widest border-b border-white/5 pb-2">Dimensional Core Status</div>
          <div className="space-y-3">
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">Active Layers</span>
              <span className="font-mono text-purple-400">D3, D4, D5, D12, D84</span>
            </div>
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">Fold Entropy</span>
              <span className="font-mono">0.1618033 (Stable Phi)</span>
            </div>
            <div className="flex justify-between text-[11px]">
              <span className="opacity-40">Space Factor</span>
              <span className="font-mono">15.4 PB / 1 TB physical</span>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="text-[10px] uppercase font-bold text-white/30 px-1">Resource Utilization</div>
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <div className="flex justify-between text-[9px] uppercase font-bold opacity-40">CPU Usage</div>
            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
              <motion.div animate={{ width: `${cpuUsage}%` }} className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" />
            </div>
            <div className="text-right text-[10px] font-mono opacity-60">{cpuUsage.toFixed(1)}%</div>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between text-[9px] uppercase font-bold opacity-40">Memory Usage</div>
            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
              <motion.div animate={{ width: `${(ramUsage / 16) * 100}%` }} className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" />
            </div>
            <div className="text-right text-[10px] font-mono opacity-60">{ramUsage.toFixed(1)} GB / 32 GB</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const GIMPApp: React.FC = () => (
  <div className="flex h-full bg-[#303030] text-white">
    <div className="w-12 bg-[#212121] border-r border-[#111] flex flex-col items-center py-4 gap-4">
      <ImageIcon size={20} className="opacity-60" />
      <div className="w-8 h-px bg-white/10" />
      <div className="flex flex-col gap-3">
        {[1,2,3,4,5].map(i => <div key={i} className="w-6 h-6 bg-white/5 rounded border border-white/5" />)}
      </div>
    </div>
    <div className="flex-1 flex flex-col">
      <div className="h-8 bg-[#212121] border-b border-[#111] flex items-center px-4 gap-4 text-[10px] uppercase tracking-wider opacity-60">
        <span>File</span><span>Edit</span><span>Select</span><span>View</span><span>Image</span><span>Layer</span>
      </div>
      <div className="flex-1 p-10 flex items-center justify-center bg-[#1a1a1a]">
        <div className="w-96 h-64 bg-[#2b2b2b] shadow-2xl border border-white/5 flex items-center justify-center flex-col gap-4">
          <ImageIcon size={48} className="text-white/10" />
          <span className="text-[10px] font-mono opacity-20 uppercase tracking-[0.5em]">Canvas Area [Classic Mode]</span>
        </div>
      </div>
    </div>
  </div>
);

const VSCodeApp: React.FC = () => (
  <div className="flex h-full bg-[#1e1e1e] text-[#cccccc] font-sans">
    <div className="w-12 bg-[#333333] flex flex-col items-center py-4 gap-6">
      <div className="text-blue-400"><FileCode size={24} /></div>
      <Search size={22} className="opacity-40" />
      <GitBranch size={22} className="opacity-40" />
      <Play size={22} className="opacity-40" />
    </div>
    <div className="w-48 bg-[#252526] border-r border-[#1e1e1e] p-3">
      <div className="text-[10px] uppercase font-bold opacity-40 mb-4 tracking-widest">Explorer</div>
      <div className="space-y-2 text-xs">
        <div className="flex items-center gap-2 opacity-80"><FileCode size={12} className="text-blue-400" /> main.cpp</div>
        <div className="flex items-center gap-2 opacity-40"><FileCode size={12} /> mdb_core.c</div>
        <div className="flex items-center gap-2 opacity-40"><Folder size={12} /> kernel</div>
      </div>
    </div>
    <div className="flex-1 flex flex-col">
      <div className="h-9 bg-[#2d2d2d] flex items-center px-4 border-b border-[#1e1e1e] gap-4">
        <div className="bg-[#1e1e1e] px-4 py-2 border-t-2 border-blue-500 text-xs">main.cpp</div>
      </div>
      <div className="flex-1 p-6 font-mono text-sm leading-relaxed overflow-auto">
        <div className="flex gap-4">
          <span className="opacity-20">1</span>
          <span><span className="text-blue-400">#include</span> <span className="text-orange-400">&lt;iostream&gt;</span></span>
        </div>
        <div className="flex gap-4">
          <span className="opacity-20">2</span>
          <span><span className="text-blue-400">#include</span> <span className="text-orange-400">&lt;mdb/kernel.h&gt;</span></span>
        </div>
        <div className="flex gap-4">
          <span className="opacity-20">3</span>
          <span />
        </div>
        <div className="flex gap-4">
          <span className="opacity-20">4</span>
          <span><span className="text-blue-400">int</span> <span className="text-yellow-400">main</span>() {"{"}</span>
        </div>
        <div className="flex gap-4">
          <span className="opacity-20">5</span>
          <span>&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-green-400">// Classic Mode execution</span></span>
        </div>
        <div className="flex gap-4">
          <span className="opacity-20">6</span>
          <span>&nbsp;&nbsp;&nbsp;&nbsp;std::cout &lt;&lt; <span className="text-orange-400">"MDB-OS Bridge Active"</span>;</span>
        </div>
      </div>
    </div>
  </div>
);

const SettingsPanel: React.FC = () => {
  const handleDownload = () => {
    window.location.href = '/api/export-source';
  };

  return (
    <div className="p-6 space-y-8 max-w-xl mx-auto">
      <div className="text-center space-y-2">
        <div className="w-16 h-16 bg-blue-500/10 rounded-2xl flex items-center justify-center mx-auto border border-blue-500/30">
          <Settings size={32} className="text-blue-400" />
        </div>
        <h2 className="text-xl font-bold tracking-widest mt-4 text-white uppercase">MDB Kernel Settings</h2>
        <p className="text-[10px] text-white/30 font-mono uppercase tracking-[0.2em]">Version 1.1.0 // Stable Release</p>
      </div>

      <div className="space-y-4">
        <div className="p-6 bg-blue-500/5 rounded-xl border border-blue-500/20 space-y-6">
          <div className="text-xs font-bold text-blue-400 uppercase tracking-widest flex items-center gap-2">
            <Download size={14} /> EXPORT SOURCE CODE
          </div>
          <p className="text-sm text-white/70 leading-relaxed">
            Download the complete MDB-OS source repository, including kernel modules, the Rust folding engine, and the UI source.
          </p>
          
          <button 
            onClick={handleDownload}
            className="w-full mdb-button bg-blue-600 hover:bg-blue-700 py-3 text-sm font-bold flex items-center justify-center gap-3 transition-colors shadow-[0_0_15px_rgba(59,130,246,0.2)]"
          >
            <Download size={18} /> DOWNLOAD .ZIP SOURCE
          </button>

          <div className="bg-black/40 p-4 rounded-lg border border-white/5 text-[10px] font-mono text-white/30 leading-normal">
            INCLUDES:<br/>
            - kernel/mdb_core.c (Folding logic)<br/>
            - main.rs (Rust engine)<br/>
            - scripts/make_iso.sh (ISO Build)<br/>
            - server.ts & src/App.tsx (OS Interface)
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="text-[10px] uppercase font-bold text-white/30 mb-1 tracking-widest">Base Arch</div>
            <div className="text-xs font-bold font-mono">MULTI-ARCH</div>
          </div>
          <div className="p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="text-[10px] uppercase font-bold text-white/30 mb-1 tracking-widest">Entropy</div>
            <div className="text-xs font-bold font-mono">PHI-LOCK</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
const App: React.FC = () => {
  const [openWindows, setOpenWindows] = useState<any[]>([]);
  const [focusedId, setFocusedId] = useState<string | null>(null);
  const [time, setTime] = useState(new Date());
  const [installedApps, setInstalledApps] = useState<string[]>([]);

  const handleInstall = async (id: string) => {
    try {
      const res = await fetch('/api/apps/install', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ appId: id })
      });
      if (res.ok) {
        setInstalledApps(prev => [...prev, id]);
      }
    } catch (e) {
      console.error("Installation failed", e);
    }
  };

  const handleUninstall = (id: string) => {
    setInstalledApps(prev => prev.filter(a => a !== id));
  };

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const openApp = (id: string, title: string, icon: any, content: any, mode?: string) => {
    if (openWindows.find(w => w.id === id)) {
      setFocusedId(id);
      const maxZ = openWindows.length > 0 ? Math.max(...openWindows.map(win => win.zIndex)) : 0;
      setOpenWindows(openWindows.map(w => 
        w.id === id ? { ...w, zIndex: maxZ + 1 } : w
      ));
      return;
    }
    const newWindow = { id, title, mode, icon, content, isOpen: true, isMaximized: false, zIndex: openWindows.length + 1 };
    setOpenWindows([...openWindows, newWindow]);
    setFocusedId(id);
  };

  const closeWindow = (id: string) => {
    setOpenWindows(openWindows.filter(w => w.id !== id));
    if (focusedId === id) setFocusedId(null);
  };

  const focusWindow = (id: string) => {
    setFocusedId(id);
    const maxZ = openWindows.length > 0 ? Math.max(...openWindows.map(win => win.zIndex)) : 0;
    setOpenWindows(openWindows.map(w => 
      w.id === id ? { ...w, zIndex: maxZ + 1 } : w
    ));
  };

  const apps = [
    { id: 'browser', title: 'Firefox', icon: <Globe size={20} />, content: <FirefoxApp />, mode: 'Classic' },
    { id: 'code', title: 'VS Code', icon: <FileCode size={20} />, content: <VSCodeApp />, mode: 'Classic' },
    { id: 'gimp', title: 'GIMP', icon: <ImageIcon size={20} />, content: <GIMPApp />, mode: 'Classic' },
    { id: 'libreoffice', title: 'LibreOffice', icon: <FileText size={20} />, content: <LibreOfficeApp />, mode: 'Classic' },
    { id: 'vlc', title: 'VLC Player', icon: <Music size={20} />, content: <VLCApp />, mode: 'Classic' },
    { id: 'system', title: 'System Info', icon: <Activity size={20} />, content: <SystemInformation />, mode: 'Classic' },
    { id: 'terminal', title: 'Terminal', icon: <Terminal size={20} />, content: <MDBTerminal />, mode: 'Classic' },
    { id: 'folder', title: 'Fold Engine', icon: <Scaling size={20} />, content: <DimensionalFoldTool />, mode: 'Dimensional' },
    { id: 'quantum', title: 'Quantum Lab', icon: <Cpu size={20} />, content: <QuantumLab />, mode: 'Dimensional' },
    { id: 'store', title: 'App Store', icon: <ShoppingBag size={20} />, content: <AppStore installed={installedApps} onInstall={handleInstall} onUninstall={handleUninstall} />, mode: 'Classic' },
    { id: 'settings', title: 'Settings', icon: <Settings size={20} />, content: <SettingsPanel />, mode: 'Classic' }
  ];

  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;

  return (
    <div className="h-screen w-screen overflow-hidden relative select-none bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-[#050505] to-black">
      {/* Background Decor */}
      <div className="absolute inset-0 scanline opacity-10 pointer-events-none" />
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-5 pointer-events-none" />
      
      {/* Desktop Grid */}
      <div className={`p-4 md:p-8 grid ${isMobile ? 'grid-cols-4' : 'grid-cols-1'} w-full md:w-fit gap-2 md:gap-8`}>
        {apps.map((app) => (
          <motion.div 
            key={app.id} 
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => openApp(app.id, app.title, app.icon, app.content, app.mode)}
            className="flex flex-col items-center gap-1 md:gap-2 cursor-pointer transition-all hover:bg-white/5 p-2 md:p-4 rounded-xl md:rounded-2xl"
          >
            <div className="w-12 h-12 md:w-16 md:h-16 glass-morphism rounded-xl md:rounded-2xl flex items-center justify-center text-blue-400 shadow-xl border-white/20 relative">
              {React.cloneElement(app.icon, { size: isMobile ? 24 : 32 })}
              <div className={`absolute -top-1 -right-1 w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-bold border ${app.mode === 'Dimensional' ? 'bg-purple-500 border-purple-400 text-white' : 'bg-blue-500 border-blue-400 text-white'}`}>
                {app.mode === 'Dimensional' ? 'Δ' : 'C'}
              </div>
            </div>
            <span className="text-[8px] md:text-[10px] font-bold tracking-[0.1em] md:tracking-[0.2em] opacity-80 uppercase text-center leading-tight">
              {isMobile ? app.id : app.title}
            </span>
          </motion.div>
        ))}
      </div>

      {/* Windows Layer */}
      <AnimatePresence>
        {openWindows.map((win) => (
          <Window 
            key={win.id}
            {...win}
            onClose={closeWindow}
            onFocus={focusWindow}
            onMinimize={() => {}} 
          />
        ))}
      </AnimatePresence>

      {/* Taskbar */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 h-14 w-fit px-4 glass-morphism rounded-2xl flex items-center gap-3 window-shadow">
        <button className="p-2 rounded-xl hover:bg-white/10 text-blue-400">
          <Monitor size={20} />
        </button>
        <div className="h-6 w-px bg-white/10 mx-2" />
        {apps.map((app) => (
          <button 
            key={app.id}
            onClick={() => openApp(app.id, app.title, app.icon, app.content, app.mode)}
            className={`p-2 rounded-xl transition-all ${focusedId === app.id ? 'bg-blue-500/20 text-blue-400' : 'hover:bg-white/5 opacity-60'}`}
          >
            {React.cloneElement(app.icon, { size: 24 })}
          </button>
        ))}
        <div className="h-6 w-px bg-white/10 mx-2" />
        <div className="flex items-center gap-6 px-2 text-[10px] font-mono tracking-widest uppercase opacity-60">
          <div className="flex items-center gap-2"><Wifi size={14} className="text-blue-400"/></div>
          <div className="flex items-center gap-2">
            {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </div>
        </div>
      </div>

      {/* Boot Animation Overlay */}
      <motion.div 
        initial={{ opacity: 1 }}
        animate={{ opacity: 0 }}
        transition={{ delay: 1.5, duration: 0.8 }}
        className="absolute inset-0 bg-black z-[9999] pointer-events-none flex flex-col items-center justify-center gap-6"
      >
        <motion.div 
          animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="relative"
        >
          <Box size={64} className="text-blue-500" />
          <motion.div 
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 3, ease: "linear" }}
            className="absolute -inset-4 border-2 border-dashed border-blue-500/30 rounded-full"
          />
        </motion.div>
        <div className="font-mono text-blue-500 tracking-[0.8em] text-lg font-bold ml-4">MDB OS</div>
        <div className="text-white/20 text-[10px] font-mono tracking-[0.3em] uppercase">Dimensional Kernel v1.1.0 // Authored by Ryan</div>
      </motion.div>
    </div>
  );
};

export default App;
