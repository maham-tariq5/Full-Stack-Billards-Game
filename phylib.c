#include "phylib.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>



// Function #1

phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos ) 
{

    // dynamically allocating space for the new still ball
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    // if memory allocation fails, return NULL
    if (new_object == NULL) 
    {
        return NULL; 
    }

    // Setting the new object to to its still ball type
    new_object->type = PHYLIB_STILL_BALL;

    // tranferring still ball info into the structure
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos.x = pos->x;
    new_object->obj.still_ball.pos.y = pos->y;

    
    return new_object;
}

// Function #2 

phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc ) 
{

    phylib_object *new_roll_object = (phylib_object *)malloc(sizeof(phylib_object));

    if (new_roll_object == NULL)
    {
        return NULL;
    }

    new_roll_object->type = PHYLIB_ROLLING_BALL;

    new_roll_object->obj.rolling_ball.number = number;
    
    // setting x and y positions tranferring in struct
    new_roll_object->obj.rolling_ball.pos.x = pos->x;
    new_roll_object->obj.rolling_ball.pos.y = pos->y;
   
     // setting x and y velocity transfering in struct
    new_roll_object->obj.rolling_ball.vel.x = vel->x;
    new_roll_object->obj.rolling_ball.vel.y = vel->y;

     // setting x and y accerlation into struct
    new_roll_object->obj.rolling_ball.acc.x = acc->x;
    new_roll_object->obj.rolling_ball.acc.y = acc->y;

    return new_roll_object;

}

// Function 3

phylib_object *phylib_new_hole( phylib_coord *pos ) 
{

    phylib_object *new_hole_object = (phylib_object *)malloc(sizeof(phylib_object));

    if (new_hole_object == NULL)
    {
        return NULL;
    }

    new_hole_object->type = PHYLIB_HOLE;

    new_hole_object->obj.hole.pos.x = pos->x;
    new_hole_object->obj.hole.pos.y = pos->y;

    return new_hole_object;
}


// Function #4
phylib_object *phylib_new_hcushion( double y )
{

    phylib_object *new_hcushion = (phylib_object *)malloc(sizeof(phylib_object));

    if (new_hcushion == NULL) 
    {
        return NULL;
    }

    new_hcushion->type = PHYLIB_HCUSHION;

    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;

}

// Function #5
phylib_object *phylib_new_vcushion( double x ) 
{

    phylib_object *new_vcushion = (phylib_object *)malloc(sizeof(phylib_object));

    if (new_vcushion == NULL) 
    {
        return NULL;
    }

    new_vcushion->type = PHYLIB_VCUSHION;

    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;

}

// Function #6
phylib_table *phylib_new_table( void )
{

    // allocating space for new table
    phylib_table *table = (phylib_table *)malloc(sizeof(phylib_table));

    // if allocation fails check
    if (table == NULL)
    {
        return NULL;
    }

    table->time = 0.0;  // intital time for new table

    // setting objects to NULL 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        table->object[i] = NULL;
    }

    // Create and place the cushions and holes
    table->object[0] = phylib_new_hcushion(0.0); // Bottom horizontal cushion
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); // Top horizontal cushion
    table->object[2] = phylib_new_vcushion(0.0); // Left vertical cushion
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); // Right vertical cushion


    phylib_coord hole_positions[6] = 
    {
        {0.0, 0.0}, // Bottom-left corner hole
        {0.0, PHYLIB_TABLE_WIDTH }, // Bottom-right corner hole
        {0.0, PHYLIB_TABLE_LENGTH}, 
        {PHYLIB_TABLE_WIDTH,0.0 }, 
        {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH}, // Middle bottom hole
        {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH} // Middle top hole
    };

    // Create the holes and place them in the object array
    for (int i = 0; i < 6; i++) 
    {
        table->object[4 + i] = phylib_new_hole(&hole_positions[i]);
    }

    // Return the pointer to the new table
    return table;




}

// Part 2 utility functions

