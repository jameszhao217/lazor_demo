# LAZOR Group Project
### CHEME 5500 Software Carpentry
### Instructor: Henry Herbol
### 2018/04/13



```markdown
## Group Members:
Moran, Terrence: tpm92@cornell.edu
Zhao, Mingjie: mz467@cornell.edu
Zhong, Ren: rz346@cornell.edu
```



## Brief Description
Our code automatically find solutions to the "Lazor" game on androids and iphones. 
It reads in an input file to obtain the board layout to obtain the number and types of blocks, the number of points that needs to go through, and the position and direction of the laser beam. Then, it generates all the potential variations of placing blocks onto this board, uses laser to test each one of the variations, finds one board that satisfies all the points, and then save that solution into a text file. 

Our code consists of the following objects:
1. _Game_ Object
2. _Block_ Object
3. _Point_ Object
4. _Laser_ Object



### Installation
One may access and use our code by forking this directory.





### How-to
In the repository, you may find the _solve.py_ file that contains the main call to the Lazor code. 
To solve a designated board, simply change the name of the input file inside _solve()_ at the last line of _solve.py_. 
The program will automatically prints a board solution onto screen, as well as generating a text file named _solution.txt_. 





Please contact us by the listed emails if you have any questions.

Thank you very much! 
