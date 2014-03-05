#Gabe Aron 
#This is the Graph-plotting module of the AHOYZ Reality TV Tracker (ARTT). 
#Input: the database table "show_data"
#Output: a .png graph as an output (starting on line 145)
#Any number of genres can be specified in show_data. However, only seven unique colors exist as of now (on line 140)
#Currently, it displays only results for genre. The rest should be implemented fairly shortly.
#I was not able to access the database from my computer because I could not install the module DBD::mysql (although, I am allowed to declare it in for use in the 
#	use *module specification). 
#Values from the table must be entered into a 2-dimensional array: temp[rows][columns]. Once this is done, this program should work (on line 176)
#This program plots a graph based on the contents of a dynamically-allocated series of arrays (one array for each genre). 
#	The graph is written to my desktop, but I assume that it should be written to a URL. Feel free to choose one. (starting on line 145)

#modules so far (and their dependencies):
#   void choice() - line 166 - calls void categories(string[][]) - line 72 -, void networks(string[][]) - line 158 - and void netCat(string[][]) -line 162 -
#   void networks(string[][]) - line 158 - calls void fillArray(string, int, int, int, int) - line 34 -

#Note - to integrate this module, one must:
#   enter the database table "show_data" into the array "temp[][]" (on line 183),
#   designate a specific location for the .png file to be written (on line 153)
#   one may optionally write the file to the current web page


#!/usr/bin/perl
use Fcntl; #for files
use CGI ':standard';
use GD::Graph::lines;
use GD::Graph::colour qw( :files );
use strict;
use DBI;
use DBD::mysql;

#globals
our @genres;		#contains arrays with values to be plotted
our @genNames;		#contains set of unique genres
our $genNumber = 0;
our @networks;		#contains array with values to be plotted
our @netNames;
our $netNumber = 0;
our $size = 30;		#in the future, this will be dynamically allocated


sub fillArray{	#puts values into the appropriate array to be plotted. This array is dynamically allocated as genres are added.
	my $name = $_[0];
	my $i = $_[1];
	my $j = $_[2];
	my $startDate = $_[3];
	my $endDate = $_[4];
	my $flag = $_[5];
	my $address;

	##############################assigns a pointer to the address of the correct genre. This is required for dynamically adding genres
	my $ind;

	if ($flag eq "genre"){
		for ($ind = 0; $ind < $genNumber; $ind++){
			print "Genres:$genNames[$ind]\n";
			if ($genNames[$ind] eq $name)
			{
				$address = \@genres;		
				last;
			}
		}
	}
	elsif ($flag eq "networks"){
		for ($ind = 0; $ind < $netNumber; $ind++){
			print "networks:$netNames[$ind]\n";
			if ($netNames[$ind] eq $name)
			{
				$address = \@networks;		
				last;
			}
		}
	}
	
	#########################################

	###########Fill the plotting arrays of the specified genre
	if ($endDate > $startDate)	#if there's a range (that is, a start year and an end year)
	{
		my $range = $endDate - $startDate;			# range works, don't disgard
		my $k;
		for ($k = $j; $k <= $range + $j; $k++)
		{
			$$address[$ind][$k] = $$address[$ind][$k] + 1;	#dereference pointer and write updates to array
		}
	}
	elsif ($endDate <= $startDate)		#no range (only a start year)
	{
		$$address[$ind][$j] = $$address[$ind][$j] + 1;		#dereference pointer and write updates to array
	}
	############################################################
	
}


