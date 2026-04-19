% generator.lp
% 3D Symbolic Region Puzzle - Map Generator
% Authors: Abdelouahad Alla & Odan Lafrance

% Execution parameters (can be overridden from clingo command line, e.g., -c c=12 -c n=4)
#const c = 12. % total cubes in the polycube board (c >= m*k)
#const n = 4.  % bounding box size dimension (1..n)
#const m = 3.  % number of regions
#const k = 2.  % number of distinct symbol types
#const w = 4.  % number of walls to place on the board

regions(m).
symbol_type(1..k).
dim(1..n).

% -------------------------------------------------------------
% 1. Board Generation
% Generate exactly c cubes within the bounding box
c { cube(X,Y,Z) : dim(X), dim(Y), dim(Z) } c.

% Connectivity rule for the board
adj_board(X,Y,Z, X',Y',Z') :- cube(X,Y,Z), cube(X',Y',Z'), |X-X'| + |Y-Y'| + |Z-Z'| == 1.

root_board(X,Y,Z) :- cube(X,Y,Z), not cube(X',Y',Z') : cube(X',Y',Z'), (X',Y',Z') < (X,Y,Z).
reach_board(X,Y,Z) :- root_board(X,Y,Z).
reach_board(X',Y',Z') :- reach_board(X,Y,Z), adj_board(X,Y,Z, X',Y',Z').

% Force all cubes to be connected
:- cube(X,Y,Z), not reach_board(X,Y,Z).

% Non-planarity of the overall board
:- #count { X : cube(X,Y,Z) } < 3.
:- #count { Y : cube(X,Y,Z) } < 3.
:- #count { Z : cube(X,Y,Z) } < 3.

% -------------------------------------------------------------
% 2. Symbol Placement
% Place exactly m symbols for each symbol type S
m { symbol(X,Y,Z, S) : cube(X,Y,Z) } m :- symbol_type(S).

% Constraints: each cube can hold at most one symbol
:- cube(X,Y,Z), #count { S : symbol(X,Y,Z,S) } > 1.

% -------------------------------------------------------------
% 3. Wall Placement
potential_wall(X,Y,Z, X',Y',Z') :- adj_board(X,Y,Z, X',Y',Z'), (X,Y,Z) < (X',Y',Z').

% Select exactly w walls from the adjacent cubes
w { wall(X,Y,Z, X',Y',Z') : potential_wall(X,Y,Z, X',Y',Z') } w.

% -------------------------------------------------------------
% 4. Solvability Guarantee (Embedded Solver)
% We embed solving rules to ensure generated instance is actually solvable!

u_wall(X,Y,Z, X',Y',Z') :- wall(X,Y,Z, X',Y',Z').
u_wall(X',Y',Z', X,Y,Z) :- wall(X,Y,Z, X',Y',Z').

% Coverage
1 { region(X,Y,Z, R) : R = 1..m } 1 :- cube(X,Y,Z).

% Connectivity
adj_region(X,Y,Z, X',Y',Z') :- adj_board(X,Y,Z, X',Y',Z'), not u_wall(X,Y,Z, X',Y',Z'), region(X,Y,Z,R), region(X',Y',Z',R).

root_reg(X,Y,Z, R) :- region(X,Y,Z,R), not region(X',Y',Z',R) : cube(X',Y',Z'), (X',Y',Z') < (X,Y,Z).
reach_reg(X,Y,Z, R) :- root_reg(X,Y,Z, R).
reach_reg(X',Y',Z', R) :- reach_reg(X,Y,Z, R), adj_region(X,Y,Z, X',Y',Z').
:- region(X,Y,Z, R), not reach_reg(X,Y,Z, R).

% Non-planarity
distinct_x(R, X) :- region(X,Y,Z, R).
distinct_y(R, Y) :- region(X,Y,Z, R).
distinct_z(R, Z) :- region(X,Y,Z, R).
:- R=1..m, #count { X : distinct_x(R, X) } < 2.
:- R=1..m, #count { Y : distinct_y(R, Y) } < 2.
:- R=1..m, #count { Z : distinct_z(R, Z) } < 2.

% Symbol completeness
:- R=1..m, symbol_type(S), #count { X,Y,Z : region(X,Y,Z, R), symbol(X,Y,Z, S) } != 1.

% Wall separation
:- u_wall(X,Y,Z, X',Y',Z'), region(X,Y,Z, R), region(X',Y',Z', R).

% Make sure clingo hides the intermediate solver variables during board generation
#show cube/3.
#show symbol/4.
#show wall/6.
#show regions/1.
#show symbol_type/1.
