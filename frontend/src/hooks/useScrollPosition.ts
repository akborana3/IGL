/** Scroll position hook for navbar behavior. */

import { useEffect, useState } from "react";

export function useScrollPosition(threshold: number = 50) {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handler = () => {
      setIsScrolled(window.scrollY > threshold);
    };
    window.addEventListener("scroll", handler, { passive: true });
    handler();
    return () => window.removeEventListener("scroll", handler);
  }, [threshold]);

  return isScrolled;
}
