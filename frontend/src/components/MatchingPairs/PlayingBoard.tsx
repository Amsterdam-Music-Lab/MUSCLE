import React from "react";
import "./PlayingBoard.scss";

interface PlayingBoardProps {
  columns: number;
  children: React.ReactNode;
}

const PlayingBoard = ({ columns = 4, children }: PlayingBoardProps) => {
  console.log(children.length, children[2])
  return (
    <div className="mcg-playing-board aspect-square sharp-border bg-inset-lg md-flush">
        <div className="square-grid" style={{"--columns": columns}}>
          {children}
      </div>
    </div>
  )
}

export default PlayingBoard
