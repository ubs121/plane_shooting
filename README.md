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

The agent's goal is to find the plane head with minimum possible shots.  So how many shots are required to destroy any plane? I couldn't tell exact number, but I have some reasonable metrics.

In worst case the agent could find the head with 100 shots, which means it has to hit every square on the grid. But our agent has to be smarter than this.


It's possible to find some part of the plane with 10 shots at maximum. Because the plane occupies 1/10 size of space on the board. Only thing is to keep correct amount of gap between shots to cover all area.

Once the agent hit on the body of the plane it should be easy to guess the head. Usually 2-4 shots needed to find the head after body shot. So in total, 14 shots should be enough to destroy any plane.




## II. Analysis

### Data Exploration

There is no existing dataset for this problem. There is some input, a hint.

In order to minimize shots, a hint of next possible head locations is given to the agent. The agent must learn from this hint, and learn to select the best guess for head shot.

The agent could use all random guess tactic. But it will not succeed, even it may be worse than the simple 100 shots.

As I know, there are some well known tactics for the best guess. I didn't explore all best tactics, but here is shown two sample of them.

** Sample 1: A body shot **

For example, if got a body shot ('B') on location (4,5), then after this shot the hint will look like the following. There are 32 possible head location after the body shot at (4,5).

  ![shot B](shot_B.png)

Furthermore from this visualization of head distribution, we could see that intersected squares (with tick borders) are the most efficient shots. Specially the square (3,4), (5,4), (3,6) and (5,6) are the most efficient locations to try. By shooting at these squares the agent will be rewarded anyway as one of the following:

* Could win the game by just hitting a head, because these four locations are possible head locations.

* Could be a body shot, for example at (3,4). If so the next possible head locations will be 3 times less at least.

  ![shot BB](shot_BB.png)

* Could be a miss. Even in this case the agent will get benefit, because the next possible head locations will be reduced by 6.

  ![shot BM](shot_BM.png)

** Sample 2: A missed shot **

If the agent missed at (2,2), then it still has to learn something from this shot, because this shot will reduce the next possible heads. In the below figure, white squares are non-head coordinates after this missed shot, so the agent will ignore this locations for the next shot.

![shot M](shot_M.png)


### Algorithms and Techniques

This problem could be solved by using the Reinforcement Learning (RL) approach.

The idea is to reward every efficient shot of the agent. How efficient is measured by the reduction of possible head locations after every shot.

Also could be some punishment, for example we could punish the agent if it shot at same location repeatedly.

So the tactic is to explore the grid and shrink the unknown area as much as possible while seeking the plane head.

With this idea and enough number of training, I think the agent could 'learn' how to shoot efficiently.

** Parameters for RL **

Here is the main parameters for RL:

* *States*: If we count every square of the grid, there are 3^100 states for this game. 3 is the number of shot marks, these are 'B', 'M' and empty square, 100 is the number of squares. This is a huge number and takes tremendous amount of time to train the agent. Anyway we will use the grid with the shot marks as a state, because it represents the current state the best.

* *Actions*: There are 100 actions, each for every square coordinates. Luckily we will use hints to limit the number of actions. So it will be fewer and fewer 'state-action' combinations for each shot.

* *Reward*: If the agent hit the head of plane, then we will reward it by 100 points. In other cases, the reward will be the reduction size of possible head locations. It won't exceed than 100, that is why the maximum reward is 100.

 General reward formula is:

  ```
  reward = len(hint_old) - len(hint_new)
  ```

  For example, in case of the `Sample 1` of the section 'Data Exploration', by shooting at `(3,4)`, the agent will be rewarded by score 22, because before the shot the length of hint was 32, after the shot it become 10, so 32 - 10 = 22. So the shot was efficient that much in that particular state.

* *Punishment*: The agent should avoid repeated shots at same location. It's extremely useless and stupid action, so we could punish the agent by -1000 (almost never do it again). Also we could punish the agent if it shot at another location than suggested hint.

* *Alpha*: alpha 0.1 is suggested value for a stochastic problem

* *Gamma*: It could be 2.0. So the agent will focus on current rewards. I think current reward policy is efficient enough to guide the agent into correct choice.

* *Epsilon*: Since this is a stochastic type of problem, I set the epsilon to 0.5. So the agent is allowed to make a random shot with 50% probability. In other 50% it will use it's past experience.


### Benchmark

Гүйцэтгэлийг хэмжихийн тулд дундаж буудсан тоо, буудалтын тархалтын статистик гэсэн үзүүлэлтүүдийг сонгож авсан.

Дундаж буудалтыг нийт буудалтын тоог тоглолтын тоонд хувааж гаргасан. Тоглолт нь онгоцны тухайлсан нэг байрлал дээр яригдана.

```
  Average shot = totals shots / the number of play
```

From my experience, it is possible to find the head of plane with 6-10 shots at maximum. Энэ дундаж үзүүлэлтийг мөн баримжаа болгож үзэх хэрэгтэй. Ө.х `Average shot` нь ойролцоогоор 10 байхад хэвийн.




## III. Methodology

### Data Preprocessing

There is no data pre-processing is required for this problem.

