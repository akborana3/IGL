/** Premium footer. */

import Link from "next/link";
import { APP_NAME, APP_TAGLINE } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="mt-20 border-t border-white/5 glass">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <h3 className="text-2xl font-bold gradient-text mb-2">{APP_NAME}</h3>
            <p className="text-gray-400 text-sm max-w-md">{APP_TAGLINE}</p>
            <p className="text-gray-500 text-xs mt-4">
              A premium streaming experience powered by cutting-edge technology.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Explore</h4>
            <ul className="space-y-2">
              <li><Link href="/browse" className="text-gray-400 hover:text-white text-sm transition-colors">Browse</Link></li>
              <li><Link href="/categories" className="text-gray-400 hover:text-white text-sm transition-colors">Categories</Link></li>
              <li><Link href="/search" className="text-gray-400 hover:text-white text-sm transition-colors">Search</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-3">About</h4>
            <ul className="space-y-2">
              <li><span className="text-gray-400 text-sm">About Us</span></li>
              <li><span className="text-gray-400 text-sm">Contact</span></li>
              <li><span className="text-gray-400 text-sm">Privacy Policy</span></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/5 text-center">
          <p className="text-gray-500 text-xs">
            © {new Date().getFullYear()} {APP_NAME}. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
