/** Beautiful error page. */
"use client";

"use client";

import { motion } from "framer-motion";
import { AlertCircle, RefreshCw } from "lucide-react";

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        <AlertCircle className="w-16 h-16 text-neon-purple mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-white mb-2">Something went wrong</h1>
        <p className="text-gray-400 mb-6">An unexpected error occurred. Please try again.</p>
        <button
          onClick={reset}
          className="px-6 py-3 rounded-xl glass-strong text-white font-medium hover:bg-white/10 transition-colors flex items-center gap-2 mx-auto"
        >
          <RefreshCw size={18} /> Try Again
        </button>
      </motion.div>
    </div>
  );
}