sub categories{		#allows graph generation by categories. Finished prototype. Will be able to generate filtered graphs based on specific category.

	my @temp = @_;
	
	my $icount = 0;

	my @time1;			#time plotting array
	$time1[0] = 1973;		#fill in the initial time
	
	#####indexing variables				
	my $i;
	my $j;
	my $k;
	##########
	
	for ($i = 1; $i < 26; $i++){	#fill in time plotting array
		$time1[$i] = 1988 + $i;
	}


	##############main loop for creating genre plotting arrays. Calls fillArray
	$i = 0;
	$j = 0;
	while ($i < 30){	
		if ($j < 27){			#haven't exceeded size of time
			if ($temp[$i][5] >= $time1[0]){
				if ($temp[$i][5] == $time1[$j]){		#time match 
					&fillArray($temp[$i][1], $i, $j, $temp[$i][5], $temp[$i][6], "genre");
					$i++;
				}
				else{	#time is behind temp[5], and must be brough up

					$j++;
				}	
				
			}
			
			else{	#start date not given
				$i++;
				$j++;	
			}

		}
		else{
			$i++;
		}
	}
	##########################################################


	####create the data1[] array (single array for plotting), into which insert put addresses of plotting arrays 	
	my @data1 = (\@time1);

	
	for ($i = 0; $i < $genNumber; $i++)		
	{
		my @values;
		for ($j = 0; $j < 27; $j++)
		{
			$values[$j] = $genres[$i][$j];
		}
		$data1[$i+1] = \@values;
	}

	my $mygraph1 = GD::Graph::lines->new(750, 450);
	$mygraph1->set(
    		x_label     => 'Year',
    		y_label     => 'Number of shows',
    		title       => 'Amount of genre wax/wane',

		dclrs	    => [ qw(orange blue purple
				green black red dgreen
				dblue dpurple dred
				lorange lblue lpurple lred lgreen) ]	
	) or warn $mygraph1->error;
	#####################################################################
	####create .png file for graph
	$mygraph1->set_legend (@genNames);

	my $myimage1 = $mygraph1->plot(\@data1) or die $mygraph1->error;
	sysopen(PNGFILE1, "genreGraph1.png", O_RDWR|O_CREAT, 0755) or die "Cannot open genreGraph1.png";#|O_EXCL|O_CREAT, 0755) or die "Cannot open genreGraph1.png";
	binmode PNGFILE1;	#destinguishes PNGFILE as a binary file
	print PNGFILE1 $myimage1->png;
	close(PNGFILE1);
	#################################

}

sub networks{			#allows graph generation by network. Not done.
	my @temp = @_;
	
	my $icount = 0;

	my @time1;			#time plotting array
	$time1[0] = 1973;		#fill in the initial time
	
	#####indexing variables				
	my $i;
	my $j;
	my $k;
	##########
	
	for ($i = 1; $i < 26; $i++){	#fill in time plotting array
		$time1[$i] = 1988 + $i;
	}


	##############main loop for creating network plotting arrays. Calls fillArray
	$i = 0;
	$j = 0;
	while ($i < 30){	
		if ($j < 27){			#haven't exceeded size of time
			if ($temp[$i][5] >= $time1[0]){
				if ($temp[$i][5] == $time1[$j]){		#time match 
					&fillArray($temp[$i][3], $i, $j, $temp[$i][5], $temp[$i][6], "networks");
					$i++;
				}
				else{	#time is behind temp[5], and must be brough up

					$j++;
				}	
				
			}
			
			else{	#start date not given
				$i++;
				$j++;	
			}

		}
		else{
			$i++;
		}
	}
	##########################################################


	####create the data1[] array (single array for plotting), into which insert put addresses of plotting arrays 	
	my @data1 = (\@time1);

	
	for ($i = 0; $i < $netNumber; $i++)		
	{
		my @values;
		for ($j = 0; $j < 27; $j++)
		{
			$values[$j] = $networks[$i][$j];
		}
		$data1[$i+1] = \@values;
	}

	my $mygraph1 = GD::Graph::lines->new(750, 450);
	$mygraph1->set(
    		x_label     => 'Year',
    		y_label     => 'Number of shows',
    		title       => 'Amount of network wax/wane',

		dclrs	    => [ qw(orange blue purple
				green black red dgreen
				dblue dpurple dred
				lorange lblue lpurple lred lgreen) ]	
	) or warn $mygraph1->error;
	#####################################################################
	####create .png file for graph
	$mygraph1->set_legend (@netNames);

	my $myimage1 = $mygraph1->plot(\@data1) or die $mygraph1->error;
	sysopen(PNGFILE1, "networkGraph.png", O_RDWR|O_CREAT, 0755) or die "Cannot open networkGraph.png";#|O_EXCL|O_CREAT, 0755) or die "Cannot open genreGraph1.png";
	binmode PNGFILE1;	#destinguishes PNGFILE as a binary file
	print PNGFILE1 $myimage1->png;
	close(PNGFILE1);
	#################################

	print "networks\n";
	
}

