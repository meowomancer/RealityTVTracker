RealityTVTracker
================

About
-----
RealityTVTracker is a web based information system written in Perl used to organize, sort, display, and store information related to reality TV. This system was originally designed to assist a University of Oregon PhD candidate with organizing, sorting, and displaying information for her PhD dissertation. 

Limitations
-----------
This project was developed as a five-week project for a software development methodologies course and thus has a number of limitations including:

* Lack of proper installer, manual installation is required
* No automatic module installation. While RealityTVTracker was built to be modular created modules must be integrated into the code manually. This can be done by editing the source of index.cgi
* No template system. All HTML is embedded within the source code. 

Installation
------------
To install RealityTVTracker place the files in a directory that is CGI enabled by your http service of choice. 

Next, in a directory outside of your www-files path, create a file called db_config.cgi and put the following data as well as correct values into it.

    $db_user = "";                                                                                                                                                                                          
    $db_password = "";
    $db_host = "";
    $db_database = "";

Next, update line 53 of index.cgi to point toward the correct file and line 59 to the proper FQDN of RealityTVTracker.

Finally, use db_setup.sql to create the required database structure.

Credits
-------
* Gabe Aron: Developer (graphing), Tester
* Mack Hagen: Designer, Tester
* Cory Olivieri: Requirements Analyst, Architect
* Zachary Yamada: Project Manager, Lead Developer
* Adam Zucker: Architect, Designer

Other
-------
RealityTVTracker uses Bootstrap by Twitter which is released under the MIT license