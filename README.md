# sma_if_twoturtle
Ce package contient le package de la première partie du projet SMA.
Il permet d'implémenter un système de Leader-Follower en simulant deux turtlebot3 sur Gazebo.

## Installation
Pour installer ce noeud il faut le cloner dans le dossier src de votre catkin workspace (catkin_ws).

```
cd catkin_ws/src
git clone https://github.com/IF488/sma_if_twoturtle.git
cd ..
catkin_make
source devel/setup.bash
```

## Execution
Dans un premier terminal, lancer la simulation Gazebo:

```
roslaunch sma_if_twoturtle two_in_turtle_world.launch
```

Dans un deuxième terminal, lancer le map_server:

```
rosrun map_server map_server ~/map.yaml
```

Dans un troisième terminal, lancer AMCL pour le premier robot:

```
roslaunch sma_if_twoturtle amcl_tb0.launch
```

Dans un quatrième terminal, lancer AMCL pour le deuxième robot:

```
roslaunch sma_if_twoturtle amcl_tb1.launch
```

Dans un autre terminal lancer les commandes suivantes:

```
rosservice call /tb3_0/request_nomotion_update 
rosservice call /tb3_1/request_nomotion_update
```

Optionnellement, lancer RViz pour verifier que tous fonctionne:

```
roslaunch sma_if_twoturtle multi_rviz.launch
```

Si tous fonctionne correctement, vous pouvez lancer le noeud leader_follower.py dans un autre terminal:

```
rosrun sma_if_twoturtle leader_follower.py
```

Finalement, téléopérer le robot leader avec:

```
ROS_NAMESPACE=tb3_0 rosrun turtlebot3_teleop turtlebot3_teleop_key
```
