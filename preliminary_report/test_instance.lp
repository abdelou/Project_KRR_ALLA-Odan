% test_instance.lp
regions(2).
symbol_type(1..2).

% Board: 2x2x2 cube
cube(0..1, 0..1, 0..1).

% Symbols: region 1 and region 2 each need one of type 1 and type 2.
symbol(0,0,0, 1).
symbol(1,1,1, 1).
symbol(1,0,0, 2).
symbol(0,1,1, 2).

% Walls
wall(0,0,0, 0,0,1).
wall(1,1,1, 1,1,0).
