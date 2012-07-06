parser grammar events;

// This file is part of Demystify.
// 
// Demystify: a Magic: The Gathering parser
// Copyright (C) 2012 Benjamin S Wolf
// 
// Demystify is free software; you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published
// by the Free Software Foundation; either version 3 of the License,
// or (at your option) any later version.
// 
// Demystify is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with Demystify.  If not, see <http://www.gnu.org/licenses/>.

/* Events and conditions. */

// Although it doesn't look great, it was necessary to factor 'subset' out
// of the event and condition rules. It's a bad idea to leave it unfactored
// since ANTLR will run itself out of memory (presumably trying to generate
// lookahead tables).
trigger : subset
          ( event -> ^( EVENT subset event )
          | condition -> ^( CONDITION subset condition )
          );

// An event is something that happens, usually an object taking an action
// or having an action done to it.

event : zone_transfer
      | phases_in_out
      ;

/* Events. */

zone_transfer : ( ENTER | ( IS | ARE ) PUT ( INTO | ONTO ) ) a=zone_subset
                ( FROM ( b=zone_subset | ANYWHERE ) )?
                -> ^( ENTER[] $a ^( FROM[] $b? ANYWHERE[]? )? )
              | LEAVE zone_subset
                -> ^( LEAVE[] zone_subset )
              | DIE
                -> ^( ENTER[] ^( ZONE_SET ^( NUMBER NUMBER[$DIE, "1"] ) GRAVEYARD )
                              ^( FROM[] BATTLEFIELD ) )
              ;

phases_in_out : PHASE^ ( IN | OUT );

// A condition is a true-or-false statement about the game state. These
// types of triggered abilities (sometimes called "state triggers") will
// trigger any time that statement is true and it isn't already on the stack.
// Since otherwise this would lead to a mandatory loop, the effects of these
// triggered conditions usually serve to end the game or change the relevant
// state (e.g. 'when SELF has flying, sacrifice it').

condition : has_ability
          | HAS! has_counters
          ;

/* Conditions. */

has_ability : HAS raw_keyword -> ^( HAS[] raw_keyword );
