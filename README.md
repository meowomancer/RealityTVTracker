RealityTVTracker
================

About
-----
RealityTVTracker is a series of CGI perl scripts used to organize, sort, display, and store information related to reality TV. 

Originally designed to assist a University of Oregon PhD canidate with her research. 

Installation
------------
To install RealityTVTracker place the files in a directory that is CGI enabled by your http service of choice. 

Next, in a directory outside of your www-files path, create a file called db_config.cgi and put the following data as well as correct values into it.

    $db_user = "";                                                                                                                                                                                          
    $db_password = "";
    $db_host = "localhost";
    $db_database = "";

Next, update index.cgi to point toward the correct file.

Finally, use db_setup.sql to create the required database structure.

Credits
-------
* Gabe Aron: Developer (graphing), Tester
* Mack Hagen: Designer, Tester
* Cory Olivieri: Requirements Analyst, Architect
* Zachary Yamada: Project Manager, Lead Developer
* Adam Zucker: Architect, Designer
