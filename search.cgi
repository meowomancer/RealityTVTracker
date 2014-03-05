=begin comment
search.cgi

MODULE DESCRIPTION:
		Allow a user to search/filter the dataset by dynamically creating
		drop-down boxes from existing columns and the data contained within each
		one, as well as a text search box for show titles.

MODULE SUBROUTINES
		search(): Creates and validates the search field. Queries the database
				  with search terms and renders the results as a table. From
				  here admins can edit the data, and users can flag entries or
				  propose changes to the entries. 

ELSEIF BLOCK
		#PUBLIC MODULE: search.cgi
		elsif 	($s eq 'search') 		{ search(); }
=end comment
=cut

sub search{
	my $inner_query;
	my @arr;
	my @inner;
	
	my $numFields = 0;
	my %formData;
	my %fieldNames;
	my %fieldOrder;
	
	my $a = $CGI->param("a");
	
	print qq(
	<script>
	function validateForm(){
		var title = document.forms["search"]["title"].value;
		var start_date = document.forms["search"]["start_date"].value;
		var end_date = document.forms["search"]["end_date"].value;
		var genre = document.forms["search"]["genre"].value;
		var network = document.forms["search"]["network"].value;
		if(title == "" && start_date == "null" && end_date == "null" && genre == "null" && network == "null"){
			alert("One search critera from title, start date, end date, genre, or network is required.");
			return false;
		}else{
			return true;					
		}
	}
	</script>
	);
	
	if ($a eq "search") {
		my @names = $CGI->param;
		my $numArgs = @names;
		my $query = "SELECT * FROM show_data WHERE ";
		my $firstQuery = 0;
		my $printString = "";
		my $header = "";
		
		$db_query = $db->prepare("SELECT col_name, name, weight FROM field_names WHERE weight >= 0");
		$db_query->execute();
		
		while (@arr = $db_query->fetchrow_array) {
			my($column,$name,$weight) = @arr;
			$fieldNames{$column} = $name;
			$fieldOrder{$weight} = $column;
			$numFields++;
		}
		
		
		$db_query = $db->prepare("DESCRIBE show_data");
		$db_query->execute();
		
		while(@arr = $db_query->fetchrow_array()){
			my $column = @arr[0];
			if($column eq 'id' || $column eq 'title'){
			}else{
				if ($column =~ /secondary/i) {$column =~ s/secondary_//gi;}
				else{$inner_query = $db->prepare("SELECT DISTINCT $column FROM show_data ORDER BY $column ASC");}
				
				if(!exists $formData{$column}){
					$formData{$column} = qq(<option value="null">N/A</option>);
					$inner_query->execute();
					while(@inner = $inner_query->fetchrow_array()){
						if(@inner[0] eq "-1"){@inner[0]="Current";}
						if(@inner[0] ne ""){
							my $selected = 0;
							for(my $i = 0; $i < $numArgs; $i++){
								if ($CGI->param($names[$i]) eq @inner[0] && $names[$i] eq $column) {
									$selected = 1;
								}
							}
							if($selected){
								$formData{$column} .= qq(<option value="@inner[0]" selected>@inner[0]</option>);
							}else{
								$formData{$column} .= qq(<option value="@inner[0]">@inner[0]</option>);
							}
							
						}
					}
				}
			}
		}
		my $title = $CGI->param('title');
		print qq(
			<div align="center"><form name="search" onsubmit="return validateForm()"><fieldset><table border=0px>
				<tr><td colspan="2" style="padding-left:125px;padding-right:125px;">
				<label>Title</label>
				<input type="text" name="title" value="$title">
				</td></tr><tr>);
		
		for(my $i = 0; $i < $numFields; $i++){
			if($i > 0 && $i%2 == 0){
				print qq(</tr><tr>)
			}
			print qq(
				<td style="padding-left:125px;padding-right:125px;">
				<label>$fieldNames{$fieldOrder{$i}}</label>
					<select name="$fieldOrder{$i}">
						$formData{$fieldOrder{$i}}
					</select>
				</td>
			);
				
		}
		
		print qq(</tr><tr><td colspan="2" style="padding-left:125px;padding-right:125px;"><input type="hidden" name="s" value="search"><input type="hidden" name="a" value="search"><button>Search</button> or <a href="?s=graph">generate a graph</a></td></table></fieldset></form><hr />);
		
		#BEGIN OUTPUT
		#Prepare Header
		my $tableHeader = "<tr>";
		$db_query = $db->prepare("DESCRIBE show_data");
		$db_query->execute();
		
		while(@arr = $db_query->fetchrow_array()){
			my $column = @arr[0];
			if ($column =~ /secondary/ || $column =~ /id/) {}
			else{
				$inner_query = $db->prepare("SELECT name FROM field_names WHERE col_name='$column'");
				$inner_query->execute();
				
				@inner = $inner_query->fetchrow_array();
				
				$column = $inner[0];
				
				$tableHeader .= qq(<td><strong>$column</strong></td>)
			}
		}
		
		$tableHeader .= qq(</tr>);

		for (my $i = 0; $i < $numArgs; $i++){
			my $param = $CGI->param($names[$i]);
			if ($param eq "Current") {
				$param = 3000;
			}
			if ($param ne 'null' && $param ne '' && ($names[$i] ne 'a' && $names[$i] ne 's')) {
				if ($firstQuery) {$query .= " AND "}
				if($names[$i] eq 'start_date'){
					$query .= qq($names[$i] >= '$param');
					$firstQuery = 1;
				}elsif($names[$i] eq 'end_date'){
					if ($param == 3000) {
						$query .= qq($names[$i] <= '$param');
					}else{
						$query .= qq($names[$i] <= '$param' AND $names[$i] >= 1900);
					}
					$firstQuery = 1;
				}elsif($names[$i] eq 'title'){
					$query .= qq($names[$i] LIKE '%$param%');
					$firstQuery = 1;
				}else{	
					$query .= qq($names[$i] = '$param');
					$firstQuery = 1;
				}
			}
		}
		$query .= qq( ORDER BY title ASC);
		if($DEBUG){print $query;}
		$db_query = $db->prepare($query);
		$db_query->execute();
		if ($session->param('access') == 0 && $session->param('name')) {
			print qq(<div align="right">[<a onclick="window.open('?s=proposeShow', 'newwindow', 'width=500, height=718px'); return false;">Propose a new show</a>]</div>);
		}
		print qq(<table border="1px">\n $tableHeader);
		my $id;
		while (@arr = $db_query->fetchrow_array) {
			$printString = qq(<tr>);
			for(my $i = 1; $i < @arr; $i++){
				my $genreCheck = $arr[$i-1];
				my $param = $arr[$i];
				$param =~ s/\s+$//;
				if (grep( /^$param$/gi, @genres)){
					if ($arr[$i+1] ne "") {
						$param = $param." / $arr[$i+1]";
					}
					$i++;					
					$printString .= qq(<td>$param</td>);
				}
				elsif (grep( /^$param$/gi, @networks) && $param ne "no_network") {
					if ($arr[$i+1] ne "") {
						$param = $param." / $arr[$i+1]";
					}
					$i++;
					$printString .= qq(<td>$param</td>);
				}
				elsif($param eq "no_network"){
					$i++;
					$printString .= qq(<td></td>);
				}
				elsif($param eq ""){
					if ($i != 5) {
						$printString .= qq(<td>$i</td>);
					}
				}
				else{
					if ($param eq "-1") {$param = "Current"}
					$printString .= qq(<td>$param</td>);
				}
				$id = $arr[0];
			}
			
			#TODO
			if ($session->param('access') == 0 && $session->param('name')) {
				$printString .= qq(<td><a onclick="window.open('?s=flag&id=$id', 'newwindow', 'width=350, height=718px'); return false;">Flag</a></td><td><a onclick="window.open('?s=proposeData&id=$id', 'newwindow', 'width=500, height=718px'); return false;">Propose Data</a></td></tr>)				
			}elsif ($session->param('access') => 1 && $session->param('name')){
				$printString .= qq(<td><a onclick="window.open('?s=edit&id=$id', 'newwindow', 'width=300, height=718px'); return false;">Edit</a></td></tr>)
			}else{
				$printString .= qq(</tr>);				
			}
			
			print $printString."\n";
		}
		print qq(</table></div>);
	
	#NO ACTION
	}
	else{
		$db_query = $db->prepare("SELECT col_name, name, weight FROM field_names WHERE weight >= 0");
		$db_query->execute();
		
		while (@arr = $db_query->fetchrow_array) {
			my($column,$name,$weight) = @arr;
			$fieldNames{$column} = $name;
			$fieldOrder{$weight} = $column;
			$numFields++;
		}
		
		
		$db_query = $db->prepare("DESCRIBE show_data");
		$db_query->execute();
		
		while(@arr = $db_query->fetchrow_array()){
			my $column = @arr[0];
			if($column eq 'id' || $column eq 'title'){
				#Nothing
			}else{
				if ($column =~ /secondary/i) {$column =~ s/secondary_//gi;}
				else{$inner_query = $db->prepare("SELECT DISTINCT $column FROM show_data ORDER BY $column ASC");}
				
				if(!exists $formData{$column}){
					#if($column ne "start_date" && $column ne "end_date"){$formData{$column} = qq(<option value=""></option>);}
					#else{$formData{$column} = "";}
					$formData{$column} = qq(<option value="null"></option>);	
					$inner_query->execute();
					while(@inner = $inner_query->fetchrow_array()){
						if(@inner[0] eq "-1"){@inner[0]="Current";}
						if(@inner[0] ne ""){$formData{$column} .= qq(<option value="@inner[0]">@inner[0]</option>);}
					}
				}
			}
		}
		print qq(
			<div align="center"><form name="search" onsubmit="return validateForm()"><fieldset><table border=0px>
				<tr><td colspan="2" style="padding-left:125px;padding-right:125px;">
				<label>Title</label>
				<input type="text" name="title">
				</td></tr><tr>);
		
		for(my $i = 0; $i < $numFields; $i++){
			if($i > 0 && $i%2 == 0){
				print qq(</tr><tr>)
			}
			print qq(
				<td style="padding-left:125px;padding-right:125px;">
				<label>$fieldNames{$fieldOrder{$i}}</label>
					<select name="$fieldOrder{$i}">
						$formData{$fieldOrder{$i}}
					</select>
				</td>
			);
				
		}
		
		print qq(</tr><tr><td colspan="2" style="padding-left:125px;padding-right:125px;"><input type="hidden" name="s" value="search"><input type="hidden" name="a" value="search"><button>Search</button> or <a href="?s=graph">generate a graph</a></td></table></fieldset></form></div><hr />);
	}	
}
