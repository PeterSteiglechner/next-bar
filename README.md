# next-bar

Code deployed at 

https://www.pythonanywhere.com/user/petersteiglechner/files/home/petersteiglechner/mysite/

Website available at: http://petersteiglechner.pythonanywhere.com/

## Description

The tool is designed to suggest a bar/café from a pre-defined set taking the users' preferences into account, but maintaining some degree of stochasticity to foster exploration.  

The $N$ users rate all pre-selected $n$ bars. Ratings $r_i$ of a user $i$ are hard-coded and range from $1$ (least favourite bar) to $n$ (favourite bar). The probability that a bar $x$ is chosen is

$$ p(x) = 1/R \cdot \sum_{i} \, r_i(x) $$

where $R$ is the normalisation $\sum_{i} \, r_i(x)$.


## Issues and plans

### UI/Backend: Flexible users 
- create a "User" and store their rating.
- enable user selection and load their stored ratings.

### UI: Rating input
- make ratings adjustable

### UI: Bar selection/exclusion
- create a tickbox behind each bar/café to enable manual selection or exclusion of certain bars/cafés.

### UI: Bar-set selection
- enable to switch between "cafés" and "bars" with a simple click.
- enable to switch between "cafés" and "bars" with a simple click. 

### Backend: 0-10 rating 
- Instead of ranking the bars from 1 to n, one could give scores from 0 to 10. 

### Backend: "no rating"
- enable the possibility to assign no rating to a bar $r_i = NA$. The probability needs to be adjusted somehow.

### Backend: Decision-function
- slider from "secure choice" to "experimental choice" --> parameter $f$ in the range from 0 to a large value.

The new decision function is: 

  $$ p(x) = 1/R \cdot \sum_{i} \, r_i(x)^{f} $$

For $f=0$, all bars are equally likely. For $f=1$, the average rating determines the probability. For $f=\infty$, the overall best-rated bar is chosen.

- Alternative: slider "min rating" from 1 to n --> parameter $r_{min}$. All bars with any rating $r_i < r_{min}$ are excluded (and the normalisation is adjusted accordingly).


