=begin comment
edit.cgi

MODULE DESCRIPTION:
		Allows an admin to edit entries in that are displayed after searching
		the dataset. 

MODULE SUBROUTINES
		edit(): Creates the interface allowing an admin to change data held
				within the show_data db table. Once an admin submit a change
				the subroutine updates the database accordingly

ELSEIF BLOCK
		+-------------+
		| ADMIN LEVEL |
		+-------------+
		#ADMIN MODULE: edit.cgi
		elsif	($s eq 'edit')			{ edit(); }
=end comment
=cut


sub edit{
	my @columns;
	my @arr;
	my $inner_query;
	my @inner;
	my $id = $CGI->param("id");
	my $a = $CGI->param("a");
	
	if ($a eq "confirm") {
		my @params = $CGI->param;
		my $query = qq(UPDATE show_data SET );
		for( my $i = 0; $i < @params; $i++ ){
			my $param = $params[$i];
			if ($param ne "s" && $param ne "a") {
				my $pValue = $CGI->param("$param");
				$pValue =~ s/'/&#39;/g;
				$pValue =~ s/"/&#34;/g;
				$query .= qq($param='$pValue', );
			}
		}
		$query =~ s/, $//;
		$query =~ s/current/-1/i;
		$query .= qq( WHERE id='$id');
		$db_query = $db->prepare($query);
		$db_query->execute();
		print qq(
		<div align="center">Show updated successfully.<br /><script>window.opener.location.reload(false);</script><button onclick="window.close();return false;">Close Window</button>
		);
	}elsif ($a eq "delete") {
		$db_query = $db->prepare("DELETE FROM show_data WHERE id=?");
		$db_query->execute($id);
		print qq(
		<div align="center">Show deleted successfully.<br /><script>window.opener.location.reload(false);</script><button onclick="window.close();return false;">Close Window</button>
		);
	}else{
		my $db_query = $db->prepare("DESCRIBE show_data");
		$db_query->execute();
		while (@arr = $db_query->fetchrow_array) {
			push(@columns,$arr[0]);
		}
		
		
		my $db_query = $db->prepare("SELECT * FROM show_data WHERE id = '$id'");
		$db_query->execute();
		
		print qq(<form><fieldset>);
		
		while (@arr = $db_query->fetchrow_array) {
			for(my $i = 0; $i < @arr; $i++){
				my $colName = $columns[$i];
				my $colData = $arr[$i];
				
				if ($colName ne "id") {
					if ($colName eq "end_date" && $colData == -1) {
						$colData = "Current"
					}
					
					$inner_query = $db->prepare("SELECT name FROM field_names WHERE col_name = '$colName'");
					$inner_query->execute();
					@inner = $inner_query->fetchrow_array();
					my $fieldName = $inner[0];
					
					print qq(<label>$fieldName</label>);
					print qq(<input type="text" name="$colName" value="$colData"<br />);
				}
			}
		}
		print qq(
		<br ><input type="hidden" name="id" value="$id"><input type="hidden" name="s" value="edit">
		<button name="a" value="confirm">Update</button></fieldset></form>
		<button onclick="window.close();return false;">Cancel</button>
		<button onclick="if(confirm('Are you sure you want to delete this entry?')){window.location = '?s=edit&a=delete&id=$id';}else{return false;}">Delete</button>);
	}
}