But after the problem is solved we could use the trained dataset for a real game (against real human). Also the agent could improve that learnt data over time.

### Implementation

The solution code consists 3 sections of code: environment, agent and simulation.


** The environment **

Implementing the environment was the most important part of the problem. The environment contains a grid and plane.

new_game - нь тоглоомыг эхлүүлнэ. Үүнд grid-г цэвэрлэх, онгоцыг байршуулах г.м бэлтгэл кодууд багтана.

shoot() - нь өгөгдсөн буудалтыг шалгаад тохирох шагналыг өгнө.

get_hints() - нь буудалтын дараах  hint мэдээллийг өгнө.

Эдгээрээс гадна зарим туслах функцүүд бий.

random_plane() - нь санамсаргүй байрлалтай онгоц үүсгэнэ.
valid() - нь өгөгдсөн байрлал зөв эсэхийг шалгана
show() - нь орчныг дэлгэц дээр дүрсэлж харуулна


** The agent **

Энэ класс нь бидний гол суралцагч agent юм. RL аргачлалын дагуу state шинэчилэх, дараагийн action санал болгох, үр дүнгээсээ суралцах гэсэн үндсэн чадвартай байгаа.

** The simulator **

Орчин болон agent бэлэн болсон цагт бидэнд agent-г шалгах тоглогч хэрэгтэй. Бодит хүнтэй тоглож шалгаж болох боловч их цаг хугацаа орсон залхуутай ажил болно. Тийм учраас хүн тоглогчийг орлуулсан simulator хийсэн.

Энэ simulator нь онгоцны нийт 168 боломжит байрлал дээр agent-тай тоглолт хийнэ. Нэг байрлал дээр 100 удаа тоглолт хийж agent-г шалгана, бас давхар сургана. 168*100 удаа давтагдах учраас бага зэрэг удаан ажиллана.


### Refinement

hint-н дагуу цэвэр санамсаргүй буудах аргаар явж болох байсан. Гэвч энэ нь тавьсан зорилгод ерөөсөө хүрэхгүй гэдэг нь нотлогдсон. Тиймээс agent суралцах хэрэгтэй байсан.

Сургахын тулд хамгийн гол хэсэг нь environment, тэр дотроо reward policy-г яаж тодорхойлох вэ гэдэг нь хамгийн чухал байлаа.

Agent-г гүйцэтгэлийг оновчлохын тулд RL параметрүүдийг янз бүрээр турших хэрэгтэй, мөн reward policy-г өөр хувилбараар турших хэрэгтэй.

Эхлээд body шот хийсэн бол 10 оноо, miss болсон бол -1 оноо өгөх байдлаар reward policy-г тодорхойлж байсан юм. Гэвч энэ reward policy-р agent-н гүйцэтгэл олигтой сайн гарахгүй байсан.



Some lucky human players could find the head with 5-6 shots. Anyway the agent must learn optimal technique, and be able to compete with a human player.


The following picture shows how the agent sees the plane layout after 100 trails. From this visualization we could see dark blue parts are head and body squares, and lighter parts are less or non-related squares with the plane.

**Sample 1:**

A plane that South headed at (7, 7):

![viz1](viz1.png)

**Sample 2:**

A plane that East headed at (8, 7):

![viz2](viz2.png)



simulator-с ажиглах ёстой гол зүйлс нь дундаж буудалтын тоо болон буудалтын статистик visualization байгаа. Энэ visualization нь тухайн layout-г agent баримжаагаар тодорхойлж чадсан эсэхийг харуулах зорилготой юм.

Захын цэгүүдээр тархалт муутай, гол руугаа өндөр болж харагдаж байгаа.
Энэ нь өнгөний уусалтаар тодорхой харагдаж байна.

## IV. Results


Agent-г онгоцны нийт боломжит 168 байрлал дээр туршиж үзсэн. Дунджаар 8-11 буудалтын дараа онгоцны толгойг олж байсан.

Дундаж буудалт нь 8.1 болсон.


Хамгийн төгс agent бол бүх 3^100 state-с бүх 100 action-г хийж үзээд хамгийн оновчтойг нь сонгож сурсан байх хэрэгтэй болно. Үүнийг хийхэд их хэмжээний computing power шаардлагатай болох учраас одоогоор түр орхисон.


## V. Conclusion

This is a simple guessing game. But the most important question was could the agent learn well enough to compete against a experienced human player.

I wanted to see if the agent could find the best tactics.

The agent could learn and play like experienced human by 'practicing' every possible layouts of the plane.


RL шийдлээр шийдэхэд state болон action тоо маш их байсан учраас сургахад  маш их хугацаа шаардлагатай сул талтай байсан. Үүнийг шийдэх нэг хувилбар нь hint ашиглах юм. Эцсийн зорилго бол жинхэнэ хүн тоглогчтой өрсөлдөх хэмжээний agent бий болгох учраас hint ашиглах нь болохгүй зүйлгүй.

Эцэст нь agent боломжийн хэмжээнд сурсан гэж үзэж байна. Дунджаар 8-11 буудалтаар онгоцны толгойн байрлалыг олж чадаж байгаа.



### Improvement

Энэ шийдлийг цааш нь сайжруулах боломж бий.
