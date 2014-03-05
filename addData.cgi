=begin comment
addData.cgi

MODULE DESCRIPTION:
		Allows an administrator to add data to the show_data column, containing
		all graphable and searchable data.

MODULE SUBROUTINES
		addData(): Creates the interface for adding data, and adds the data to
				   the DB upon successful input.

ELSEIF BLOCK
		+-------------+
		| ADMIN LEVEL |
		+-------------+
		#ADMIN MODULE: addData.cgi
		elsif	($s eq "addColumn")		{ addColumn(); }

=end comment
=cut


sub addData{
	my $access = $session->param('access');
	if($access >= 1){
		$a = $CGI->param('a');
		
		if ($a eq 'submit') {
			my @names = $CGI->param;
			my $numArgs = @names;
			my $query = "";
			my $columns = "";
			my $values = "";
			
			#Build SQL INSERT Statement
			for(my $i = 0; $i < $numArgs; $i++){
				#If not s or a...
				if ($names[$i] ne "s" && $names[$i] ne "a") {
					my $value = $CGI->param($names[$i]);
					$columns .= qq(`$names[$i]`,);
					$values .= qq('$value',);
				}
			}
			
			#Clean up query elements
			$columns =~ s/,$//;
			$values =~ s/,$//;
			
			$query .= qq(INSERT INTO show_data ($columns) VALUES ($values));
			
			$db_query = $db->prepare($query);
			$db_query->execute();
			
			success("Show added!");
			$CGI->param("a","");
			addData();
		}
		
		#If no action is defined
		else{
			my @arr;
			my $inner_query;
			my @inner;
			
			#Query DB for columns
			$db_query = $db->prepare("DESCRIBE show_data");
			$db_query->execute();
			
			#Prepare table and form
			print qq(<form><table border=0px>);
			
			#For each column...
			while (@arr = $db_query->fetchrow_array) {
				my $column = @arr[0];
				if ($column ne "id") {
					#Relate column ID to proper name	
					$inner_query = $db->prepare("SELECT name FROM field_names WHERE col_name='$column'");
					$inner_query->execute();
					@inner = $inner_query->fetchrow_array();
					my $colName = $inner[0];
					
					#Print form field
					print qq(<tr><td align="right">$colName:</td><td><input type="text" name="$column"></input></td></tr>);
				}
				
			}
			
			#End Table
			print qq(<tr><td colspan="2" align="right"><input type="hidden" name="a" value="submit"><input type="hidden" name="s" value="addData"> <button>Add</button></td></table border=1px></form>);
		}
	}
}