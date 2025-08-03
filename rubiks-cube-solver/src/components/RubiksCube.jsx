import React, { useRef, useState, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Box, Text } from '@react-three/drei'
import * as THREE from 'three'

// Color mapping for cube faces
const COLORS = {
  0: '#ffffff', // White
  1: '#ffff00', // Yellow
  2: '#ff0000', // Red
  3: '#ff8000', // Orange
  4: '#00ff00', // Green
  5: '#0000ff'  // Blue
}

// Individual cube piece component
function CubePiece({ position, colors, size = 0.95 }) {
  const meshRef = useRef()
  
  return (
    <group position={position}>
      <Box ref={meshRef} args={[size, size, size]}>
        <meshStandardMaterial color="#333333" />
      </Box>
      
      {/* Face stickers */}
      {colors.map((color, index) => {
        if (color === null) return null
        
        const facePositions = [
          [0.5, 0, 0],   // Right face
          [-0.5, 0, 0],  // Left face
          [0, 0.5, 0],   // Top face
          [0, -0.5, 0],  // Bottom face
          [0, 0, 0.5],   // Front face
          [0, 0, -0.5]   // Back face
        ]
        
        const faceRotations = [
          [0, Math.PI/2, 0],   // Right
          [0, -Math.PI/2, 0],  // Left
          [-Math.PI/2, 0, 0],  // Top
          [Math.PI/2, 0, 0],   // Bottom
          [0, 0, 0],           // Front
          [0, Math.PI, 0]      // Back
        ]
        
        return (
          <Box
            key={index}
            position={facePositions[index]}
            rotation={faceRotations[index]}
            args={[0.9, 0.9, 0.01]}
          >
            <meshStandardMaterial color={COLORS[color]} />
          </Box>
        )
      })}
    </group>
  )
}

// Main Rubik's Cube component
function RubiksCube3D({ cubeState, isAnimating = false }) {
  const groupRef = useRef()
  
  // Auto-rotate the cube when not being manually controlled
  useFrame((state, delta) => {
    if (groupRef.current && !isAnimating) {
      groupRef.current.rotation.y += delta * 0.2
    }
  })
  
  // Generate cube pieces from state
  const generateCubePieces = () => {
    const pieces = []
    
    // For a 3x3 cube, we have 27 pieces (including the invisible center)
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          // Skip the center piece (not visible)
          if (x === 0 && y === 0 && z === 0) continue
          
          const position = [x * 1.1, y * 1.1, z * 1.1]
          
          // Determine which faces are visible for this piece
          const colors = [null, null, null, null, null, null]
          
          // Right face (x = 1)
          if (x === 1) colors[0] = 4 // Green
          // Left face (x = -1)
          if (x === -1) colors[1] = 5 // Blue
          // Top face (y = 1)
          if (y === 1) colors[2] = 0 // White
          // Bottom face (y = -1)
          if (y === -1) colors[3] = 1 // Yellow
          // Front face (z = 1)
          if (z === 1) colors[4] = 2 // Red
          // Back face (z = -1)
          if (z === -1) colors[5] = 3 // Orange
          
          pieces.push(
            <CubePiece
              key={`${x}-${y}-${z}`}
              position={position}
              colors={colors}
            />
          )
        }
      }
    }
    
    return pieces
  }
  
  return (
    <group ref={groupRef}>
      {generateCubePieces()}
    </group>
  )
}

// Main component that includes the Canvas
export default function RubiksCubeViewer({ cubeState, className = "" }) {
  return (
    <div className={`w-full h-full ${className}`}>
      <Canvas
        camera={{ position: [5, 5, 5], fov: 60 }}
        style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
      >
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />
        
        <RubiksCube3D cubeState={cubeState} />
        
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={3}
          maxDistance={15}
        />
      </Canvas>
    </div>
  )
}

