import java.util.ArrayList;  

public class MoveChooser {
  
    public static Move chooseMove(BoardState boardState){

	    int searchDepth= Othello.searchDepth;
        ArrayList<Move> moves= boardState.getLegalMoves();// this will only return the move options for white
        if(moves.isEmpty()){
            return null;
	    }
        int optimum_value = Alpha_Beta(boardState,searchDepth,-10000,10000,true); // generate a optimum value
        int optimum_move_index = -1;
        for(int i=0; i<moves.size(); i++) {
            BoardState try_boardState = boardState.deepCopy();
            try_boardState.setContents(moves.get(i).x,moves.get(i).y,1); // first level option states
            int try_score =  Alpha_Beta(try_boardState,searchDepth-1, -10000,10000,false);
//            System.out.println("Move option: " + (i+1));
//            System.out.println("x: "+ moves.get(i).x);
//            System.out.println("y: "+ moves.get(i).y);
//            System.out.println("Try score: " + try_score);
            if(try_score == optimum_value){
                optimum_move_index = i;
//                System.out.println("Optimum score: " + optimum_value);
                break;
            }
        }
//        System.out.println("Current move");
//        System.out.println("x: "+ moves.get(optimum_move_index).x);
//        System.out.println("y: "+ moves.get(optimum_move_index).y);
//        System.out.println("Alpha-beta results: " + optimum_value);
        return moves.get(optimum_move_index);

//        return moves.get(0);
    }

    //assign value to each square, with input of current boardState
    public static int evaluation(BoardState boardState){
        int[][] square_array = {
                {120,-20,20,5,5,20,-20,120},
                {-20,-40,-5,-5,-5,-5,-40,-20},
                {20,-5,15,3,3,15,-5,20},
                {5,-5,3,3,3,3,-5,5},
                {5,-5,3,3,3,3,-5,5},
                {20,-5,15,3,3,15,-5,20},
                {-20,-40,-5,-5,-5,-5,-40,-20},
                {120,-20,20,5,5,20,-20,120}
        };

        // loop through the board and check the position of each black piece and white piece
        // then calculate the score value of a board position can then be defined by adding up the weights of
        // all those squares occupied by white pieces and subtracting the weights of those squares occupied by black
        // pieces. Thus, the value is always counted from white’s point of view.
        int value = 0;
        for(int i= 0; i < 8; i++){
            for(int j=0; j < 8; j++){
                if(boardState.getContents(i,j)==1)
                    value = value + square_array[i][j];
                else if(boardState.getContents(i,j)==-1)
                    value = value - square_array[i][j];
            }

        }
        return value;

    }

    public static int Alpha_Beta(BoardState node, int depth, int alpha, int beta, boolean maximizingPlayer) {
        // as we help the computer to make decisions, the computer is maximizingplayer
        // depth = 0 means we dont search
        ArrayList<Move> moves = node.getLegalMoves(); // black and white moves in turn, white first
        if (depth == 0|| moves.isEmpty()) {
            return evaluation(node);
        }
        // search according to depth
        else {
            // now is white piece's turn
            if (maximizingPlayer) {
                // for loop makes every child of the current node will search in depth of val(depth)
                for (int i = 0; i < moves.size(); i++) {
                    BoardState try_boardState = node.deepCopy();
                    try_boardState.setContents(moves.get(i).x, moves.get(i).y, 1);
                    alpha = Math.max(alpha, Alpha_Beta(try_boardState, depth - 1, alpha, beta, false));
                    //pruning
                    if (alpha >= beta) {
                        break;
                    }
                }
                return alpha;
            } else {
                for (int i = 0; i < moves.size(); i++) {
                    BoardState try_boardState = node.deepCopy();
                    try_boardState.setContents(moves.get(i).x, moves.get(i).y, -1);
                    beta = Math.min(beta, Alpha_Beta(try_boardState, depth - 1, alpha, beta, true));
                    //pruning
                    if (alpha >= beta) {
                        break;
                    }
                }
                return beta;
            }
        }
    }

}
