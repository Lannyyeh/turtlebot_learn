## turtlebot_learn
### This is a backup and record for self-using, for the homework in 3th grade, in project-4e of Automation of SJTU. 

1.  To open the world use 
```sh
roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=/home/lanny/turtlebot_ws/src/turtlebot_custom_gazebo_worlds/world12.world
```
2. To open the map that already scanned for the world use
```sh
roslaunch turtlebot_gazebo amcl_demo.launch map_file:=/home/lanny/turtlebot_ws/src/turtlebot_learn/maps/C1.yaml
```
3. To launch Rviz
```sh
roslaunch turtlebot_rviz_launchers view_navigation.launch
```
4. To start the misson of homework3 use
```sh
python go_to_specific_point_on_map.py