// function #1

void phylib_copy_object(phylib_object **dest, phylib_object **src) 
{
 
    // checking if NULL
    if (src == NULL || *src == NULL) 
    {
        *dest = NULL;
        return;
    }
    
    // Allocate memory for desired desination
    *dest = (phylib_object *)malloc(sizeof(phylib_object));
    
    // checking for allocation fail
    if (*dest == NULL) 
    {
        return;
    }
    
    // Using memcpy for simplcity
    memcpy(*dest, *src, sizeof(phylib_object));
}


// Function #2

phylib_table *phylib_copy_table(phylib_table *table) 
{

    // Allocate memory for a new table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    
    // checking for allocation fail of new table
    if (new_table == NULL) 
    {
        return NULL;
    }

    //  time field
    new_table->time = table->time;

    // copy of the object pointers
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
       // using copy object function for cleaner code and making sure it makes deep copy for each object
       phylib_copy_object(&(new_table->object[i]), &(table->object[i]));
    }

    // Return the address of the new table
    return new_table;
}

// Function #3

void phylib_add_object( phylib_table *table, phylib_object *object ) 
{

    // iteriating through the object array
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        // if a spot for an object is NULL we can add a new object there and exit the function after
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }

    }

}

// Function #4

void phylib_free_table( phylib_table *table ) 
{

    // iterating through to free evert single object in table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        free(table->object[i]);
    }
    // freeing the table after objects are freed
    free(table);

}

// Function #5 

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) 
{

    phylib_coord sub; // intialziing new variable for coordinate

    sub.x = c1.x - c2.x; // X-values for difference between c1 and c2

    sub.y = c1.y - c2.y; // Y-values for difference between c1 and c2

    return sub;

}

// Function #6

double phylib_length( phylib_coord c ) 
{

    // assigning variable to length calculation
    double lengthResult = sqrt(c.x * c.x + c.y * c.y);

    return lengthResult;

}

// Function #7

double phylib_dot_product( phylib_coord a, phylib_coord b ) 
{

    double X = a.x * b.x; // X components

    double Y = a.y * b.y; // Y components

    double dotProd = X + Y; // sum of two components

    return dotProd;
}


// Function #8
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) 
{

    // error check to make sure ball is rolling
    if (obj1->type != PHYLIB_ROLLING_BALL) 
    {
        return -1.0;
    }

    // variables for readability
    phylib_coord pos1 = obj1->obj.rolling_ball.pos;
    phylib_coord pos2 = pos1;

    // handling diff types of objects
    switch (obj2->type) 
    {
        case PHYLIB_ROLLING_BALL:
        case PHYLIB_STILL_BALL:
            // position of ball based off type
            if (obj2->type == PHYLIB_ROLLING_BALL) 
            {
                pos2 = obj2->obj.rolling_ball.pos;  // getting position of rolling 
            } else {
                pos2 = obj2->obj.still_ball.pos;    // getting position of still
            }
            // returning distance between obj1 and the ball minus diameter
            return phylib_length(phylib_sub(pos1, pos2)) - PHYLIB_BALL_DIAMETER;

        case PHYLIB_HOLE:
            // returning distance between minus hole and minus of radius
            return phylib_length(phylib_sub(pos1, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;

        case PHYLIB_HCUSHION:
        case PHYLIB_VCUSHION:
            
            // updating  based on the type of cushion
            if (obj2->type == PHYLIB_VCUSHION) 
            {
                pos2.x = obj2->obj.vcushion.x; // vertical cushion
                pos2.y = pos1.y;
            } else if (obj2->type == PHYLIB_HCUSHION) 
            { 
                 pos2.x = pos1.x;
                pos2.y = obj2->obj.hcushion.y;  // horizontal cushion
            }
            // returning distance 
            return phylib_length(phylib_sub(pos1, pos2)) - PHYLIB_BALL_RADIUS;

        default:
            return -1.0; // if other cases dont match default to this 
    }

}


// / Function #1
void phylib_roll(phylib_object *new, phylib_object *old, double time) 
{
    
    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x) + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * (time * time));
    new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y) + (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * (time * time));

    new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x) + (old->obj.rolling_ball.acc.x * time);
    new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y) + (old->obj.rolling_ball.acc.y * time);

     if (new->obj.rolling_ball.vel.x >= 0 && old->obj.rolling_ball.vel.x <= 0)
     {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
     }

     if (new->obj.rolling_ball.vel.x <= 0 && old->obj.rolling_ball.vel.x >= 0)
     {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
     }

     if (new->obj.rolling_ball.vel.y >= 0 && old->obj.rolling_ball.vel.y <= 0)
     {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
     }

     if (new->obj.rolling_ball.vel.y <= 0 && old->obj.rolling_ball.vel.y >= 0)
     {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
     }

 }


