#!/usr/bin/perl

=begin comment
index.cgi

THIS IS THE DRIVER FOR THE REST OF THE APPLICATION AND THUS THIS FILE IS
HEAVILY COMMENTED. PLEASE REFER TO THE ACTUAL FILE FOR FURTHER INFORMATION
REGARDING INDIVIDUAL MODULE ACTIONS.

INDEX.CGI IS RESPONSIBLE FOR:
		| --Connecting to the database
		| --Triggering debug mode
		| --Creating global variables and objects
		| --Loading Modules
		| --Routing pages
		| --Defining custom CSS
		| --Defining website URL

=end
=cut


#This causes error messages to be printed in the web browser as opposed to a log
#file. This saves a ton of time overall
use CGI::Carp qw/fatalsToBrowser/;

#Should use these for neat coding. They ensure that a mistake isn't made when in
#terms of improper scoping, accidental casting, etc.
use warnings;
use strict;

#Debug bit -- make sure this is "0" before put into a production environment. If
#you ever want to make something show up only when this is set to 1, then you
#just need to wrap your code in "if($DEBUG){[code]}
my $DEBUG = 0;

#Modules
use CGI;						#http://perldoc.perl.org/CGI.html
use DBI;						#http://dbi.perl.org/
use CGI::Session;				#http://search.cpan.org/~markstos/CGI-Session-4.48/
use Digest::SHA qw(sha384_hex);	#http://search.cpan.org/~mshelor/Digest-SHA-5.85/lib/Digest/SHA.pm

#Initialization of variable for CGI as well as the creation of the objects
our($CGI, $session);
$CGI = new CGI;
$session = new CGI::Session();

#Session Management
our $CGISESSID = $session->id();

#DB Connection
our($db_user, $db_password, $db_host, $db_database);
do("");
our $dbString = "DBI:mysql:" . $db_database . ":" . $db_host;
our $db = DBI->connect($dbString, $db_user, $db_password, {'RaiseError' => 1});
our $db_query;

#Website URL -- FQA of index.cgi
our $url = qq();

#Custom CSS
our $CSS = qq(
	td,tr,th{padding:10px;}
);

#Page routing
my $s;

#Check paramaters to see if a source is defined
if(defined($CGI->param('s'))){
	$s = $CGI->param('s');
}else{
	$s = 'm'
}
our @temp;
our @genres;
$db_query = $db->prepare("SELECT DISTINCT genre FROM show_data WHERE genre <> '' UNION SELECT DISTINCT secondary_genre FROM  show_data WHERE secondary_genre <> ''");
$db_query->execute();
while(@temp = $db_query->fetchrow_array){
	push(@genres, $temp[0]);
}

our @networks;
$db_query = $db->prepare("SELECT DISTINCT network FROM show_data WHERE network<>'' UNION SELECT DISTINCT secondary_network FROM show_data WHERE secondary_network<>''");
$db_query->execute();
@networks = $db_query->fetchrow_array();
while(@temp = $db_query->fetchrow_array){
	push(@networks, $temp[0]);
}

do "layout.cgi";	#Header and footer code
do "helpers.cgi";	#Helper method
do "addData.cgi";	#Adding of existing entries
do "edit.cgi";		#Editing of existing entries
do "search.cgi";	#Search and display functionality
do "flag.cgi";
do "admin.cgi";
do "pages.cgi";
do "user.cgi";		#User management
do "manageColumns.cgi";
do "propose.cgi";
do "graph.cgi";
do "credits.cgi";

#---#---#BEGIN ELSEIF BLOCK#---#---#
#SYSTEM MODULE: layout.cgi (prints header)
start();

#SYSTEM MODULE: index.cgi
if      ($s eq 'm' )    		{ main(); }

#PUBLIC MODULE: search.cgi
elsif 	($s eq 'search') 		{ search(); }

#PUBLIC MODULE: flag.cgi
elsif 	($s eq 'flag')			{ flag(); }

#PUBLIC MODULE: pages.cgi
elsif 	($s eq 'showPage')		{ showPage(); }

#PUBLIC MODULE: propose.cgi
elsif	($s eq 'proposeData')		{ proposeData(); }
elsif	($s eq 'proposeShow')		{ proposeShow(); }

#PUBLIC MODULE: graph.cgi
elsif	($s eq 'graph')			{ graph(); }

#PUBLIC MODULE: user.cgi
elsif   ($s eq 'l')     		{ login();  }
elsif   ($s eq 'r')     		{ register();  }
elsif   ($s eq 'lo')    		{ logout();  }
elsif	($s eq 'f')				{ forgotPassword();}
elsif	($s eq 'reset')			{ resetPassword();}
elsif	($s eq 'cpw')			{ changePassword();}

#PUBLIC MODULE: credits.cgi
elsif	($s eq 'credits')		{ credits(); }

#ADMIN MODULE: admin.cgi
elsif	($s eq 'admin')			{ admin(); }
elsif	($s eq "adminQueue")	{ adminQueue(); }
elsif	($s eq "dismiss")		{ dismiss(); }
elsif	($s eq "accept")		{ acceptChange(); }
elsif       ($s eq "acceptShow")    {acceptShow();}

#ADMIN MODULE: addData.cgi
elsif   ($s eq 'addData')		{ addData(); }

#ADMIN MODULE: edit.cgi
elsif	($s eq 'edit')			{ edit(); }

#ADMIN MODULE: pages.cgi
elsif	($s eq "newPage")		{ newPage(); }
elsif	($s eq "editPage")		{ editPage(); }
elsif	($s eq "managePages") 	{ managePages(); }

#ADMIN MODULE: user.cgi
elsif	($s eq "manageUsers")	{ manageUsers(); }
elsif	($s eq "deleteUser")	{ deleteUser(); }
elsif	($s eq "makeUser")		{ makeUser(); }
elsif	($s eq "makeAdmin")		{ makeAdmin(); }

#ADMIN MODULE: manageColumns.cgi
elsif	($s eq "manageColumns")	{ manageColumns(); }
elsif	($s eq "addColumn")		{ addColumn(); }
elsif	($s eq "deleteColumn")	{ deleteColumn() ;}


#SYSTEM MODULE: layout.cgi (prints footer)
end();
#---#---#END ELSEIF BLOCK#---#---#

sub main{
	
	search();
	
}

exit;

