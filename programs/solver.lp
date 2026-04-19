% solver.lp
% 3D Symbolic Region Puzzle - Solver
% Authors: Abdelouahad Alla & Odan Lafrance

% Input specifications (provided by the puzzle instance):
% cube(X,Y,Z) : represents a cell of the non-planar polycube board.
% symbol(X,Y,Z, S) : indicates a symbol of type S at cell (X,Y,Z).
% wall(X,Y,Z, X',Y',Z') : represents a wall between two face-adjacent cubes.
% regions(M) : the required number of regions.
% symbol_type(S) : the types of symbols (1..K).

% Ensure walls are treated symmetrically
u_wall(X,Y,Z, X',Y',Z') :- wall(X,Y,Z, X',Y',Z').
u_wall(X',Y',Z', X,Y,Z) :- wall(X,Y,Z, X',Y',Z').

% -------------------------------------------------------------
% Rule 1: Coverage
% Every cube is assigned to exactly one region 1..M
1 { region(X,Y,Z, R) : R = 1..M } 1 :- cube(X,Y,Z), regions(M).

% -------------------------------------------------------------
% Rule 2: Connectivity
% Cubes are topologically face-adjacent if they differ by 1 in exactly one coordinate
adj_board(X,Y,Z, X',Y',Z') :- cube(X,Y,Z), cube(X',Y',Z'), |X-X'| + |Y-Y'| + |Z-Z'| == 1.

% Two adjacent cubes are connected if there is no wall between them
adj(X,Y,Z, X',Y',Z') :- adj_board(X,Y,Z, X',Y',Z'), not u_wall(X,Y,Z, X',Y',Z').

% Adjacency within the same region
adj_region(X,Y,Z, X',Y',Z') :- adj(X,Y,Z, X',Y',Z'), region(X,Y,Z, R), region(X',Y',Z', R).

% Define the root of each region (lexicographically smallest coordinate in the region)
root(X,Y,Z, R) :- region(X,Y,Z, R), 
                  not region(X',Y',Z', R) : cube(X',Y',Z'), (X',Y',Z') < (X,Y,Z).

% Reachability from the root within the region
reachable(X,Y,Z, R) :- root(X,Y,Z, R).
reachable(X',Y',Z', R) :- reachable(X,Y,Z, R), adj_region(X,Y,Z, X',Y',Z').

% Constraint: all cubes in a region must be reachable from its root
:- region(X,Y,Z, R), not reachable(X,Y,Z, R).

% -------------------------------------------------------------
% Rule 3: Non-planarity
% Each region must extend in all three spatial dimensions
distinct_x(R, X) :- region(X,Y,Z, R).
distinct_y(R, Y) :- region(X,Y,Z, R).
distinct_z(R, Z) :- region(X,Y,Z, R).

:- regions(M), R=1..M, #count { X : distinct_x(R, X) } < 2.
:- regions(M), R=1..M, #count { Y : distinct_y(R, Y) } < 2.
:- regions(M), R=1..M, #count { Z : distinct_z(R, Z) } < 2.

% -------------------------------------------------------------
% Rule 4: Symbol completeness
% Each region contains exactly one symbol of each type.
:- regions(M), R=1..M, symbol_type(S), #count { X,Y,Z : region(X,Y,Z, R), symbol(X,Y,Z, S) } != 1.

% -------------------------------------------------------------
% Rule 5: Wall separation
% For every wall, the separated cubes must belong to different regions.
:- u_wall(X,Y,Z, X',Y',Z'), region(X,Y,Z, R), region(X',Y',Z', R).

#show region/4.