unsigned char phylib_stopped(phylib_object *object){
    
    if (object == NULL) {
        return 0; // Return 0 to indicate failure due to invalid input
    }

    // Retrieve the velocity of the rolling ball from the object
    phylib_coord velocity = object->obj.rolling_ball.vel;

    // Check if the ball has effectively stopped by comparing the velocity's magnitude to a threshold
    if (phylib_length(velocity) < PHYLIB_VEL_EPSILON) {
        // Ball is considered to have stopped, proceed with updating its state

        // Save the current position of the rolling ball
        phylib_coord currentPosition = object->obj.rolling_ball.pos;

        // Update the object's type to indicate it is now a still ball
        object->type = PHYLIB_STILL_BALL;

        // Transfer the saved position and the unique identifier (number) from the rolling state to the still state
        object->obj.still_ball.pos = currentPosition;
        object->obj.still_ball.number = object->obj.rolling_ball.number;

        return 1; // Return 1 to indicate updated to a still state
    }

    
    return 0;
}
    
    




// Function #3
void phylib_bounce(phylib_object **a, phylib_object **b) 
{
   
    phylib_object *pointA = *a; // variable for readability
    phylib_object *pointB = *b; // variable for readabiliy 

    // Going through all bounce cases 
    switch (pointB->type) 
    {
        case PHYLIB_HCUSHION:
            pointA->obj.rolling_ball.vel.y *= -1; // if it bounces of cushion ball travels in opposite direction
            pointA->obj.rolling_ball.acc.y *= -1;
            break;

        case PHYLIB_VCUSHION:
            pointA->obj.rolling_ball.vel.x *= -1; // ball travels in opposite direction if cushion
            pointA->obj.rolling_ball.acc.x *= -1;
            break;

        case PHYLIB_HOLE: // ball falls off the table so free memory and set it NULL
            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL: // upgrading still ball to rolling
        case PHYLIB_ROLLING_BALL:
            if (pointB->type == PHYLIB_STILL_BALL) 
            {
                pointB->type = PHYLIB_ROLLING_BALL;
                pointB->obj.rolling_ball.number = pointB->obj.still_ball.number;
                pointB->obj.rolling_ball.pos = pointB->obj.still_ball.pos;
                pointB->obj.rolling_ball.vel.x = 0;
                pointB->obj.rolling_ball.vel.y = 0;
                pointB->obj.rolling_ball.acc.x = 0;
                pointB->obj.rolling_ball.acc.y = 0;
            }
            // logic for collison rolling balls
            phylib_coord r_ab = phylib_sub(pointA->obj.rolling_ball.pos, pointB->obj.rolling_ball.pos); // posiiton of a with respect to b
            phylib_coord v_rel = phylib_sub(pointA->obj.rolling_ball.vel, pointB->obj.rolling_ball.vel); //computing relative velo
            phylib_coord n = { r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab) }; // normal vector
            double v_rel_n = phylib_dot_product(v_rel, n); // ratio of relative velo
            pointA->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            pointA->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            pointB->obj.rolling_ball.vel.x += v_rel_n * n.x;
            pointB->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // Update acceleration based on new velos
            double aLength = phylib_length(pointA->obj.rolling_ball.vel);
            double bLength = phylib_length(pointB->obj.rolling_ball.vel);
            if (aLength > PHYLIB_VEL_EPSILON) 
            {
                pointA->obj.rolling_ball.acc.x = -pointA->obj.rolling_ball.vel.x / aLength * PHYLIB_DRAG;
                pointA->obj.rolling_ball.acc.y = -pointA->obj.rolling_ball.vel.y / aLength * PHYLIB_DRAG;
            }
            if (bLength > PHYLIB_VEL_EPSILON) 
            {
                pointB->obj.rolling_ball.acc.x = -pointB->obj.rolling_ball.vel.x / bLength * PHYLIB_DRAG;
                pointB->obj.rolling_ball.acc.y = -pointB->obj.rolling_ball.vel.y / bLength * PHYLIB_DRAG;
            }
            break;

        default:
            // Handle any other cases or do nothing if there are no other cases
            break;
    }
}


