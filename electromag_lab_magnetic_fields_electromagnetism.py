<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ElectroMag Lab | Magnetic Fields & Electromagnetism</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- Font Awesome for crisp scientific & UI icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- MathJax for clean physics formulas -->
    <script>
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\(', '\\)']] },
            svg: { fontCache: 'global' }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        slate: {
                            850: '#152033',
                            900: '#0f172a',
                            950: '#090d16',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }

        /* Subtle scientific grid background */
        .bg-lab-grid {
            background-size: 32px 32px;
            background-image: 
                linear-gradient(to right, rgba(6, 182, 212, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(6, 182, 212, 0.05) 1px, transparent 1px);
        }

        /* Glowing accents */
        .glow-cyan { box-shadow: 0 0 20px rgba(6, 182, 212, 0.25); }
        .glow-amber { box-shadow: 0 0 20px rgba(245, 158, 11, 0.25); }
        .glow-purple { box-shadow: 0 0 20px rgba(139, 92, 246, 0.25); }

       input[type=range] {
    appearance: none;
    -webkit-appearance: none;
    background: transparent;
}
        
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 6px;
            cursor: pointer;
            background: #1e293b;
            border-radius: 999px;
            border: 1px solid #334155;
        }
        input[type=range]::-webkit-slider-thumb {
            height: 18px;
            width: 18px;
            border-radius: 50%;
            background: #06b6d4;
            cursor: pointer;
            -webkit-appearance: none;
            margin-top: -7px;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.8);
            transition: transform 0.15s ease, background-color 0.15s ease;
        }
        input[type=range]::-webkit-slider-thumb:hover {
            transform: scale(1.15);
            background: #22d3ee;
        }

        /* Canvas container */
        .sim-canvas {
            display: block;
            width: 100%;
            height: 100%;
            touch-action: none; /* Prevent scrolling while dragging probes/magnets on touch devices */
            cursor: grab;
        }
        .sim-canvas:active {
            cursor: grabbing;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }

        @keyframes pulseGlow {
            0%, 100% { opacity: 0.85; }
            50% { opacity: 1; }
        }
        .animate-pulse-slow {
            animation: pulseGlow 3s infinite ease-in-out;
        }
    </style>
