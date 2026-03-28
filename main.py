import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const AdaptationWheel = ({ factor = 32 }) => {
  const [timeLeft, setTimeLeft] = useState(14);
  const [activeSegments, setActiveSegments] = useState([]);

  // Lógica del Temporizador de 14 segundos
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev <= 1 ? 14 : prev - 1));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Simulación de "Procesamiento de Datos" en los segmentos
  useEffect(() => {
    const interval = setInterval(() => {
      const randomSegments = Array.from({ length: 3 }, () => Math.floor(Math.random() * 8));
      setActiveSegments(randomSegments);
    }, 800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-[#0A0E14] border border-[#1A1F26] rounded-sm shadow-2xl">
      <span className="text-[10px] text-gray-600 tracking-[0.2em] mb-4 uppercase font-mono">
        Adaptation Engine
      </span>

      <div className="relative w-40 h-40 flex items-center justify-center">
        {/* Rueda de Segmentos Radiales */}
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 w-full h-full"
        >
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className="absolute top-0 left-1/2 w-[2px] h-1/2 origin-bottom transition-all duration-300"
              style={{
                transform: `translateX(-50%) rotate(${i * 45}deg)`,
                background: activeSegments.includes(i) 
                  ? 'linear-gradient(to top, #00F2FF, transparent)' 
                  : 'linear-gradient(to top, #1A1F26, transparent)',
                opacity: activeSegments.includes(i) ? 1 : 0.3
              }}
            />
          ))}
        </motion.div>

        {/* Timón Central (Icono de Mahoraga) */}
        <div className="relative z-10 w-16 h-16 bg-[#0A0E14] border-2 border-[#00F2FF] rounded-full flex items-center justify-center shadow-[0_0_15px_rgba(0,242,255,0.3)]">
          <span className="text-3xl text-[#00F2FF] drop-shadow-[0_0_5px_#00F2FF]">☸</span>
        </div>
      </div>

      {/* Status y Timer */}
      <div className="mt-6 text-center font-mono">
        <div className="text-[#8A2BE2] text-xs font-bold tracking-widest uppercase">
          Next Check: <span className="text-white">{timeLeft}s</span>
        </div>
        <div className="text-[10px] text-gray-500 mt-1">
          FACTOR_SET: <span className="text-[#00F2FF]">{factor}</span>
        </div>
      </div>
    </div>
  );
};

export default AdaptationWheel;