sub netCat{			#allows graph generation by category and network. Not done.
	my @temp = @_;
	
	my $icount = 0;

	my @time1;			#time plotting array
	$time1[0] = 1973;		#fill in the initial time
	
	#####indexing variables				
	my $i;
	my $j;
	my $k;
	##########
	
	for ($i = 1; $i < 26; $i++){	#fill in time plotting array
		$time1[$i] = 1988 + $i;
	}


	##############main loop for creating network and genre plotting arrays. Calls fillArray
	$i = 0;
	$j = 0;
	while ($i < 30){	
		if ($j < 27){			#haven't exceeded size of time
			if ($temp[$i][5] >= $time1[0]){
				if ($temp[$i][5] == $time1[$j]){		#time match 
					&fillArray($temp[$i][3], $i, $j, $temp[$i][5], $temp[$i][6], "networks");
					#&fillArray($temp[$i][1], $i, $j, $temp[$i][5], $temp[$i][6], "netGen");
					$i++;
				}
				else{	#time is behind temp[5], and must be brough up

					$j++;
				}	
				
			}
			
			else{	#start date not given
				$i++;
				$j++;	
			}

		}
		else{
			$i++;
		}
	}
	$i = 0;
	$j = 0;
	while ($i < 30){	
		if ($j < 27){			#haven't exceeded size of time
			if ($temp[$i][5] >= $time1[0]){
				if ($temp[$i][5] == $time1[$j]){		#time match 
					&fillArray($temp[$i][1], $i, $j, $temp[$i][5], $temp[$i][6], "genre");
					$i++;
				}
				else{	#time is behind temp[5], and must be brough up

					$j++;
				}	
				
			}
			
			else{	#start date not given
				$i++;
				$j++;	
			}

		}
		else{
			$i++;
		}
	}
	##########################################################


	####create the data1[] array (single array for plotting), into which insert put addresses of plotting arrays 	
	my @data1 = (\@time1);

	my $netInd = 0;
	my $genInd = 0;
	#for ($i = 0; $i < ($netNumber+$genNumber); $i++)
	while ($netInd < $netNumber || $genInd < $genNumber)		
	{
		my @values;
		my @values2;
		for ($j = 0; $j < 27; $j++)
		{
			$values[$j] = $networks[$netInd][$j];	
		}
		
		for ($j = 0; $j < 27; $j++)
		{
			$values2[$j] = $genres[$genInd][$j];
		}
		$data1[$netInd+1] = \@values;
		$data1[$genInd + $netNumber] = \@values2;
		if ($netInd < $netNumber)
		{
			$netInd += 1;
		}
		if ($genInd < $netNumber)
		{
			$genInd += 1;
		}
	}

	my $mygraph1 = GD::Graph::lines->new(750, 450);
	$mygraph1->set(
    		x_label     => 'Year',
    		y_label     => 'Number of shows',
    		title       => 'Amount of network and genre wax/wane',	
		dclrs	    => [ qw(orange blue purple
				green black red dgreen
				dblue dpurple dred
				lorange lblue lpurple lred lgreen) ]
	) or warn $mygraph1->error;
	#####################################################################
	####create .png file for graph
	$mygraph1->set_legend (@netNames, @genNames);

	my $myimage1 = $mygraph1->plot(\@data1) or die $mygraph1->error;
	sysopen(PNGFILE1, "netGenGraph.png", O_RDWR|O_CREAT, 0755) or die "Cannot open networkGraph.png";#|O_EXCL|O_CREAT, 0755) or die "Cannot open genreGraph1.png";
	binmode PNGFILE1;	#destinguishes PNGFILE as a binary file
	print PNGFILE1 $myimage1->png;
	close(PNGFILE1);
	#################################
	print "netCat\n";
}

