import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Play, Shuffle, RotateCcw, Zap, Clock, Trophy } from 'lucide-react'

export default function ControlPanel({ 
  onScramble, 
  onSolve, 
  onReset, 
  onApplyMove,
  isLoading = false,
  isSolved = false,
  moveHistory = [],
  solutionMoves = []
}) {
  const [selectedMove, setSelectedMove] = useState('')
  
  const basicMoves = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]
  
  const handleMoveClick = (move) => {
    setSelectedMove(move)
    onApplyMove(move)
  }
  
  return (
    <div className="space-y-6">
      {/* Status Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="h-5 w-5" />
            Cube Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2 mb-4">
            <Badge variant={isSolved ? "default" : "secondary"}>
              {isSolved ? "Solved" : "Scrambled"}
            </Badge>
            <Badge variant="outline">
              {moveHistory.length} moves
            </Badge>
          </div>
          
          {solutionMoves.length > 0 && (
            <div className="space-y-2">
              <p className="text-sm font-medium">Solution Found:</p>
              <div className="flex flex-wrap gap-1">
                {solutionMoves.map((move, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    {move}
                  </Badge>
                ))}
              </div>
              <p className="text-xs text-muted-foreground">
                {solutionMoves.length} moves to solve
              </p>
            </div>
          )}
        </CardContent>
      </Card>
      
      {/* Main Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5" />
            Quick Actions
          </CardTitle>
          <CardDescription>
            Control your Rubik's Cube with these actions
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-3">
            <Button 
              onClick={onScramble} 
              disabled={isLoading}
              className="w-full"
              variant="outline"
            >
              <Shuffle className="h-4 w-4 mr-2" />
              Scramble Cube
            </Button>
            
            <Button 
              onClick={onSolve} 
              disabled={isLoading || isSolved}
              className="w-full"
            >
              <Play className="h-4 w-4 mr-2" />
              {isLoading ? "Solving..." : "Solve Cube"}
            </Button>
            
            <Button 
              onClick={onReset} 
              disabled={isLoading}
              variant="secondary"
              className="w-full"
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Reset to Solved
            </Button>
          </div>
        </CardContent>
      </Card>
      
      {/* Manual Moves */}
      <Card>
        <CardHeader>
          <CardTitle>Manual Moves</CardTitle>
          <CardDescription>
            Click to apply individual moves to the cube
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-2">
            {basicMoves.map((move) => (
              <Button
                key={move}
                variant={selectedMove === move ? "default" : "outline"}
                size="sm"
                onClick={() => handleMoveClick(move)}
                disabled={isLoading}
                className="font-mono"
              >
                {move}
              </Button>
            ))}
          </div>
          
          <Separator className="my-4" />
          
          <div className="space-y-2">
            <p className="text-sm font-medium">Move Notation:</p>
            <div className="text-xs text-muted-foreground space-y-1">
              <p><strong>U/D:</strong> Up/Down face</p>
              <p><strong>R/L:</strong> Right/Left face</p>
              <p><strong>F/B:</strong> Front/Back face</p>
              <p><strong>':</strong> Counter-clockwise rotation</p>
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Move History */}
      {moveHistory.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Move History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-1 max-h-32 overflow-y-auto">
              {moveHistory.map((move, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {index + 1}. {move}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

