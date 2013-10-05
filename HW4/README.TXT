-----------------------------------------
Features Used
-----------------------------------------
1)	Image size
2)	Mean of Red channel 
3)	Mean of Green channel 
4)	Mean of Blue channel 
5)	Standard deviation of Red channel 
6)	Standard deviation of Green channel 
7)	Standard deviation of Blue channel 
8)	Mean of  X coordinate of highest intensity gray scale channel
9)	Mean of  Y coordinate of highest intensity gray scale channel
10)	Mean of  X coordinate of minimum intensity gray scale channel
11)	Mean of  Y coordinate of minimum intensity gray scale channel
12)	SD of  X coordinate of highest intensity gray scale channel
13)	SD of  Y coordinate of highest intensity gray scale channel
14)	SD of  X coordinate of minimum intensity gray scale channel
15)	SD of  Y coordinate of minimum intensity gray scale channel
16)	Edge height of image
17)	Edge width of image

-----------------------------------------
Running the code
-----------------------------------------
To run the code follow the steps below:
1) Make sure you have classifier.py and 50_categories folder in the same folder

Note:
2) trained_classifier.p has been shared on google drive. Make sure you download the file correctly and place it in the
same folder where classifier.py and 50_categories folder are placed.

If this does not work, you can recrete the model file simply by running all the ipython 
commands in notebook HW4.ipynb one by one. Make sure in the variable , correct path to 50_categories folder is provided.
MYDIRECTORY ="/Users/sonali/Documents/Ischool/PythonSeminar/pythonseminar/HW4/50_categories"

3) Now open python on Terminal and call the function as shown below:
e.g.
$ python
>>> import classifier
>>> classifier.run_final_classifier("/Users/sonali/Documents/Ischool/PythonSeminar/pythonseminar/HW4/50_categories/airplanes","trained_classifier.p")

4) Make sure the path provided to the function run_final_classifier is the absolue path till the folder that contains the files

-----------------------------------------
Accuracy
-----------------------------------------
Running cross validation score using 20 fold cross validation, I got a mean accuracy score of approx 29%
mean: 0.292187, stdev: 0.029380