sub choice{			#allows user to choose graph sorting scheme. Also will put database values into a 2-dimensional array, temp[rows][columns]
	my @temp;		#2-dimensional array that holds values of the database table				
	our $title = 0;
	our $genre = 1;
	our $secGen = 2;	
	our $network = 3;
	our $secNet = 4;
	our $staDat = 5;
	our $endDat = 6;

	###############################put the values of show_data into this 2-dimensional array. The first index is the row, the second index is the column.
	#This array is initially defined for testing purposes
	$temp[0][$title] = "An American Family";
	$temp[0][$genre] = "Intimate";
	$temp[0][$secGen] = "";
	$temp[0][$network] = "PBS";
	$temp[0][$secNet] = "";
	$temp[0][$staDat] = "1973";
	$temp[0][$endDat] = "1973";

	$temp[1][$title] = "COPS";
	$temp[1][$genre] = "Workplace";
	$temp[1][$secGen] = "";
	$temp[1][$network] = "no_network";
	$temp[1][$secNet] = "";
	$temp[1][$staDat] = "1989";
	$temp[1][$endDat] = "-1";

	$temp[2][$title] = "America's Funniest Home Videos";
	$temp[2][$genre] = "Competitive";
	$temp[2][$secGen] = "";
	$temp[2][$network] = "no_network";
	$temp[2][$secNet] = "";
	$temp[2][$staDat] = "1990";
	$temp[2][$endDat] = "-1";

	$temp[3][$title] = "The Real World";
	$temp[3][$genre] = "Intimate";
	$temp[3][$secGen] = "";
	$temp[3][$network] = "MTV";
	$temp[3][$secNet] = "";
	$temp[3][$staDat] = "1992";
	$temp[3][$endDat] = "-1";

	$temp[4][$title] = "Survivor";
	$temp[4][$genre] = "Competitive";
	$temp[4][$secGen] = "";
	$temp[4][$network] = "no_network";
	$temp[4][$secNet] = "";
	$temp[4][$staDat] = "2000";
	$temp[4][$endDat] = "-1";

	$temp[5][$title] = "Big Brother";
	$temp[5][$genre] = "Competitive";
	$temp[5][$secGen] = "";
	$temp[5][$network] = "no_network";
	$temp[5][$secNet] = "";
	$temp[5][$staDat] = "2001";
	$temp[5][$endDat] = "-1";

	$temp[6][$title] = "Amazing Race";
	$temp[6][$genre] = "Competitive";
	$temp[6][$secGen] = "";
	$temp[6][$network] = "no_network";
	$temp[6][$secNet] = "";
	$temp[6][$staDat] = "2001";
	$temp[6][$endDat] = "-1";

	$temp[7][$title] = "Toddlers & Tiaras";
	$temp[7][$genre] = "Workplace";
	$temp[7][$secGen] = "";
	$temp[7][$network] = "no_network";
	$temp[7][$secNet] = "";
	$temp[7][$staDat] = "2001";
	$temp[7][$endDat] = "-1";

	$temp[8][$title] = "American Idol";
	$temp[8][$genre] = "Competitive";
	$temp[8][$secGen] = "";
	$temp[8][$network] = "no_network";
	$temp[8][$secNet] = "";
	$temp[8][$staDat] = "2002";
	$temp[8][$endDat] = "-1";

	$temp[9][$title] = "The Bachelor";
	$temp[9][$genre] = "Competitive";	
	$temp[9][$secGen] = "";
	$temp[9][$network] = "no_network";
	$temp[9][$secNet] = "";
	$temp[9][$staDat] = "2002";
	$temp[9][$endDat] = "-1";

	$temp[10][$title] = "The Osbournes";
	$temp[10][$genre] = "Intimate";
	$temp[10][$secGen] = "";
	$temp[10][$network] = "no_network";
	$temp[10][$secNet] = "";
	$temp[10][$staDat] = "2002";
	$temp[10][$endDat] = "2005";

	$temp[11][$title] = "Extreme Makeover";
	$temp[11][$genre] = "Expert Intervention";
	$temp[11][$secGen] = "";	
	$temp[11][$network] = "no_network";
	$temp[11][$secNet] = "";
	$temp[11][$staDat] = "2002";
	$temp[11][$endDat] = "2007";

	$temp[12][$title] = "America's Next Top Model";
	$temp[12][$genre] = "Competitive";
	$temp[12][$secGen] = "";
	$temp[12][$network] = "CW";
	$temp[12][$secNet] = "";
	$temp[12][$staDat] = "2003";
	$temp[12][$endDat] = "-1";

	$temp[13][$title] = "The Simple Life";
	$temp[13][$genre] = "Intimate";
	$temp[13][$secGen] = "";
	$temp[13][$network] = "no_network";
	$temp[13][$secNet] = "";
	$temp[13][$staDat] = "2003";
	$temp[13][$endDat] = "2007";

	$temp[14][$title] = "Clean House";
	$temp[14][$genre] = "Expert Intervention";
	$temp[14][$secGen] = "";
	$temp[14][$network] = "no_network";
	$temp[14][$secNet] = "";
	$temp[14][$staDat] = "2003";
	$temp[14][$endDat] = "-1";

	$temp[15][$title] = "Newlyweds: Nick and Jessica";
	$temp[15][$genre] = "Intimate";
	$temp[15][$secGen] = "";
	$temp[15][$network] = "no_network";
	$temp[15][$secNet] = "";
	$temp[15][$staDat] = "2003";	
	$temp[15][$endDat] = "2005";

	$temp[16][$title] = "The Bachelorette";
	$temp[16][$genre] = "Competitive";
	$temp[16][$secGen] = "";
	$temp[16][$network] = "no_network";
	$temp[16][$secNet] = "";
	$temp[16][$staDat] = "2003";
	$temp[16][$endDat] = "-1";

	$temp[17][$title] = "Extreme Makeover: Home Edition";
	$temp[17][$genre] = "Expert Intervention";
	$temp[17][$secGen] = "";	
	$temp[17][$network] = "no_network";
	$temp[17][$secNet] = "";
	$temp[17][$staDat] = "2003";
	$temp[17][$endDat] = "2012";

	$temp[18][$title] = "Queer Eye";
	$temp[18][$genre] = "Expert Intervention";
	$temp[18][$secGen] = "";	
	$temp[18][$network] = "no_network";
	$temp[18][$secNet] = "";
	$temp[18][$staDat] = "2003";
	$temp[18][$endDat] = "2007";

	$temp[19][$title] = "The Apprentice";
	$temp[19][$genre] = "Competitive";
	$temp[19][$secGen] = "";
	$temp[19][$network] = "no_network";
	$temp[19][$secNet] = "";
	$temp[19][$staDat] = "2004";
	$temp[19][$endDat] = "-1";

	$temp[20][$title] = "Project Runway";
	$temp[20][$genre] = "Competitive";
	$temp[20][$secGen] = "";
	$temp[20][$network] = "Bravo";
	$temp[20][$secNet] = "Lifetime";
	$temp[20][$staDat] = "2004";
	$temp[20][$endDat] = "-1";

	$temp[21][$title] = "The Biggest Loser";
	$temp[21][$genre] = "Expert Intervention";
	$temp[21][$secGen] = "Competitive";
	$temp[21][$network] = "no_network";
	$temp[21][$secNet] = "";
	$temp[21][$staDat] = "2004";
	$temp[21][$endDat] = "-1";

	$temp[22][$title] = "Dog Whisperer with Cesar Millan";
	$temp[22][$genre] = "Expert Intervention";
	$temp[22][$secGen] = "";
	$temp[22][$network] = "no_network";
	$temp[22][$secNet] = "";
	$temp[22][$staDat] = "2004";
	$temp[22][$endDat] = "-1";

	$temp[23][$title] = "Laguna Beach";
	$temp[23][$genre] = "Intimate";
	$temp[23][$secGen] = "";
	$temp[23][$network] = "MTV";
	$temp[23][$secNet] = "";
	$temp[23][$staDat] = "2004";
	$temp[23][$endDat] = "2006";

	$temp[24][$title] = "Dog the Bounty Hunter";
	$temp[24][$genre] = "Workplace";
	$temp[24][$secGen] = "";
	$temp[24][$network] = "no_network";	
	$temp[24][$secNet] = "";
	$temp[24][$staDat] = "2004";
	$temp[24][$endDat] = "-1";

	$temp[25][$title] = "Dancing with the Stars";
	$temp[25][$genre] = "Competitive";
	$temp[25][$secGen] = "";
	$temp[25][$network] = "no_network";	
	$temp[25][$secNet] = "";
	$temp[25][$staDat] = "2005";
	$temp[25][$endDat] = "-1";

	$temp[26][$title] = "Intervention";
	$temp[26][$genre] = "Expert Intervention";
	$temp[26][$secGen] = "";
	$temp[26][$network] = "no_network";
	$temp[26][$secNet] = "";
	$temp[26][$staDat] = "2005";
	$temp[26][$endDat] = "-1";

	$temp[27][$title] = "Supernanny";
	$temp[27][$genre] = "Expert Intervention";
	$temp[27][$secGen] = "";
	$temp[27][$network] = "no_network";
	$temp[27][$secNet] = "";
	$temp[27][$staDat] = "2005";
	$temp[27][$endDat] = "2011";

	$temp[28][$title] = "Deadliest Catch";
	$temp[28][$genre] = "Workplace";				#Workplace
	$temp[28][$secGen] = "";
	$temp[28][$network] = "no_network";
	$temp[28][$secNet] = "";
	$temp[28][$staDat] = "2005";
	$temp[28][$endDat] = "-1";

	$temp[29][$title] = "Miami Ink";
	$temp[29][$genre] = "Fun";				#Workplace
	$temp[29][$secGen] = "";
	$temp[29][$network] = "no_network";
	$temp[29][$secNet] = "";
	$temp[29][$staDat] = "2005";	
	$temp[29][$endDat] = "2008";
	####################################################################
	
	######################dynamically allocate genre arrays to be plotted, based on the temp array defined above
	my $flag = 0;	
	my $i;
	my $j;
	for ($i = 0; $i < $size; $i++){				#traverse the database table to determine the individual genres
		for ($j = 0; $j < $i; $j++){
			if ($temp[$i][$genre] eq $temp[$j][$genre]){
				$flag = 1;
				last;
			}
		}
		if ($flag == 0){
			my @array;
			$genNames[$genNumber] = $temp[$i][$genre];
			$genres[$genNumber][0] = @array; 
			print "names:$temp[$i][$genre]\n";
			$genNumber++;
		}
		$flag = 0;
	}
	for ($i = 0; $i < $genNumber; $i++)		#initialize each value of genre plotting arrays to zero
	{
		for ($j = 0; $j < 27; $j++)
		{
			$genres[$i][$j] = 0;
		}
	}
	################################################################################################################
	######################dynamically allocate network arrays to be plotted, based on the temp array defined above
	$flag = 0;
	for ($i = 0; $i < $size; $i++){
		for ($j = 0; $j < $i; $j++){				#if the same network was already encountered
			if ($temp[$i][$network] eq $temp[$j][$network]){
				$flag = 1;
				last;
			}
		}
		if ($flag == 0){
			my @array;
			$netNames[$netNumber] = $temp[$i][$network];
			$networks[$netNumber][0] = @array;
			print "networks:$temp[$i][$network]\n";
			$netNumber++;
		}
		$flag = 0;
	}
	for ($i = 0; $i < $netNumber; $i++)		#initialize each value of network plotting arrays to zero
	{
		for ($j = 0; $j < 27; $j++)
		{
			$networks[$i][$j] = 0;
		}
	}
	############################allow user to select graph generation by category, network, or both. So far, only category works.
	my $choice = 0;
	print "Sort by: (1) Category, (2) Network, (3) Category and network \n";
	$choice = <>;		#will be replaced by an html form
	
	if ($choice == 1){
		&categories(@temp);
	}
	elsif ($choice == 2){
		&networks(@temp);
	}
	elsif ($choice == 3){
		&netCat(@temp);
	}
	else{
		print "Not a good choice\n";
	}
	###################################################################################################
} 

&choice();		#initial call
