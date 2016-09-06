# Capstone Project - Plane shooting

## Machine Learning Engineer Nanodegree

Uuganbayar Sukhbaatar  
August 29th, 2016

## I. Definition

### Project Overview

This is a pencil and paper game similar to the [Battleship game](https://en.wikipedia.org/wiki/Battleship_game). We used to play this game during school days.

The game is played by 2 players on four grids, two for each player. The grids are 10×10 square – and the individual squares in the grid are identified by row and column number. On one grid the player arranges ships and records the shots by the opponent. On the other grid the player records their own shots.

Before play begins, each player secretly arranges their planes on their primary grid, usually 2-3 planes. Each plane occupies a number of consecutive squares on the grid, arranged either horizontally or vertically.

One player tells the coordinates for shot, and the other give a feedback whether the player has hit or missed the plane. The best shooter who shot all planes of the opponent will win the game.


### Problem Statement

Human player secretly arranges a plane with the following figure on a grid with size of 10x10, let's say it an environment. You have to develop an agent that is capable to learn how to shoot the plane in this environment.

![](plane1.png)

The human player gives a feedback with letter `H` for head shot, `B` for body shot and `M` for miss (see the figure above).

Using this feedback the agent have to find the head of the plane with minimum possible shots.

### Metrics

The agent's goal is to find the head of the plane with minimum possible shots.

It's possible to find the plane (some part of the plane) with 10 shots at maximum, if the agent has some intelligence. Because the plane occupies 1/10 space on the board.

In worst case the agent could find the head with 100 shots, which means it has to hit every square on the grid.

Once hit on the body of the plane it should be easy to guess the head, usually 2-4 shots needed after body shot. So in total, 14 shots should be enough to find the head. Some lucky human players find the head with 5-6 shots usually. The agent must learn this technique, and be able to compete with a human player.


## II. Analysis

### Data Exploration

There is no existing dataset for this problem.

The simplest agent could find the head with 100 shots, just by hitting each square of the grid.

In order to minimize shots, a hint of next possible head locations is given to the agent. The agent must learn from this hint, and learn to select the best guess for head shot.

The agent could learn and play like experienced human by 'practicing' every possible layouts of the plane.

** Sample 1: Hint after body shot **

For example, if got a body shot ('B') on location (4,5), then after this shot the hint will look like the following. There are 32 possible head location after the body shot at (4,5).

![shot B](shot_B.png)

Furthermore from this hint visualization, we could see that intersected squares are the most efficient shots. Specially the square (3,4), (5,4), (3,6) and (5,6) are the most efficient locations. By shooting at one of these locations the agent will be rewarded anyway:

* Could win the game by just hitting a head, because these four locations are head locations.

* Could be a body shot, for example at (3,4). If so the next possible head locations will be less at least 3 times.

  ![shot BB](shot_BB.png)

* Could be miss. Even in this case the next possible head locations will be reduced a little.

** Sample 2: Hint after missed shot **

If the agent shot at (2,2) and missed, then it still has to learn something from this shot, because this shot will reduce the next possible heads.

![shot M](shot_M.png)

### Algorithms and Techniques

This problem could be solved by using the Reinforcement Learning approach.

The idea is to reward every efficient shot of the agent. How efficient is measured by reduction of possible head locations after every shot. Also could be some punishment, for example we could punish the agent if it shot at same location repeatedly.

With this idea and enough number of training, I think the agent could 'learn' how to shoot efficiently.

Here is parameters for RL:

* *States*: If we count every square of the grid, there are 3^100 states for this game. 3 is for 'B', 'M' and empty square. This is a huge number and takes tremendous amount of time to train the agent. Luckily we will use hints. Anyway we will use the current shot marks on the grid as a state, because it represents the current state the best.

* *Actions*: There are 100 actions for every square coordinates. Again we will use hints. So it will reduce the 'state-action' combinations a lot.

* *Reward*:


Alpha утгыг 1.0 сонгоно.

Gamma утгыг 2.0 гэж сонгож болно. Хамгийн цөөн хувилбар үлдээхийг зорих хэрэгтэй. Reward нь мөн энэ зарчим дээр үндэслэсэн байгаа, тиймээс тухай тухайн шагнал хамгийн чухал байна.

- _Are the algorithms you will use, including any default variables/parameters in the project clearly defined?_

- _Are the techniques to be used thoroughly discussed and justified?_

- _Is it made clear how the input data or datasets will be handled by the algorithms and techniques chosen?_

### Benchmark

In this section, you will need to provide a clearly defined benchmark result or threshold for comparing across performances obtained by your solution. The reasoning behind the benchmark (in the case where it is not an established result) should be discussed. Questions to ask yourself when writing this section:
- _Has some result or value been provided that acts as a benchmark for measuring performance?_
- _Is it clear how this result or value was obtained (whether by data or by hypothesis)?_


## III. Methodology

### Data Preprocessing

Өгөгдөл урьдчилан боловсруулах шаардлага байхгүй.

But after the problem is solved we could use the trained dataset for a real game (with real human). Дараа нь энэ training өгөгдөлөө файлд хадгалаад, цааш нь нэмж суралцаад байж болно.

### Implementation

The solution code consists 3 code sections: environment, agent and simulation.





### Refinement

In this section, you will need to discuss the process of improvement you made upon the algorithms and techniques you used in your implementation. For example, adjusting parameters for certain models to acquire improved solutions would fall under the refinement category. Your initial and final solutions should be reported, as well as any significant intermediate results as necessary. Questions to ask yourself when writing this section:
- _Has an initial solution been found and clearly reported?_
- _Is the process of improvement clearly documented, such as what techniques were used?_
- _Are intermediate and final solutions clearly reported as the process is improved?_


## IV. Results

### Model Evaluation and Validation

In this section, the final model and any supporting qualities should be evaluated in detail. It should be clear how the final model was derived and why this model was chosen. In addition, some type of analysis should be used to validate the robustness of this model and its solution, such as manipulating the input data or environment to see how the model’s solution is affected (this is called sensitivity analysis). Questions to ask yourself when writing this section:

- _Is the final model reasonable and aligning with solution expectations? Are the final parameters of the model appropriate?_

- _Has the final model been tested with various inputs to evaluate whether the model generalizes well to unseen data?_

- _Is the model robust enough for the problem? Do small perturbations (changes) in training data or the input space greatly affect the results?_

- _Can results found from the model be trusted?_

### Justification

In this section, your model’s final solution and its results should be compared to the benchmark you established earlier in the project using some type of statistical analysis. You should also justify whether these results and the solution are significant enough to have solved the problem posed in the project. Questions to ask yourself when writing this section:
- _Are the final results found stronger than the benchmark result reported earlier?_
- _Have you thoroughly analyzed and discussed the final solution?_
- _Is the final solution significant enough to have solved the problem?_


## V. Conclusion
_(approx. 1-2 pages)_

### Free-Form Visualization

The following picture shows how the agent sees the plane layout after 100 trails. From this visualization we could see dark blue parts are head and body squares, and lighter parts are less or non-related squares with the plane.

**Sample 1:**

A plane that South headed on location (7, 7):

![viz1](viz1.png)

**Sample 2:**

A plane that East headed on location (8, 7):

![viz2](viz2.png)



TODO: Захын цэгүүдээр магадлал муутай, гол руугаа өндөр болж харагдах ёстой.
Мөн аль нэг байрлал дээр шарх олсон бол өнгөний уусалтаар маш тодорхой харагдах ёстой.


### Reflection

This is a simple guessing game. But the most important question was could the agent learn well enough to compete against a experienced human player.

RL шийдлээр шийдэхэд state болон action тоо маш их байсан учраас сургах хугацаа маш их шаардлагатай байсан нь гол асуудал байсан. Үүнийг шийдэх нэг хувилбар нь hint ашиглах юм. Эцсийн зорилго бол жинхэнэ хүн тоглогчтой өрсөлдөх хэмжээний agent бий болгох учраас hint ашиглах нь болохгүй зүйлгүй.

Эцэст нь agent боломжийн хэмжээнд сурсан гэж үзэж байна. Дунджаар 8-12 буудалтаар онгоцны толгойн байрлалыг олж чадаж байгаа.


### Improvement