</head>
<body class="bg-lab-grid min-h-screen flex flex-col selection:bg-cyan-500/30 selection:text-cyan-200">

    <!-- Top Navigation Bar -->
    <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row items-center justify-between py-3 md:h-20 gap-3">
                <!-- Brand Logo -->
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center shadow-lg glow-cyan">
                        <i class="fa-solid fa-magnet text-white text-xl"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-purple-400 bg-clip-text text-transparent">
                            ElectroMag Lab
                        </h1>
                        <p class="text-[11px] text-slate-400 font-mono tracking-wider uppercase">Interactive Physics Sandbox</p>
                    </div>
                </div>

                <!-- Main Navigation Tabs -->
                <nav class="flex items-center bg-slate-950/80 p-1.5 rounded-2xl border border-slate-800 w-full md:w-auto justify-between md:justify-start gap-1">
                    <button onclick="switchMainTab('lab')" id="tab-btn-lab" class="main-tab flex-1 md:flex-none flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm">
                        <i class="fa-solid fa-flask"></i>
                        <span>1. Interactive Lab</span>
                    </button>
                    <button onclick="switchMainTab('concepts')" id="tab-btn-concepts" class="main-tab flex-1 md:flex-none flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent">
                        <i class="fa-solid fa-book-open"></i>
                        <span>2. Concept Explorer</span>
                    </button>
                    <button onclick="switchMainTab('quiz')" id="tab-btn-quiz" class="main-tab flex-1 md:flex-none flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent">
                        <i class="fa-solid fa-trophy"></i>
                        <span>3. Knowledge Quiz</span>
                    </button>
                </nav>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">

        <!-- ========================================================= -->
        <!-- TAB 1: INTERACTIVE LAB (3 SIMULATORS)                     -->
        <!-- ========================================================= -->
        <section id="section-lab" class="space-y-6">
            <!-- Simulator Selector Pills -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <button onclick="switchSim('bar')" id="sim-btn-bar" class="sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-800/90 border-cyan-500/60 glow-cyan">
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center shrink-0">
                        <i class="fa-solid fa-compass text-lg"></i>
                    </div>
                    <div>
                        <div class="text-xs font-mono text-cyan-400 uppercase">Simulator A</div>
                        <div class="font-bold text-slate-100 text-sm sm:text-base">Bar Magnet & Field Lines</div>
                    </div>
                </button>

                <button onclick="switchSim('solenoid')" id="sim-btn-solenoid" class="sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-900/70 border-slate-800 hover:border-slate-700">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
                        <i class="fa-solid fa-bolt text-lg"></i>
                    </div>
                    <div>
                        <div class="text-xs font-mono text-amber-400 uppercase">Simulator B</div>
                        <div class="font-bold text-slate-100 text-sm sm:text-base">Electromagnet & Solenoid</div>
                    </div>
                </button>

                <button onclick="switchSim('faraday')" id="sim-btn-faraday" class="sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-900/70 border-slate-800 hover:border-slate-700">
                    <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center shrink-0">
                        <i class="fa-solid fa-lightbulb text-lg"></i>
                    </div>
                    <div>
                        <div class="text-xs font-mono text-purple-400 uppercase">Simulator C</div>
                        <div class="font-bold text-slate-100 text-sm sm:text-base">Faraday's Induction</div>
                    </div>
                </button>
            </div>

            <!-- SIMULATOR A: BAR MAGNET & FIELD LINES -->
            <div id="sim-container-bar" class="sim-panel grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Canvas Area -->
                <div class="lg:col-span-8 bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl flex flex-col">
                    <div class="px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
                        <span class="text-cyan-400 font-semibold flex items-center gap-2">
                            <i class="fa-solid fa-hand-pointer"></i> Drag the Bar Magnet or Compass Probe anywhere on canvas
                        </span>
                        <div class="flex items-center gap-3 font-mono">
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span> North (N)</span>
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span> South (S)</span>
                        </div>
                    </div>
                    <div class="relative w-full h-[380px] sm:h-[460px]">
                        <canvas id="canvas-bar" class="sim-canvas"></canvas>
                    </div>
                </div>

                <!-- Controls & Telemetry -->
                <div class="lg:col-span-4 bg-slate-900/90 rounded-2xl border border-slate-800 p-5 flex flex-col justify-between space-y-5">
                    <div class="space-y-4">
                        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                            <h2 class="font-bold text-lg text-slate-100">Field Controls</h2>
                            <span class="px-2.5 py-1 rounded-full text-xs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">Dipole Model</span>
                        </div>

                        <!-- Live Probe Readout -->
                        <div class="bg-slate-950/90 rounded-xl p-4 border border-slate-800 space-y-3">
                            <div class="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center justify-between">
                                <span><i class="fa-solid fa-satellite-dish text-cyan-400 mr-1.5"></i>Compass Probe Sensor</span>
                                <span class="text-emerald-400 animate-pulse">● LIVE</span>
                            </div>
                            <div class="grid grid-cols-2 gap-3">
                                <div class="bg-slate-900 p-3 rounded-lg border border-slate-800/80">
                                    <div class="text-xs text-slate-400">Field Strength ($B$)</div>
                                    <div id="bar-readout-b" class="text-xl font-mono font-bold text-cyan-400 mt-0.5">14.2 mT</div>
                                </div>
                                <div class="bg-slate-900 p-3 rounded-lg border border-slate-800/80">
                                    <div class="text-xs text-slate-400">Field Angle ($\theta$)</div>
                                    <div id="bar-readout-angle" class="text-xl font-mono font-bold text-amber-400 mt-0.5">0.0°</div>
                                </div>
                            </div>
                        </div>

                        <!-- Toggles -->
                        <div class="space-y-3 pt-1">
                            <label class="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700/60 cursor-pointer hover:bg-slate-800 transition">
                                <span class="text-sm font-medium text-slate-200"><i class="fa-solid fa-wave-square text-cyan-400 w-5"></i> Show Field Lines</span>
                                <input type="checkbox" id="bar-toggle-lines" checked class="w-4 h-4 accent-cyan-500 rounded cursor-pointer">
                            </label>

                            <label class="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700/60 cursor-pointer hover:bg-slate-800 transition">
                                <span class="text-sm font-medium text-slate-200"><i class="fa-solid fa-border-all text-purple-400 w-5"></i> Show Compass Grid</span>
                                <input type="checkbox" id="bar-toggle-grid" checked class="w-4 h-4 accent-cyan-500 rounded cursor-pointer">
                            </label>
                        </div>

                        <!-- Magnet Strength Slider -->
                        <div class="space-y-1.5 pt-1">
                            <div class="flex justify-between text-xs font-medium">
                                <span class="text-slate-300">Magnet Strength</span>
                                <span id="bar-strength-val" class="font-mono text-cyan-400">100%</span>
                            </div>
                            <input type="range" id="bar-strength" min="25" max="150" value="100" class="w-full">
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="grid grid-cols-2 gap-3 pt-2">
                        <button onclick="flipBarMagnet()" class="py-2.5 px-4 rounded-xl bg-gradient-to-r from-red-500/20 to-blue-500/20 hover:from-red-500/30 hover:to-blue-500/30 border border-slate-700 text-slate-100 font-semibold text-sm transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-arrows-rotate text-cyan-400"></i> Flip Polarity
                        </button>
                        <button onclick="resetBarMagnet()" class="py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 font-semibold text-sm transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-rotate-left"></i> Reset
                        </button>
                    </div>
                </div>
            </div>

            <!-- SIMULATOR B: ELECTROMAGNET & SOLENOID BUILDER -->
            <div id="sim-container-solenoid" class="sim-panel hidden grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Canvas Area -->
                <div class="lg:col-span-8 bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl flex flex-col">
                    <div class="px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
                        <span class="text-amber-400 font-semibold flex items-center gap-2">
                            <i class="fa-solid fa-sliders"></i> Adjust Current, Turns & Core Material to lift steel paperclips!
                        </span>
                        <span class="font-mono text-slate-400">Formula: $B = \mu_0 \mu_r \left(\frac{N}{L}\right) I$</span>
                    </div>
                    <div class="relative w-full h-[380px] sm:h-[460px]">
                        <canvas id="canvas-solenoid" class="sim-canvas !cursor-default"></canvas>
                    </div>
                </div>

                <!-- Controls & Telemetry -->
                <div class="lg:col-span-4 bg-slate-900/90 rounded-2xl border border-slate-800 p-5 flex flex-col justify-between space-y-4">
                    <div class="space-y-4">
                        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                            <h2 class="font-bold text-lg text-slate-100">Solenoid Parameters</h2>
                            <span class="px-2.5 py-1 rounded-full text-xs font-mono bg-amber-500/10 text-amber-400 border border-amber-500/30">DC Coil</span>
                        </div>

                        <!-- Live Telemetry -->
                        <div class="bg-slate-950/90 rounded-xl p-3.5 border border-slate-800 grid grid-cols-2 gap-3">
                            <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800/80">
                                <div class="text-[11px] text-slate-400">Core Field ($B$)</div>
                                <div id="sol-readout-b" class="text-lg font-mono font-bold text-amber-400 mt-0.5">0.0 mT</div>
                            </div>
                            <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800/80">
                                <div class="text-[11px] text-slate-400">Paperclips Lifted</div>
                                <div id="sol-readout-clips" class="text-lg font-mono font-bold text-cyan-400 mt-0.5">0 / 24</div>
                            </div>
                        </div>

                        <!-- Current Slider -->
                        <div class="space-y-1">
                            <div class="flex justify-between text-xs font-medium">
                                <span class="text-slate-300">Electric Current ($I$)</span>
                                <span id="sol-val-current" class="font-mono text-amber-400 font-bold">4.0 A</span>
                            </div>
                            <input type="range" id="sol-slider-current" min="0" max="10" step="0.5" value="4.0" class="w-full">
                        </div>

                        <!-- Turns Slider -->
                        <div class="space-y-1">
                            <div class="flex justify-between text-xs font-medium">
                                <span class="text-slate-300">Coil Turns ($N$)</span>
                                <span id="sol-val-turns" class="font-mono text-cyan-400 font-bold">40 Turns</span>
                            </div>
                            <input type="range" id="sol-slider-turns" min="10" max="100" step="5" value="40" class="w-full">
                        </div>

                        <!-- Core Material Dropdown -->
                        <div class="space-y-1.5">
                            <label class="block text-xs font-medium text-slate-300">Core Material ($\mu_r$ Permeability)</label>
                            <select id="sol-select-core" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                                <option value="1">Air Core (Vacuum / Non-magnetic) — μᵣ = 1</option>
                                <option value="200" selected>Soft Iron Core — μᵣ = 200</option>
                                <option value="500">High-Permeability Ferrite — μᵣ = 500</option>
                            </select>
                        </div>
                    </div>

                    <!-- Polarity Reversal -->
                    <div class="pt-2">
                        <button onclick="reverseSolenoidCurrent()" class="w-full py-2.5 px-4 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 font-semibold text-sm transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-arrow-right-arrow-left"></i> Reverse Battery Polarity (Right-Hand Rule)
                        </button>
                    </div>
                </div>
            </div>

            <!-- SIMULATOR C: FARADAY'S INDUCTION -->
            <div id="sim-container-faraday" class="sim-panel hidden grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Canvas Area -->
                <div class="lg:col-span-8 bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl flex flex-col">
                    <div class="px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
                        <span class="text-purple-400 font-semibold flex items-center gap-2">
                            <i class="fa-solid fa-arrows-left-right"></i> Drag the magnet rapidly through the copper coil to generate electricity!
                        </span>
                        <span class="font-mono text-slate-400">$\mathcal{E} = -N \frac{\Delta \Phi_B}{\Delta t}$</span>
                    </div>
                    <div class="relative w-full h-[380px] sm:h-[460px]">
                        <canvas id="canvas-faraday" class="sim-canvas"></canvas>
                    </div>
                </div>

                <!-- Controls & Telemetry -->
                <div class="lg:col-span-4 bg-slate-900/90 rounded-2xl border border-slate-800 p-5 flex flex-col justify-between space-y-4">
                    <div class="space-y-4">
                        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                            <h2 class="font-bold text-lg text-slate-100">Induction Lab</h2>
                            <span class="px-2.5 py-1 rounded-full text-xs font-mono bg-purple-500/10 text-purple-400 border border-purple-500/30">Lenz's Law</span>
                        </div>

                        <!-- Live Telemetry -->
                        <div class="bg-slate-950/90 rounded-xl p-4 border border-slate-800 space-y-3">
                            <div class="grid grid-cols-2 gap-3">
                                <div class="bg-slate-900 p-3 rounded-lg border border-slate-800/80">
                                    <div class="text-xs text-slate-400">Induced EMF ($\mathcal{E}$)</div>
                                    <div id="far-readout-emf" class="text-xl font-mono font-bold text-purple-400 mt-0.5">0.00 V</div>
                                </div>
                                <div class="bg-slate-900 p-3 rounded-lg border border-slate-800/80">
                                    <div class="text-xs text-slate-400">Magnetic Flux ($\Phi_B$)</div>
                                    <div id="far-readout-flux" class="text-xl font-mono font-bold text-cyan-400 mt-0.5">0.0 mWb</div>
                                </div>
                            </div>
                            <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/50">
                                <span class="text-amber-400 font-semibold">Observation:</span> <span id="far-status-text">Stationary magnet — zero change in flux ($\Delta\Phi_B = 0$), so no current is induced.</span>
                            </div>
                        </div>

                        <!-- Coil Loops Slider -->
                        <div class="space-y-1.5">
                            <div class="flex justify-between text-xs font-medium">
                                <span class="text-slate-300">Coil Loops ($N$)</span>
                                <span id="far-val-loops" class="font-mono text-purple-400 font-bold">3 Loops</span>
                            </div>
                            <input type="range" id="far-slider-loops" min="1" max="5" step="1" value="3" class="w-full">
                        </div>

                        <!-- Auto-Oscillate AC Generator Mode -->
                        <div class="pt-1">
                            <button onclick="toggleFaradayAuto()" id="far-btn-auto" class="w-full py-3 px-4 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/50 text-purple-300 font-semibold text-sm transition flex items-center justify-center gap-2">
                                <i class="fa-solid fa-wave-square"></i> <span id="far-auto-label">Start AC Auto-Oscillator</span>
                            </button>
                        </div>
                    </div>

                    <!-- Flip Magnet Button -->
                    <div class="pt-2">
                        <button onclick="flipFaradayMagnet()" class="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-semibold text-sm transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-arrows-rotate text-purple-400"></i> Flip Magnet Poles (N / S)
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================= -->
        <!-- TAB 2: CONCEPT EXPLORER (STUDY GUIDE)                     -->
        <!-- ========================================================= -->
        <section id="section-concepts" class="hidden space-y-6">
            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-extrabold text-slate-100">Core Principles of Electromagnetism</h2>
                    <p class="text-slate-400 text-sm mt-1">Master the fundamental laws governing magnetic fields, electric currents, and electromagnetic induction.</p>
                </div>
                <button onclick="switchMainTab('lab')" class="px-4 py-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-sm font-semibold hover:bg-cyan-500/30 transition shrink-0">
                    Test in Interactive Lab <i class="fa-solid fa-arrow-right ml-1.5"></i>
                </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Card 1: Magnetic Fields & Dipoles -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-cyan-500/50 transition rounded-2xl p-6 flex flex-col justify-between space-y-4">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <div class="w-12 h-12 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-xl">
                                <i class="fa-solid fa-magnet"></i>
                            </div>
                            <span class="text-xs font-mono uppercase px-2.5 py-1 rounded-full bg-slate-800 text-cyan-400">01 • Magnetism</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-100">Magnetic Fields & Dipoles</h3>
                        <p class="text-slate-300 text-sm leading-relaxed">
                            Every magnet is a <strong>dipole</strong> possessing both a North (N) and South (S) pole. Magnetic monopoles do not exist in isolation—cutting a magnet in half creates two smaller magnets.
                        </p>
                        <ul class="text-sm text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>Field lines emerge from the <strong>North pole</strong> and enter the <strong>South pole</strong> outside the magnet.</li>
                            <li>Line density indicates field strength ($B$), measured in <strong>Tesla (T)</strong>.</li>
                            <li>Opposite poles attract ($N \leftrightarrow S$); like poles repel ($N \leftrightarrow N$).</li>
                        </ul>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300 flex items-center justify-between">
                        <span>Dipole Axial Field:</span>
                        <span>$B \propto \frac{\mu_0 \cdot m}{2\pi r^3}$</span>
                    </div>
                </div>

                <!-- Card 2: Oersted's Discovery & Right-Hand Rule -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-amber-500/50 transition rounded-2xl p-6 flex flex-col justify-between space-y-4">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <div class="w-12 h-12 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 text-xl">
                                <i class="fa-solid fa-hand-point-up"></i>
                            </div>
                            <span class="text-xs font-mono uppercase px-2.5 py-1 rounded-full bg-slate-800 text-amber-400">02 • Electromagnetism</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-100">Oersted's Discovery & Right-Hand Rule</h3>
                        <p class="text-slate-300 text-sm leading-relaxed">
                            In 1820, Hans Christian Ørsted discovered that an electric current flowing through a wire deflects a nearby compass needle—proving that <strong>moving charges create magnetic fields</strong>.
                        </p>
                        <ul class="text-sm text-slate-400 space-y-1.5 list-disc list-inside">
                            <li><strong>Right-Hand Grip Rule (Wire):</strong> Point your right thumb in the direction of conventional current ($I$); your fingers curl in the direction of the circular magnetic field ($B$).</li>
                            <li><strong>Right-Hand Rule (Coil):</strong> Curl your fingers in the direction of coil current; your thumb points toward the electromagnet's <strong>North pole</strong>.</li>
                        </ul>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-amber-300 flex items-center justify-between">
                        <span>Ampère's Law (Long Wire):</span>
                        <span>$B = \frac{\mu_0 I}{2\pi r}$</span>
                    </div>
                </div>

                <!-- Card 3: Electromagnets & Solenoids -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 transition rounded-2xl p-6 flex flex-col justify-between space-y-4">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <div class="w-12 h-12 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-xl">
                                <i class="fa-solid fa-bolt"></i>
                            </div>
                            <span class="text-xs font-mono uppercase px-2.5 py-1 rounded-full bg-slate-800 text-emerald-400">03 • Solenoids</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-100">Electromagnets & Solenoids</h3>
                        <p class="text-slate-300 text-sm leading-relaxed">
                            A <strong>solenoid</strong> is a helical coil of wire that concentrates magnetic field lines inside its core into a strong, uniform field similar to a bar magnet—but controllable with electricity.
                        </p>
                        <ul class="text-sm text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>Increasing current ($I$) or turn density ($n = N/L$) linearly strengthens $B$.</li>
                            <li>Inserting a ferromagnetic core (like soft iron or ferrite) multiplies the magnetic field by its <strong>relative permeability ($\mu_r$)</strong>.</li>
                        </ul>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-emerald-300 flex items-center justify-between">
                        <span>Solenoid Core Field:</span>
                        <span>$B = \mu_0 \mu_r n I$</span>
                    </div>
                </div>

                <!-- Card 4: Faraday's Law & Lenz's Law -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-purple-500/50 transition rounded-2xl p-6 flex flex-col justify-between space-y-4">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <div class="w-12 h-12 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400 text-xl">
                                <i class="fa-solid fa-wave-square"></i>
                            </div>
                            <span class="text-xs font-mono uppercase px-2.5 py-1 rounded-full bg-slate-800 text-purple-400">04 • Induction</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-100">Faraday's Law & Lenz's Law</h3>
                        <p class="text-slate-300 text-sm leading-relaxed">
                            Michael Faraday demonstrated that a <strong>changing magnetic flux ($\Delta\Phi_B$)</strong> through a closed wire loop induces an electromotive force (voltage, $\mathcal{E}$) and electric current.
                        </p>
                        <ul class="text-sm text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>Faster relative motion between magnet and coil creates a larger voltage spike.</li>
                            <li><strong>Lenz's Law (the minus sign):</strong> The induced current creates a magnetic field that <em>opposes</em> the change in magnetic flux that produced it, conserving energy.</li>
                        </ul>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-purple-300 flex items-center justify-between">
                        <span>Faraday's Law of Induction:</span>
                        <span>$\mathcal{E} = -N \frac{\Delta \Phi_B}{\Delta t}$</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================= -->
        <!-- TAB 3: KNOWLEDGE QUIZ (10-QUESTION INTERACTIVE TEST)      -->
        <!-- ========================================================= -->
        <section id="section-quiz" class="hidden max-w-3xl mx-auto">
            <!-- Quiz Active Container -->
            <div id="quiz-active-box" class="bg-slate-900/95 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl space-y-6">
                <!-- Header & Progress -->
                <div class="space-y-3">
                    <div class="flex items-center justify-between text-sm">
                        <span id="quiz-progress-label" class="font-mono text-cyan-400 font-semibold">Question 1 of 10</span>
                        <span id="quiz-score-label" class="font-mono text-amber-400 font-semibold">Score: 0</span>
                    </div>
                    <div class="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                        <div id="quiz-progress-bar" class="h-full bg-gradient-to-r from-cyan-500 to-purple-500 transition-all duration-300" style="width: 10%"></div>
                    </div>
                </div>

                <!-- Question Prompt -->
                <div class="space-y-2 pt-2">
                    <span id="quiz-category-badge" class="inline-block px-2.5 py-0.5 rounded-md text-xs font-mono bg-slate-800 text-slate-300">Magnetic Fields</span>
                    <h3 id="quiz-question-text" class="text-xl sm:text-2xl font-bold text-slate-100 leading-snug">
                        Loading question...
                    </h3>
                </div>

                <!-- Options Container -->
                <div id="quiz-options-container" class="space-y-3">
                    <!-- Injected via JS -->
                </div>

                <!-- Explanation Box (Hidden until answered) -->
                <div id="quiz-explanation-box" class="hidden p-4 rounded-xl bg-slate-950/90 border border-slate-700 space-y-1.5">
                    <div id="quiz-feedback-title" class="font-bold text-sm flex items-center gap-2"></div>
                    <p id="quiz-explanation-text" class="text-sm text-slate-300 leading-relaxed"></p>
                </div>

                <!-- Next Button -->
                <div class="flex justify-end pt-2">
                    <button id="quiz-next-btn" onclick="nextQuizQuestion()" class="hidden px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-sm shadow-lg transition flex items-center gap-2">
                        <span>Next Question</span> <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            </div>

            <!-- Quiz Results Screen -->
            <div id="quiz-results-box" class="hidden bg-slate-900/95 border border-slate-800 rounded-2xl p-8 text-center shadow-2xl space-y-6">
                <div class="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-amber-400 to-purple-600 flex items-center justify-center shadow-lg glow-amber">
                    <i id="quiz-rank-icon" class="fa-solid fa-award text-4xl text-white"></i>
                </div>

                <div class="space-y-2">
                    <div class="text-xs font-mono uppercase tracking-widest text-cyan-400">Assessment Complete</div>
                    <h2 id="quiz-rank-title" class="text-3xl font-extrabold text-slate-100">Electromagnetism Master</h2>
                    <p id="quiz-rank-desc" class="text-slate-400 text-sm max-w-md mx-auto">Outstanding command of magnetic dipoles, solenoids, and Faraday's Law!</p>
                </div>

                <div class="inline-flex items-center gap-6 bg-slate-950 px-8 py-4 rounded-2xl border border-slate-800">
                    <div>
                        <div class="text-xs text-slate-400 uppercase font-mono">Final Score</div>
                        <div id="quiz-final-score" class="text-3xl font-extrabold text-cyan-400 font-mono">9 / 10</div>
                    </div>
                    <div class="h-10 w-px bg-slate-800"></div>
                    <div>
                        <div class="text-xs text-slate-400 uppercase font-mono">Accuracy</div>
                        <div id="quiz-final-percent" class="text-3xl font-extrabold text-amber-400 font-mono">90%</div>
                    </div>
                </div>

                <div class="flex flex-wrap justify-center gap-4 pt-2">
                    <button onclick="restartQuiz()" class="px-6 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm transition flex items-center gap-2">
                        <i class="fa-solid fa-rotate-right"></i> Retake Quiz
                    </button>
                    <button onclick="switchMainTab('lab')" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">
                        <i class="fa-solid fa-flask"></i> Return to Lab
                    </button>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800/80 bg-slate-950/60 py-4 text-center text-xs text-slate-500">
        ElectroMag Lab • Interactive Physics Simulation & Assessment Environment
    </footer>

    <!-- ========================================================= -->
    <!-- JAVASCRIPT: PHYSICS ENGINES, SIMULATORS & QUIZ LOGIC       -->
    <!-- ========================================================= -->
    <script>
        // =========================================================
        // 1. NAVIGATION & TAB MANAGEMENT
        // =========================================================
        let activeMainTab = 'lab';
        let activeSim = 'bar';

        function switchMainTab(tab) {
            activeMainTab = tab;
            ['lab', 'concepts', 'quiz'].forEach(t => {
                const sec = document.getElementById(`section-${t}`);
                const btn = document.getElementById(`tab-btn-${t}`);
                if (t === tab) {
                    sec.classList.remove('hidden');
                    btn.className = "main-tab flex-1 md:flex-none flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm";
                } else {
                    sec.classList.add('hidden');
                    btn.className = "main-tab flex-1 md:flex-none flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent";
                }
            });

            if (tab === 'lab') {
                resizeAllCanvases();
            }
        }

        function switchSim(sim) {
            activeSim = sim;
            const styles = {
                bar: "sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-800/90 border-cyan-500/60 glow-cyan",
                solenoid: "sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-800/90 border-amber-500/60 glow-amber",
                faraday: "sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-800/90 border-purple-500/60 glow-purple"
            };
            const inactiveStyle = "sim-selector flex items-center gap-3 p-3.5 rounded-2xl border transition-all text-left bg-slate-900/70 border-slate-800 hover:border-slate-700";

            ['bar', 'solenoid', 'faraday'].forEach(s => {
                const container = document.getElementById(`sim-container-${s}`);
                const btn = document.getElementById(`sim-btn-${s}`);
                if (s === sim) {
                    container.classList.remove('hidden');
                    container.classList.add('grid');
                    btn.className = styles[s];
                } else {
                    container.classList.add('hidden');
                    container.classList.remove('grid');
                    btn.className = inactiveStyle;
                }
            });

            resizeAllCanvases();
        }

        // =========================================================
        // 2. CANVAS SIZING & HELPER UTILITIES
        // =========================================================
        const canvasBar = document.getElementById('canvas-bar');
        const ctxBar = canvasBar.getContext('2d');

        const canvasSol = document.getElementById('canvas-solenoid');
        const ctxSol = canvasSol.getContext('2d');

        const canvasFar = document.getElementById('canvas-faraday');
        const ctxFar = canvasFar.getContext('2d');

        function resizeCanvas(canvas) {
            if (!canvas || !canvas.parentElement) return;
            const rect = canvas.parentElement.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return;
            const dpr = window.devicePixelRatio || 1;
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            const ctx = canvas.getContext('2d');
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            canvas.logicalWidth = rect.width;
            canvas.logicalHeight = rect.height;
        }

        function resizeAllCanvases() {
            resizeCanvas(canvasBar);
            resizeCanvas(canvasSol);
            resizeCanvas(canvasFar);
        }

        window.addEventListener('resize', resizeAllCanvases);

        function getPointerPos(e, canvas) {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }

        // =========================================================
        // 3. SIMULATOR A: BAR MAGNET & FIELD LINES ENGINE
        // =========================================================
        const barState = {
            magnet: { x: 0, y: 0, width: 150, height: 46, polarity: 1, initialized: false },
            probe: { x: 0, y: 0, radius: 22, initialized: false },
            dragging: null, // 'magnet' or 'probe'
            dragOffset: { x: 0, y: 0 },
            strength: 1.0,
            showLines: true,
            showGrid: true
        };

        // Dipole magnetic field calculation B(x, y)
        function calculateDipoleField(px, py) {
            const m = barState.magnet;
            const halfLen = m.width * 0.42;
            const nx = m.x + halfLen * m.polarity;
            const ny = m.y;
            const sx = m.x - halfLen * m.polarity;
            const sy = m.y;

            // Vector from North pole (+q_m)
            const dxN = px - nx;
            const dyN = py - ny;
            const rN2 = Math.max(dxN * dxN + dyN * dyN, 450);
            const rN = Math.sqrt(rN2);

            // Vector from South pole (-q_m)
            const dxS = px - sx;
            const dyS = py - sy;
            const rS2 = Math.max(dxS * dxS + dyS * dyS, 450);
            const rS = Math.sqrt(rS2);

            const scale = 180000 * barState.strength;
            const bx = scale * (dxN / (rN2 * rN) - dxS / (rS2 * rS));
            const by = scale * (dyN / (rN2 * rN) - dyS / (rS2 * rS));

            return { bx, by, mag: Math.hypot(bx, by) };
        }

        function flipBarMagnet() {
            barState.magnet.polarity *= -1;
        }

        function resetBarMagnet() {
            const w = canvasBar.logicalWidth || 600;
            const h = canvasBar.logicalHeight || 420;
            barState.magnet.x = w * 0.45;
            barState.magnet.y = h * 0.5;
            barState.magnet.polarity = 1;
            barState.probe.x = w * 0.45;
            barState.probe.y = h * 0.24;
            barState.strength = 1.0;
            document.getElementById('bar-strength').value = 100;
            document.getElementById('bar-strength-val').textContent = '100%';
        }

        // Event Listeners for Simulator A
        document.getElementById('bar-toggle-lines').addEventListener('change', e => barState.showLines = e.target.checked);
        document.getElementById('bar-toggle-grid').addEventListener('change', e => barState.showGrid = e.target.checked);
        document.getElementById('bar-strength').addEventListener('input', e => {
            barState.strength = parseInt(e.target.value) / 100;
            document.getElementById('bar-strength-val').textContent = `${e.target.value}%`;
        });

        function handleBarDown(e) {
            const pos = getPointerPos(e, canvasBar);
            const p = barState.probe;
            const m = barState.magnet;

            // Check probe first
            if (Math.hypot(pos.x - p.x, pos.y - p.y) <= p.radius + 12) {
                barState.dragging = 'probe';
                barState.dragOffset = { x: pos.x - p.x, y: pos.y - p.y };
                return;
            }
            // Check magnet bounding box
            if (Math.abs(pos.x - m.x) <= m.width / 2 + 10 && Math.abs(pos.y - m.y) <= m.height / 2 + 10) {
                barState.dragging = 'magnet';
                barState.dragOffset = { x: pos.x - m.x, y: pos.y - m.y };
            }
        }

        function handleBarMove(e) {
            if (!barState.dragging) return;
            e.preventDefault();
            const pos = getPointerPos(e, canvasBar);
            const w = canvasBar.logicalWidth;
            const h = canvasBar.logicalHeight;

            if (barState.dragging === 'probe') {
                barState.probe.x = Math.max(25, Math.min(w - 25, pos.x - barState.dragOffset.x));
                barState.probe.y = Math.max(25, Math.min(h - 25, pos.y - barState.dragOffset.y));
            } else if (barState.dragging === 'magnet') {
                barState.magnet.x = Math.max(85, Math.min(w - 85, pos.x - barState.dragOffset.x));
                barState.magnet.y = Math.max(35, Math.min(h - 35, pos.y - barState.dragOffset.y));
            }
        }

        function handleBarUp() {
            barState.dragging = null;
        }

        canvasBar.addEventListener('mousedown', handleBarDown);
        window.addEventListener('mousemove', handleBarMove);
        window.addEventListener('mouseup', handleBarUp);
        canvasBar.addEventListener('touchstart', handleBarDown, { passive: false });
        window.addEventListener('touchmove', handleBarMove, { passive: false });
        window.addEventListener('touchend', handleBarUp);

        function renderBarSimulator() {
            const w = canvasBar.logicalWidth;
            const h = canvasBar.logicalHeight;
            if (!w || !h) return;

            if (!barState.magnet.initialized) {
                resetBarMagnet();
                barState.magnet.initialized = true;
            }

            ctxBar.clearRect(0, 0, w, h);

            // 1. Compass Needle Grid
            if (barState.showGrid) {
                const spacing = 44;
                for (let gx = spacing / 2; gx < w; gx += spacing) {
                    for (let gy = spacing / 2; gy < h; gy += spacing) {
                        const field = calculateDipoleField(gx, gy);
                        const angle = Math.atan2(field.by, field.bx);
                        const alpha = Math.min(0.85, Math.max(0.18, field.mag / 35));

                        ctxBar.save();
                        ctxBar.translate(gx, gy);
                        ctxBar.rotate(angle);

                        // Mini compass needle
                        ctxBar.beginPath();
                        ctxBar.moveTo(9, 0);
                        ctxBar.lineTo(-2, -2.5);
                        ctxBar.lineTo(-2, 2.5);
                        ctxBar.closePath();
                        ctxBar.fillStyle = `rgba(239, 68, 68, ${alpha})`;
                        ctxBar.fill();

                        ctxBar.beginPath();
                        ctxBar.moveTo(-9, 0);
                        ctxBar.lineTo(-2, -2.5);
                        ctxBar.lineTo(-2, 2.5);
                        ctxBar.closePath();
                        ctxBar.fillStyle = `rgba(148, 163, 184, ${alpha * 0.7})`;
                        ctxBar.fill();

                        ctxBar.restore();
                    }
                }
            }

            // 2. Continuous Field Lines (Streamlines traced from North Pole)
            if (barState.showLines) {
                const m = barState.magnet;
                const halfLen = m.width * 0.42;
                const nx = m.x + halfLen * m.polarity;
                const ny = m.y;
                const sx = m.x - halfLen * m.polarity;
                const sy = m.y;

                const numLines = 14;
                ctxBar.lineWidth = 1.6;

                for (let i = 0; i < numLines; i++) {
                    const startAngle = (i / numLines) * Math.PI * 2;
                    let cx = nx + Math.cos(startAngle) * 14;
                    let cy = ny + Math.sin(startAngle) * 14;

                    ctxBar.beginPath();
                    ctxBar.moveTo(cx, cy);

                    const points = [];
                    for (let step = 0; step < 260; step++) {
                        const field = calculateDipoleField(cx, cy);
                        if (field.mag < 0.01) break;
                        const stepSize = 5;
                        cx += (field.bx / field.mag) * stepSize;
                        cy += (field.by / field.mag) * stepSize;
                        ctxBar.lineTo(cx, cy);
                        if (step % 35 === 15) {
                            points.push({ x: cx, y: cy, angle: Math.atan2(field.by, field.bx) });
                        }
                        // Stop if reached South pole or far outside canvas
                        if (Math.hypot(cx - sx, cy - sy) < 15) break;
                        if (cx < -100 || cx > w + 100 || cy < -100 || cy > h + 100) break;
                    }

                    ctxBar.strokeStyle = `rgba(6, 182, 212, ${0.28 * Math.min(1.3, barState.strength)})`;
                    ctxBar.stroke();

                    // Directional arrows along field lines
                    points.forEach(pt => {
                        if (pt.x > 0 && pt.x < w && pt.y > 0 && pt.y < h) {
                            ctxBar.save();
                            ctxBar.translate(pt.x, pt.y);
                            ctxBar.rotate(pt.angle);
                            ctxBar.beginPath();
                            ctxBar.moveTo(4, 0);
                            ctxBar.lineTo(-3, -3);
                            ctxBar.lineTo(-3, 3);
                            ctxBar.closePath();
                            ctxBar.fillStyle = 'rgba(34, 211, 238, 0.75)';
                            ctxBar.fill();
                            ctxBar.restore();
                        }
                    });
                }
            }

            // 3. Draw Bar Magnet
            const m = barState.magnet;
            ctxBar.save();
            ctxBar.translate(m.x, m.y);

            // Shadow
            ctxBar.shadowColor = 'rgba(0, 0, 0, 0.6)';
            ctxBar.shadowBlur = 15;
            ctxBar.shadowOffsetY = 6;

            const leftIsNorth = m.polarity === -1;
            // Left Half
            ctxBar.fillStyle = leftIsNorth ? '#ef4444' : '#3b82f6';
            ctxBar.beginPath();
            ctxBar.roundRect(-m.width / 2, -m.height / 2, m.width / 2, m.height, [8, 0, 0, 8]);
            ctxBar.fill();

            // Right Half
            ctxBar.fillStyle = leftIsNorth ? '#3b82f6' : '#ef4444';
            ctxBar.beginPath();
            ctxBar.roundRect(0, -m.height / 2, m.width / 2, m.height, [0, 8, 8, 0]);
            ctxBar.fill();

            ctxBar.shadowColor = 'transparent';
            ctxBar.strokeStyle = 'rgba(255,255,255,0.25)';
            ctxBar.lineWidth = 1.5;
            ctxBar.strokeRect(-m.width / 2, -m.height / 2, m.width, m.height);

            // Labels N & S
            ctxBar.fillStyle = '#ffffff';
            ctxBar.font = 'bold 18px Inter, sans-serif';
            ctxBar.textAlign = 'center';
            ctxBar.textBaseline = 'middle';
            ctxBar.fillText(leftIsNorth ? 'N' : 'S', -m.width / 4, 1);
            ctxBar.fillText(leftIsNorth ? 'S' : 'N', m.width / 4, 1);
            ctxBar.restore();

            // 4. Draw Draggable Compass Probe
            const p = barState.probe;
            const probeField = calculateDipoleField(p.x, p.y);
            const probeAngle = Math.atan2(probeField.by, probeField.bx);

            ctxBar.save();
            ctxBar.translate(p.x, p.y);

            // Outer glowing ring
            ctxBar.beginPath();
            ctxBar.arc(0, 0, p.radius + 4, 0, Math.PI * 2);
            ctxBar.strokeStyle = 'rgba(6, 182, 212, 0.45)';
            ctxBar.lineWidth = 2;
            ctxBar.stroke();

            // Compass housing
            ctxBar.beginPath();
            ctxBar.arc(0, 0, p.radius, 0, Math.PI * 2);
            ctxBar.fillStyle = '#0f172a';
            ctxBar.fill();
            ctxBar.strokeStyle = '#94a3b8';
            ctxBar.lineWidth = 2;
            ctxBar.stroke();

            // Rotating Needle
            ctxBar.rotate(probeAngle);
            // North tip (Red)
            ctxBar.beginPath();
            ctxBar.moveTo(p.radius - 4, 0);
            ctxBar.lineTo(0, -5);
            ctxBar.lineTo(0, 5);
            ctxBar.closePath();
            ctxBar.fillStyle = '#ef4444';
            ctxBar.fill();

            // South tip (White/Cyan)
            ctxBar.beginPath();
            ctxBar.moveTo(-(p.radius - 4), 0);
            ctxBar.lineTo(0, -5);
            ctxBar.lineTo(0, 5);
            ctxBar.closePath();
            ctxBar.fillStyle = '#e2e8f0';
            ctxBar.fill();

            // Center pivot
            ctxBar.beginPath();
            ctxBar.arc(0, 0, 3, 0, Math.PI * 2);
            ctxBar.fillStyle = '#f59e0b';
            ctxBar.fill();
            ctxBar.restore();

            // Update Telemetry Readouts
            const deg = ((probeAngle * 180 / Math.PI) + 360) % 360;
            document.getElementById('bar-readout-b').textContent = `${(probeField.mag * 0.85).toFixed(1)} mT`;
            document.getElementById('bar-readout-angle').textContent = `${deg.toFixed(1)}°`;
        }

        // =========================================================
        // 4. SIMULATOR B: ELECTROMAGNET & SOLENOID BUILDER
        // =========================================================
        const solState = {
            current: 4.0,
            turns: 40,
            muR: 200,
            polarity: 1, // 1 or -1
            electronPhase: 0,
            paperclips: []
        };

        // Initialize 24 paperclips at the bottom of the bench
        for (let i = 0; i < 24; i++) {
            solState.paperclips.push({
                id: i,
                offsetX: (i - 11.5) * 16 + (Math.random() * 6 - 3),
                angle: (Math.random() - 0.5) * 0.8,
                liftedProgress: 0 // 0 = on table, 1 = stuck to electromagnet
            });
        }

        document.getElementById('sol-slider-current').addEventListener('input', e => {
            solState.current = parseFloat(e.target.value);
            document.getElementById('sol-val-current').textContent = `${solState.current.toFixed(1)} A`;
        });

        document.getElementById('sol-slider-turns').addEventListener('input', e => {
            solState.turns = parseInt(e.target.value);
            document.getElementById('sol-val-turns').textContent = `${solState.turns} Turns`;
        });

        document.getElementById('sol-select-core').addEventListener('change', e => {
            solState.muR = parseInt(e.target.value);
        });

        function reverseSolenoidCurrent() {
            solState.polarity *= -1;
        }

        function renderSolenoidSimulator() {
            const w = canvasSol.logicalWidth;
            const h = canvasSol.logicalHeight;
            if (!w || !h) return;

            ctxSol.clearRect(0, 0, w, h);

            // Physics calculation: B = mu0 * muR * (N / L) * I
            // Assume solenoid length L = 0.20 m
            const mu0 = 4 * Math.PI * 1e-7;
            const L = 0.20;
            const B_tesla = mu0 * solState.muR * (solState.turns / L) * solState.current;
            const B_mT = B_tesla * 1000;

            // Maximum possible B here is at I=10, N=100, muR=500 -> ~3141 mT
            // Scale lifting capacity realistically (0 to 24 paperclips)
            const liftedCount = solState.current === 0 ? 0 : Math.min(24, Math.floor((B_mT / 650) * 24));

            document.getElementById('sol-readout-b').textContent = `${B_mT.toFixed(1)} mT`;
            document.getElementById('sol-readout-clips').textContent = `${liftedCount} / 24`;

            const cx = w * 0.5;
            const cy = h * 0.36;
            const coreW = Math.min(340, w * 0.58);
            const coreH = 54;

            // Advance electron animation phase
            solState.electronPhase += solState.current * 0.035 * solState.polarity;

            // 1. Draw Magnetic Field Lines around Solenoid if B > 0
            if (B_mT > 0.5) {
                const intensity = Math.min(1, B_mT / 400);
                const loops = 5;
                for (let i = 1; i <= loops; i++) {
                    const spreadY = i * 26;
                    const spreadX = coreW * 0.52 + i * 22;
                    ctxSol.beginPath();
                    ctxSol.ellipse(cx, cy, spreadX, spreadY, 0, 0, Math.PI * 2);
                    ctxSol.strokeStyle = `rgba(6, 182, 212, ${0.12 + intensity * 0.35})`;
                    ctxSol.lineWidth = 1.5;
                    ctxSol.stroke();
                }

                // Pole Indicators (N and S)
                const northRight = solState.polarity === 1;
                ctxSol.font = 'bold 14px Inter, sans-serif';
                ctxSol.textAlign = 'center';

                // Left Pole Badge
                ctxSol.fillStyle = northRight ? '#3b82f6' : '#ef4444';
                ctxSol.beginPath();
                ctxSol.roundRect(cx - coreW / 2 - 42, cy - 14, 32, 28, 6);
                ctxSol.fill();
                ctxSol.fillStyle = '#fff';
                ctxSol.fillText(northRight ? 'S' : 'N', cx - coreW / 2 - 26, cy + 5);

                // Right Pole Badge
                ctxSol.fillStyle = northRight ? '#ef4444' : '#3b82f6';
                ctxSol.beginPath();
                ctxSol.roundRect(cx + coreW / 2 + 10, cy - 14, 32, 28, 6);
                ctxSol.fill();
                ctxSol.fillStyle = '#fff';
                ctxSol.fillText(northRight ? 'N' : 'S', cx + coreW / 2 + 26, cy + 5);
            }

            // 2. Draw Back Half of Copper Windings
            const visualTurns = Math.max(8, Math.floor(solState.turns / 3));
            const turnSpacing = (coreW - 30) / visualTurns;
            const startX = cx - (coreW - 30) / 2;

            ctxSol.lineWidth = 4.5;
            ctxSol.strokeStyle = '#9a3412'; // darker copper behind core
            for (let i = 0; i < visualTurns; i++) {
                const tx = startX + i * turnSpacing;
                ctxSol.beginPath();
                ctxSol.moveTo(tx + turnSpacing * 0.5, cy - coreH / 2 - 8);
                ctxSol.lineTo(tx + turnSpacing, cy + coreH / 2 + 8);
                ctxSol.stroke();
            }

            // 3. Draw Core Material
            if (solState.muR === 1) {
                // Air core (dashed outline)
                ctxSol.save();
                ctxSol.setLineDash([6, 6]);
                ctxSol.strokeStyle = 'rgba(148, 163, 184, 0.4)';
                ctxSol.lineWidth = 2;
                ctxSol.strokeRect(cx - coreW / 2, cy - coreH / 2, coreW, coreH);
                ctxSol.fillStyle = 'rgba(148, 163, 184, 0.35)';
                ctxSol.font = '12px JetBrains Mono, monospace';
                ctxSol.textAlign = 'center';
                ctxSol.fillText('AIR CORE (μᵣ = 1)', cx, cy + 4);
                ctxSol.restore();
            } else {
                // Solid Iron or Ferrite Cylinder
                const grad = ctxSol.createLinearGradient(0, cy - coreH / 2, 0, cy + coreH / 2);
                if (solState.muR === 200) {
                    grad.addColorStop(0, '#475569');
                    grad.addColorStop(0.5, '#94a3b8');
                    grad.addColorStop(1, '#334155');
                } else {
                    grad.addColorStop(0, '#1e1b4b');
                    grad.addColorStop(0.5, '#4338ca');
                    grad.addColorStop(1, '#1e1b4b');
                }
                ctxSol.fillStyle = grad;
                ctxSol.beginPath();
                ctxSol.roundRect(cx - coreW / 2, cy - coreH / 2, coreW, coreH, 8);
                ctxSol.fill();
                ctxSol.strokeStyle = 'rgba(255,255,255,0.2)';
                ctxSol.lineWidth = 1.5;
                ctxSol.stroke();
            }

            // 4. Draw Front Half of Copper Windings + Animated Current Dots
            for (let i = 0; i < visualTurns; i++) {
                const tx = startX + i * turnSpacing;
                ctxSol.beginPath();
                ctxSol.moveTo(tx, cy - coreH / 2 - 8);
                ctxSol.lineTo(tx + turnSpacing * 0.5, cy + coreH / 2 + 8);
                ctxSol.strokeStyle = '#f59e0b';
                ctxSol.lineWidth = 5;
                ctxSol.lineCap = 'round';
                ctxSol.stroke();

                // Moving current charge indicator
                if (solState.current > 0) {
                    const t = ((solState.electronPhase + i * 0.4) % 1 + 1) % 1;
                    const dotX = tx + (turnSpacing * 0.5) * t;
                    const dotY = (cy - coreH / 2 - 8) + (coreH + 16) * t;
                    ctxSol.beginPath();
                    ctxSol.arc(dotX, dotY, 3, 0, Math.PI * 2);
                    ctxSol.fillStyle = '#fef08a';
                    ctxSol.fill();
                }
            }

            // 5. Draw Battery & Leads below Solenoid
            const batY = cy + 88;
            ctxSol.strokeStyle = '#d97706';
            ctxSol.lineWidth = 3;
            ctxSol.beginPath();
            ctxSol.moveTo(startX, cy - coreH / 2 - 8);
            ctxSol.lineTo(startX - 20, cy - coreH / 2 - 8);
            ctxSol.lineTo(startX - 20, batY);
            ctxSol.lineTo(cx - 35, batY);
            ctxSol.stroke();

            ctxSol.beginPath();
            ctxSol.moveTo(startX + (visualTurns - 1) * turnSpacing + turnSpacing * 0.5, cy + coreH / 2 + 8);
            ctxSol.lineTo(startX + (visualTurns - 1) * turnSpacing + 20, cy + coreH / 2 + 8);
            ctxSol.lineTo(startX + (visualTurns - 1) * turnSpacing + 20, batY);
            ctxSol.lineTo(cx + 35, batY);
            ctxSol.stroke();

            // Battery Graphic
            ctxSol.fillStyle = '#1e293b';
            ctxSol.strokeStyle = '#64748b';
            ctxSol.lineWidth = 2;
            ctxSol.beginPath();
            ctxSol.roundRect(cx - 35, batY - 14, 70, 28, 6);
            ctxSol.fill();
            ctxSol.stroke();

            ctxSol.font = 'bold 13px JetBrains Mono, monospace';
            ctxSol.textAlign = 'center';
            ctxSol.fillStyle = solState.polarity === 1 ? '#ef4444' : '#3b82f6';
            ctxSol.fillText(solState.polarity === 1 ? '+' : '−', cx - 18, batY + 5);
            ctxSol.fillStyle = solState.polarity === 1 ? '#3b82f6' : '#ef4444';
            ctxSol.fillText(solState.polarity === 1 ? '−' : '+', cx + 18, batY + 5);
            ctxSol.fillStyle = '#94a3b8';
            ctxSol.font = '10px Inter, sans-serif';
            ctxSol.fillText('DC', cx, batY + 4);

            // 6. Draw Bench & Steel Paperclips (Attracted upward based on liftedCount)
            const benchY = h - 32;
            ctxSol.fillStyle = '#1e293b';
            ctxSol.fillRect(20, benchY, w - 40, 10);

            solState.paperclips.forEach((clip, idx) => {
                const isLifted = idx < liftedCount;
                const targetProgress = isLifted ? 1 : 0;
                clip.liftedProgress += (targetProgress - clip.liftedProgress) * 0.12;

                const restX = cx + clip.offsetX;
                const restY = benchY - 6;

                // Cluster around the core bottom when lifted
                const liftedX = cx + (clip.offsetX * 0.75);
                const liftedY = cy + coreH / 2 + 12 + (idx % 3) * 6;

                const drawX = restX + (liftedX - restX) * clip.liftedProgress;
                const drawY = restY + (liftedY - restY) * clip.liftedProgress;
                const rot = clip.angle * (1 - clip.liftedProgress) + (Math.PI / 2) * clip.liftedProgress;

                ctxSol.save();
                ctxSol.translate(drawX, drawY);
                ctxSol.rotate(rot);
                ctxSol.strokeStyle = isLifted ? '#38bdf8' : '#94a3b8';
                ctxSol.lineWidth = 2;
                ctxSol.beginPath();
                ctxSol.roundRect(-10, -4, 20, 8, 4);
                ctxSol.stroke();
                ctxSol.restore();
            });
        }

        // =========================================================
        // 5. SIMULATOR C: FARADAY'S INDUCTION ENGINE
        // =========================================================
        const farState = {
            magnetX: 0,
            lastMagnetX: 0,
            velocity: 0,
            emf: 0,
            flux: 0,
            polarity: 1,
            loops: 3,
            dragging: false,
            dragOffsetX: 0,
            autoOscillate: false,
            oscPhase: 0,
            initialized: false
        };

        document.getElementById('far-slider-loops').addEventListener('input', e => {
            farState.loops = parseInt(e.target.value);
            document.getElementById('far-val-loops').textContent = `${farState.loops} Loop${farState.loops > 1 ? 's' : ''}`;
        });

        function toggleFaradayAuto() {
            farState.autoOscillate = !farState.autoOscillate;
            const btn = document.getElementById('far-btn-auto');
            const label = document.getElementById('far-auto-label');
            if (farState.autoOscillate) {
                label.textContent = 'Stop AC Auto-Oscillator';
                btn.classList.add('bg-purple-600/40', 'border-purple-400');
            } else {
                label.textContent = 'Start AC Auto-Oscillator';
                btn.classList.remove('bg-purple-600/40', 'border-purple-400');
            }
        }

        function flipFaradayMagnet() {
            farState.polarity *= -1;
        }

        function handleFarDown(e) {
            const pos = getPointerPos(e, canvasFar);
            const h = canvasFar.logicalHeight;
            const magnetY = h * 0.64;
            if (Math.abs(pos.x - farState.magnetX) <= 75 && Math.abs(pos.y - magnetY) <= 32) {
                farState.dragging = true;
                farState.autoOscillate = false;
                document.getElementById('far-auto-label').textContent = 'Start AC Auto-Oscillator';
                farState.dragOffsetX = pos.x - farState.magnetX;
            }
        }

        function handleFarMove(e) {
            if (!farState.dragging) return;
            e.preventDefault();
            const pos = getPointerPos(e, canvasFar);
            const w = canvasFar.logicalWidth;
            farState.magnetX = Math.max(85, Math.min(w - 85, pos.x - farState.dragOffsetX));
        }

        function handleFarUp() {
            farState.dragging = false;
        }

        canvasFar.addEventListener('mousedown', handleFarDown);
        window.addEventListener('mousemove', handleFarMove);
        window.addEventListener('mouseup', handleFarUp);
        canvasFar.addEventListener('touchstart', handleFarDown, { passive: false });
        window.addEventListener('touchmove', handleFarMove, { passive: false });
        window.addEventListener('touchend', handleFarUp);

        function renderFaradaySimulator() {
            const w = canvasFar.logicalWidth;
            const h = canvasFar.logicalHeight;
            if (!w || !h) return;

            const coilX = w * 0.56;
            const magnetY = h * 0.64;

            if (!farState.initialized) {
                farState.magnetX = w * 0.24;
                farState.lastMagnetX = farState.magnetX;
                farState.initialized = true;
            }

            if (farState.autoOscillate) {
                farState.oscPhase += 0.055;
                farState.magnetX = coilX + Math.sin(farState.oscPhase) * (w * 0.28);
            }

            // Calculate flux Phi(x) modeled as derivative-friendly Gaussian bell centered at coilX
            const dx = (farState.magnetX - coilX) / 95;
            const currentFlux = farState.polarity * 45 * Math.exp(-dx * dx);

            // Faraday's Law: EMF = -N * dPhi / dt
            const dFlux = currentFlux - farState.flux;
            const rawEmf = -farState.loops * dFlux * 1.4;
            // Smooth needle inertia slightly
            farState.emf += (rawEmf - farState.emf) * 0.35;
            farState.flux = currentFlux;
            farState.lastMagnetX = farState.magnetX;

            // Telemetry updates
            document.getElementById('far-readout-emf').textContent = `${farState.emf.toFixed(2)} V`;
            document.getElementById('far-readout-flux').textContent = `${farState.flux.toFixed(1)} mWb`;

            const statusEl = document.getElementById('far-status-text');
            if (Math.abs(farState.emf) > 0.25) {
                const dir = farState.emf > 0 ? 'Positive (+)' : 'Negative (−)';
                statusEl.textContent = `Flux changing! Induced ${dir} EMF lighting the bulb (Lenz's Law opposes motion).`;
            } else {
                statusEl.textContent = `Stationary magnet — zero change in flux (ΔΦ_B = 0), so no current is induced.`;
            }

            ctxFar.clearRect(0, 0, w, h);

            // 1. Draw Top Circuit: Lightbulb & Galvanometer
            const bulbX = w * 0.34;
            const meterX = w * 0.68;
            const topY = h * 0.22;

            // Wires connecting Coil to Lightbulb & Galvanometer
            ctxFar.strokeStyle = '#d97706';
            ctxFar.lineWidth = 3.5;
            ctxFar.beginPath();
            ctxFar.moveTo(coilX - 25, magnetY - 58);
            ctxFar.lineTo(coilX - 25, topY + 35);
            ctxFar.lineTo(bulbX, topY + 35);
            ctxFar.lineTo(bulbX, topY + 12);
            ctxFar.stroke();

            ctxFar.beginPath();
            ctxFar.moveTo(bulbX, topY - 12);
            ctxFar.lineTo(bulbX, topY - 35);
            ctxFar.lineTo(meterX, topY - 35);
            ctxFar.lineTo(meterX, topY - 22);
            ctxFar.stroke();

            ctxFar.beginPath();
            ctxFar.moveTo(meterX, topY + 22);
            ctxFar.lineTo(meterX, topY + 35);
            ctxFar.lineTo(coilX + 25, topY + 35);
            ctxFar.lineTo(coilX + 25, magnetY - 58);
            ctxFar.stroke();

            // Lightbulb Glow based on |EMF|
            const brightness = Math.min(1, Math.abs(farState.emf) / 5.5);
            if (brightness > 0.03) {
                const glowGrad = ctxFar.createRadialGradient(bulbX, topY, 4, bulbX, topY, 65 * brightness + 15);
                glowGrad.addColorStop(0, `rgba(253, 224, 71, ${brightness * 0.95})`);
                glowGrad.addColorStop(0.5, `rgba(245, 158, 11, ${brightness * 0.45})`);
                glowGrad.addColorStop(1, 'rgba(245, 158, 11, 0)');
                ctxFar.fillStyle = glowGrad;
                ctxFar.beginPath();
                ctxFar.arc(bulbX, topY, 80, 0, Math.PI * 2);
                ctxFar.fill();
            }

            // Lightbulb Glass
            ctxFar.fillStyle = brightness > 0.1 ? `rgba(254, 240, 138, ${0.3 + brightness * 0.7})` : 'rgba(30, 41, 59, 0.8)';
            ctxFar.strokeStyle = '#94a3b8';
            ctxFar.lineWidth = 2;
            ctxFar.beginPath();
            ctxFar.arc(bulbX, topY, 20, 0, Math.PI * 2);
            ctxFar.fill();
            ctxFar.stroke();

            // Filament
            ctxFar.strokeStyle = brightness > 0.1 ? '#ffffff' : '#64748b';
            ctxFar.lineWidth = 2;
            ctxFar.beginPath();
            ctxFar.moveTo(bulbX - 6, topY + 12);
            ctxFar.lineTo(bulbX - 4, topY - 4);
            ctxFar.lineTo(bulbX, topY + 2);
            ctxFar.lineTo(bulbX + 4, topY - 4);
            ctxFar.lineTo(bulbX + 6, topY + 12);
            ctxFar.stroke();

            // Analog Galvanometer
            ctxFar.fillStyle = '#0f172a';
            ctxFar.strokeStyle = '#8b5cf6';
            ctxFar.lineWidth = 2.5;
            ctxFar.beginPath();
            ctxFar.arc(meterX, topY, 32, 0, Math.PI * 2);
            ctxFar.fill();
            ctxFar.stroke();

            // Scale ticks
            ctxFar.strokeStyle = '#475569';
            ctxFar.lineWidth = 1.5;
            for (let a = -0.8; a <= 0.81; a += 0.4) {
                ctxFar.beginPath();
                ctxFar.moveTo(meterX + Math.sin(a) * 20, topY + 10 - Math.cos(a) * 20);
                ctxFar.lineTo(meterX + Math.sin(a) * 26, topY + 10 - Math.cos(a) * 26);
                ctxFar.stroke();
            }

            // Deflecting Needle
            const clampedDeflection = Math.max(-1.1, Math.min(1.1, farState.emf * 0.18));
            ctxFar.save();
            ctxFar.translate(meterX, topY + 12);
            ctxFar.rotate(clampedDeflection);
            ctxFar.strokeStyle = '#f43f5e';
            ctxFar.lineWidth = 2.5;
            ctxFar.beginPath();
            ctxFar.moveTo(0, 0);
            ctxFar.lineTo(0, -28);
            ctxFar.stroke();
            ctxFar.restore();

            ctxFar.fillStyle = '#cbd5e1';
            ctxFar.font = 'bold 10px JetBrains Mono, monospace';
            ctxFar.textAlign = 'center';
            ctxFar.fillText('VOLTS', meterX, topY + 24);

            // 2. Draw Back Half of Copper Coil
            const loopSpacing = 14;
            const coilStart = coilX - ((farState.loops - 1) * loopSpacing) / 2;

            for (let i = 0; i < farState.loops; i++) {
                const lx = coilStart + i * loopSpacing;
                ctxFar.strokeStyle = '#9a3412';
                ctxFar.lineWidth = 6;
                ctxFar.beginPath();
                ctxFar.ellipse(lx, magnetY, 18, 58, 0, -Math.PI / 2, Math.PI / 2);
                ctxFar.stroke();
            }

            // 3. Draw Draggable Bar Magnet (passes right through the center of the coil!)
            const mw = 136;
            const mh = 42;
            ctxFar.save();
            ctxFar.translate(farState.magnetX, magnetY);

            // Subtle magnetic field halo around magnet
            ctxFar.strokeStyle = 'rgba(6, 182, 212, 0.22)';
            ctxFar.lineWidth = 1.5;
            ctxFar.beginPath();
            ctxFar.ellipse(0, 0, mw * 0.85, mh * 1.4, 0, 0, Math.PI * 2);
            ctxFar.stroke();

            const leftNorth = farState.polarity === -1;
            ctxFar.fillStyle = leftNorth ? '#ef4444' : '#3b82f6';
            ctxFar.beginPath();
            ctxFar.roundRect(-mw / 2, -mh / 2, mw / 2, mh, [8, 0, 0, 8]);
            ctxFar.fill();

            ctxFar.fillStyle = leftNorth ? '#3b82f6' : '#ef4444';
            ctxFar.beginPath();
            ctxFar.roundRect(0, -mh / 2, mw / 2, mh, [0, 8, 8, 0]);
            ctxFar.fill();

            ctxFar.strokeStyle = 'rgba(255,255,255,0.3)';
            ctxFar.lineWidth = 1.5;
            ctxFar.strokeRect(-mw / 2, -mh / 2, mw, mh);

            ctxFar.fillStyle = '#ffffff';
            ctxFar.font = 'bold 16px Inter, sans-serif';
            ctxFar.textAlign = 'center';
            ctxFar.textBaseline = 'middle';
            ctxFar.fillText(leftNorth ? 'N' : 'S', -mw / 4, 1);
            ctxFar.fillText(leftNorth ? 'S' : 'N', mw / 4, 1);
            ctxFar.restore();

            // 4. Draw Front Half of Copper Coil (Overlapping the magnet for true 3D pass-through depth!)
            for (let i = 0; i < farState.loops; i++) {
                const lx = coilStart + i * loopSpacing;
                ctxFar.strokeStyle = '#f59e0b';
                ctxFar.lineWidth = 6;
                ctxFar.beginPath();
                ctxFar.ellipse(lx, magnetY, 18, 58, 0, Math.PI / 2, (3 * Math.PI) / 2);
                ctxFar.stroke();
            }
        }

        // =========================================================
        // 6. MAIN ANIMATION LOOP
        // =========================================================
        function animateLoop() {
            if (activeMainTab === 'lab') {
                if (activeSim === 'bar') renderBarSimulator();
                else if (activeSim === 'solenoid') renderSolenoidSimulator();
                else if (activeSim === 'faraday') renderFaradaySimulator();
            }
            requestAnimationFrame(animateLoop);
        }

        // =========================================================
        // 7. KNOWLEDGE QUIZ ENGINE (10 QUESTIONS)
        // =========================================================
        const quizQuestions = [
            {
                category: "Magnetic Fields",
                question: "In which direction do magnetic field lines point outside a bar magnet?",
                options: [
                    "From the South pole to the North pole",
                    "From the North pole to the South pole",
                    "Radially outward from the center",
                    "Perpendicular to the magnet's axis everywhere"
                ],
                correct: 1,
                explanation: "By convention, magnetic field lines emerge from the North (N) pole and curve around to enter the South (S) pole outside the magnet, forming closed loops."
            },
            {
                category: "Dipoles",
                question: "If you cut a permanent bar magnet directly in half, what happens?",
                options: [
                    "You get an isolated North monopole and an isolated South monopole",
                    "Both halves lose their magnetism completely",
                    "Each half becomes a complete smaller magnet with its own N and S poles",
                    "Only the North half remains magnetic"
                ],
                correct: 2,
                explanation: "Magnetic monopoles do not exist in nature. Breaking a dipole magnet always produces two smaller dipoles, each with a North and South pole."
            },
            {
                category: "Oersted's Discovery",
                question: "What causes a compass needle to deflect when placed near a current-carrying wire?",
                options: [
                    "Static electric charges accumulating on the glass",
                    "Moving electric charges (current) generate a circular magnetic field around the wire",
                    "Heat radiating from the copper conductor",
                    "Gravitational attraction between the wire and the needle"
                ],
                correct: 1,
                explanation: "Hans Christian Ørsted discovered in 1820 that electric currents create magnetic fields encircling the conductor."
            },
            {
                category: "Right-Hand Rule",
                question: "Using the Right-Hand Grip Rule on a straight wire, if your right thumb points upward in the direction of conventional current, how does the magnetic field curl?",
                options: [
                    "Counter-clockwise when viewed from above",
                    "Clockwise when viewed from above",
                    "Straight downward opposite to the current",
                    "Straight upward parallel to the current"
                ],
                correct: 0,
                explanation: "Pointing your right thumb upward causes your fingers to curl counter-clockwise when looking down from above the wire."
            },
            {
                category: "Solenoids",
                question: "How does inserting a soft iron core inside a current-carrying solenoid affect its magnetic field strength?",
                options: [
                    "It blocks the magnetic field completely",
                    "It decreases the field strength by half",
                    "It dramatically increases the field strength due to high magnetic permeability",
                    "It reverses the polarity of the electromagnet"
                ],
                correct: 2,
                explanation: "Ferromagnetic materials like soft iron have a high relative permeability (μᵣ), aligning their magnetic domains with the coil's field and amplifying B."
            },
            {
                category: "Electromagnets",
                question: "According to the solenoid formula B = μ₀·μᵣ·n·I, which change will DOUBLE the magnetic field inside an electromagnet?",
                options: [
                    "Doubling the electric current (I) while keeping turns and length constant",
                    "Cutting the number of turns in half",
                    "Replacing the iron core with an air core",
                    "Reversing the battery terminals"
                ],
                correct: 0,
                explanation: "The magnetic field B inside a solenoid is directly proportional to the current I and the turn density n = N/L."
            },
            {
                category: "Faraday's Law",
                question: "What is required to induce an electric current in a stationary closed coil of wire using a permanent magnet?",
                options: [
                    "Holding a very strong magnet motionless inside the coil",
                    "Changing the magnetic flux passing through the coil over time",
                    "Connecting a resistor in series with the coil",
                    "Cooling the magnet to room temperature"
                ],
                correct: 1,
                explanation: "Faraday's Law (ℰ = -N·ΔΦ_B/Δt) states that an EMF is only induced when the magnetic flux through the loop changes."
            },
            {
                category: "Faraday's Law",
                question: "If you plunge a bar magnet into a wire coil twice as fast, what happens to the induced voltage (EMF)?",
                options: [
                    "It stays the same",
                    "It drops to zero",
                    "It doubles in magnitude",
                    "It is reduced by half"
                ],
                correct: 2,
                explanation: "Because induced EMF is proportional to the rate of change of magnetic flux (ΔΦ_B / Δt), halving the time Δt doubles the induced voltage."
            },
            {
                category: "Lenz's Law",
                question: "What does the negative sign in Faraday's Law (ℰ = -N·ΔΦ_B/Δt) represent?",
                options: [
                    "Induced voltage is always negative in volts",
                    "Lenz's Law: the induced current opposes the change in magnetic flux that caused it",
                    "Magnetic flux is always decreasing",
                    "Electrons carry a positive charge"
                ],
                correct: 1,
                explanation: "Lenz's Law ensures conservation of energy: the induced current produces a magnetic field opposing the magnet's motion."
            },
            {
                category: "Applications",
                question: "Which real-world device relies directly on Faraday's Law of Electromagnetic Induction to produce AC electricity?",
                options: [
                    "A chemical alkaline battery",
                    "A hydroelectric turbine generator",
                    "A static capacitor",
                    "A permanent compass needle"
                ],
                correct: 1,
                explanation: "Generators rotate coils within magnetic fields (or magnets near coils) to continuously change magnetic flux and induce alternating current."
            }
        ];

        let currentQIndex = 0;
        let quizScore = 0;
        let quizAnswered = false;

        function renderQuizQuestion() {
            const q = quizQuestions[currentQIndex];
            quizAnswered = false;

            document.getElementById('quiz-progress-label').textContent = `Question ${currentQIndex + 1} of ${quizQuestions.length}`;
            document.getElementById('quiz-score-label').textContent = `Score: ${quizScore}`;
            document.getElementById('quiz-progress-bar').style.width = `${((currentQIndex + 1) / quizQuestions.length) * 100}%`;
            document.getElementById('quiz-category-badge').textContent = q.category;
            document.getElementById('quiz-question-text').textContent = q.question;

            const optionsContainer = document.getElementById('quiz-options-container');
            optionsContainer.innerHTML = '';

            q.options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.className = "quiz-opt-btn w-full text-left p-4 rounded-xl bg-slate-950/80 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/50 transition flex items-center gap-3.5 text-slate-200 font-medium text-sm sm:text-base";
                btn.innerHTML = `
                    <span class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center font-mono text-xs font-bold text-cyan-400 shrink-0">${String.fromCharCode(65 + idx)}</span>
                    <span>${opt}</span>
                `;
                btn.onclick = () => selectQuizAnswer(idx);
                optionsContainer.appendChild(btn);
            });

            document.getElementById('quiz-explanation-box').classList.add('hidden');
            document.getElementById('quiz-next-btn').classList.add('hidden');
        }

        function selectQuizAnswer(selectedIdx) {
            if (quizAnswered) return;
            quizAnswered = true;

            const q = quizQuestions[currentQIndex];
            const isCorrect = selectedIdx === q.correct;
            if (isCorrect) quizScore++;

            document.getElementById('quiz-score-label').textContent = `Score: ${quizScore}`;

            const buttons = document.querySelectorAll('.quiz-opt-btn');
            buttons.forEach((btn, idx) => {
                btn.disabled = true;
                btn.classList.remove('hover:bg-slate-800/90', 'hover:border-cyan-500/50');
                if (idx === q.correct) {
                    btn.className = "quiz-opt-btn w-full text-left p-4 rounded-xl bg-emerald-500/20 border border-emerald-500 text-emerald-200 font-semibold flex items-center gap-3.5 text-sm sm:text-base";
                } else if (idx === selectedIdx && !isCorrect) {
                    btn.className = "quiz-opt-btn w-full text-left p-4 rounded-xl bg-rose-500/20 border border-rose-500 text-rose-200 font-semibold flex items-center gap-3.5 text-sm sm:text-base";
                } else {
                    btn.classList.add('opacity-50');
                }
            });

            const expBox = document.getElementById('quiz-explanation-box');
            const fbTitle = document.getElementById('quiz-feedback-title');
            const expText = document.getElementById('quiz-explanation-text');

            expBox.classList.remove('hidden');
            if (isCorrect) {
                fbTitle.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400"></i> <span class="text-emerald-400">Correct!</span>`;
            } else {
                fbTitle.innerHTML = `<i class="fa-solid fa-circle-xmark text-rose-400"></i> <span class="text-rose-400">Incorrect</span>`;
            }
            expText.textContent = q.explanation;

            const nextBtn = document.getElementById('quiz-next-btn');
            nextBtn.classList.remove('hidden');
            nextBtn.querySelector('span').textContent = currentQIndex === quizQuestions.length - 1 ? 'View Final Results' : 'Next Question';
        }

        function nextQuizQuestion() {
            currentQIndex++;
            if (currentQIndex < quizQuestions.length) {
                renderQuizQuestion();
            } else {
                showQuizResults();
            }
        }

        function showQuizResults() {
            document.getElementById('quiz-active-box').classList.add('hidden');
            document.getElementById('quiz-results-box').classList.remove('hidden');

            const pct = Math.round((quizScore / quizQuestions.length) * 100);
            document.getElementById('quiz-final-score').textContent = `${quizScore} / ${quizQuestions.length}`;
            document.getElementById('quiz-final-percent').textContent = `${pct}%`;

            const titleEl = document.getElementById('quiz-rank-title');
            const descEl = document.getElementById('quiz-rank-desc');
            const iconEl = document.getElementById('quiz-rank-icon');

            if (quizScore >= 9) {
                titleEl.textContent = "Electromagnetism Master";
                descEl.textContent = "Phenomenal! You have mastered Maxwell's foundational concepts, solenoids, and Faraday induction.";
                iconEl.className = "fa-solid fa-crown text-4xl text-white";
            } else if (quizScore >= 6) {
                titleEl.textContent = "Field Technician";
                descEl.textContent = "Solid work! You understand core magnetic principles. Review the Concept Explorer to push for 100%.";
                iconEl.className = "fa-solid fa-award text-4xl text-white";
            } else {
                titleEl.textContent = "Lab Novice";
                descEl.textContent = "Good start! Experiment with the three interactive simulators in the Lab tab and try again.";
                iconEl.className = "fa-solid fa-atom text-4xl text-white";
            }
        }

        function restartQuiz() {
            currentQIndex = 0;
            quizScore = 0;
            document.getElementById('quiz-results-box').classList.add('hidden');
            document.getElementById('quiz-active-box').classList.remove('hidden');
            renderQuizQuestion();
        }

        // =========================================================
        // 8. INITIALIZATION ON WINDOW LOAD
        // =========================================================
        window.onload = function () {
            resizeAllCanvases();
            renderQuizQuestion();
            animateLoop();
        };
    </script>
</body>
</html>