// function #4
unsigned char phylib_rolling( phylib_table *t )
{

    if (t == NULL) // error check 
    {
        return 0;
    }

    unsigned char rollCount = 0; // counter variable

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        if (t->object[i] != NULL)
        {
            if(t->object[i]->type == PHYLIB_ROLLING_BALL) // if not NULL and rolling ball, increment counter
            {
                rollCount++;
            }
        }
        
    }
    return rollCount;
}






// function 5
phylib_table *phylib_segment(phylib_table *table) {
  
  double currtime = PHYLIB_SIM_RATE;
  
  // error handling
  if ( phylib_rolling(table) == 0)
  {
    return NULL;
  }
  //copy a new table
  phylib_table *copy_table = phylib_copy_table(table);

  // if it fails return NULL
  if (!copy_table) 
  {
    return NULL;
  }


  // loop since objs all start at same time
  while(PHYLIB_MAX_TIME > currtime)
  {
    
    // iteriating over max objs
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
      
      // checking if object is rolling ball
      if(copy_table->object[i] && copy_table->object[i]->type == PHYLIB_ROLLING_BALL)
      {
        
        // update the state of it if condition met
        phylib_roll(copy_table->object[i], table->object[i], currtime);
      }
    }
   
    // another loop to check if rolling ball stops
    for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
    {
      if(copy_table->object[j] && copy_table->object[j]->type == PHYLIB_ROLLING_BALL)
      {
      
        if (phylib_stopped(copy_table->object[j]) == 1)
        {
          copy_table->time = copy_table->time + currtime;
          return copy_table;
        }
        
        // checking for collisions with other objects
        for(int k = 0; k < PHYLIB_MAX_OBJECTS; k++)
        {
          
          if(copy_table->object[k]  && j != k && (0.0 > phylib_distance(copy_table->object[j], copy_table->object[k]))) 
          {
       
            phylib_bounce(&copy_table->object[j], &copy_table->object[k]);
            copy_table->time = copy_table->time + currtime;
            return copy_table;
          }
        }
      }
    }
    // increasing by the sim rate
    currtime = currtime + PHYLIB_SIM_RATE;
  }

  // updating time to max time and returning final result
copy_table->time = copy_table->time + currtime;
  return copy_table;
}





char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }

switch (object->type)
{
    case PHYLIB_STILL_BALL:
     snprintf( string, 80,
              "STILL_BALL (%d,%6.1lf,%6.1lf)",
               object->obj.still_ball.number,
               object->obj.still_ball.pos.x,
               object->obj.still_ball.pos.y );
     break;

    case PHYLIB_ROLLING_BALL:
      snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
      break;


    case PHYLIB_HOLE:
      snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
      break;
    
    case PHYLIB_HCUSHION:
      snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
      break;

    case PHYLIB_VCUSHION:
      snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
      break;
}
return string;
}























