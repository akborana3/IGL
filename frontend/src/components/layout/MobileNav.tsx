/** Mobile bottom navigation — animated. */

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Compass, Grid3x3, Search } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const MOBILE_LINKS = [
  { href: "/", label: "Home", icon: Home },
  { href: "/browse", label: "Browse", icon: Compass },
  { href: "/categories", label: "Categories", icon: Grid3x3 },
  { href: "/search", label: "Search", icon: Search },
];

export function MobileNav() {
  const pathname = usePathname();

  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 glass-strong border-t border-white/10 pb-safe">
      <div className="flex items-center justify-around py-2">
        {MOBILE_LINKS.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className="flex flex-col items-center gap-1 px-3 py-1"
            >
              <motion.div
                animate={{ scale: isActive ? 1.1 : 1 }}
                className={cn(isActive ? "text-neon-purple" : "text-gray-500")}
              >
                <Icon size={20} />
              </motion.div>
              <span className={cn(
                "text-[10px] font-medium",
                isActive ? "text-neon-purple" : "text-gray-500"
              )}>
                {link.label}
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
