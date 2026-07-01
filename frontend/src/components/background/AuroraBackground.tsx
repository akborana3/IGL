/** Animated aurora background with React Three Fiber — floating particles, glowing orbs, parallax. */

"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { useMemo, useRef, Suspense } from "react";
import * as THREE from "three";

function FloatingOrbs() {
  const groupRef = useRef<THREE.Group>(null);

  const orbs = useMemo(() => {
    return Array.from({ length: 5 }).map((_, i) => ({
      position: [
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 4 - 2,
      ] as [number, number, number],
      color: i % 2 === 0 ? "#a855f7" : "#3b82f6",
      scale: 0.5 + Math.random() * 1.5,
      speed: 0.3 + Math.random() * 0.5,
    }));
  }, []);

  useFrame((state) => {
    if (!groupRef.current) return;
    const t = state.clock.elapsedTime;
    groupRef.current.children.forEach((child, i) => {
      child.position.y = orbs[i].position[1] + Math.sin(t * orbs[i].speed) * 0.5;
      child.position.x = orbs[i].position[0] + Math.cos(t * orbs[i].speed * 0.7) * 0.3;
    });
    // Subtle parallax with mouse
    groupRef.current.rotation.y = state.mouse.x * 0.1;
    groupRef.current.rotation.x = state.mouse.y * 0.05;
  });

  return (
    <group ref={groupRef}>
      {orbs.map((orb, i) => (
        <mesh key={i} position={orb.position} scale={orb.scale}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshBasicMaterial color={orb.color} transparent opacity={0.08} />
        </mesh>
      ))}
    </group>
  );
}

function Particles() {
  const pointsRef = useRef<THREE.Points>(null);

  const positions = useMemo(() => {
    const count = 200;
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      arr[i * 3] = (Math.random() - 0.5) * 20;
      arr[i * 3 + 1] = (Math.random() - 0.5) * 12;
      arr[i * 3 + 2] = (Math.random() - 0.5) * 6 - 2;
    }
    return arr;
  }, []);

  useFrame((state) => {
    if (!pointsRef.current) return;
    pointsRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    pointsRef.current.rotation.x = state.clock.elapsedTime * 0.01;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.03}
        color="#a855f7"
        transparent
        opacity={0.4}
        sizeAttenuation
      />
    </points>
  );
}

export function AuroraBackground() {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none">
      {/* CSS aurora gradient base */}
      <div className="absolute inset-0 aurora-bg opacity-60" />

      {/* Three.js canvas overlay */}
      <Canvas
        camera={{ position: [0, 0, 5], fov: 60 }}
        style={{ background: "transparent" }}
        dpr={[1, 1.5]}
      >
        <Suspense fallback={null}>
          <FloatingOrbs />
          <Particles />
        </Suspense>
      </Canvas>

      {/* Vignette overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#0a0a0f]" />
    </div>
  );
}
