=begin comment
pages.cgi

MODULE DESCRIPTION:
	Allows a user to propose changes to the dataset after searching it. The user
	is permitted to suggest a change to one field of one entry at a time.
	
MODULE SUBROUTINES
	propose(): Allows a user to propose an edit to a field from the show_data
			   db table. The user select the column from the field they want to
			   edit and enters their propsed edit. The edit is added to the
			   admin_queue db table for admin approval.

ELSEIF BLOCK
	+------------+
	| USER LEVEL |
	+------------+
	#PUBLIC MODULE: propose.cgi
	elsif	($s eq 'proposeData')		{ proposeData(); }
	elsif	($s eq 'proposeShow')		{ proposeShow(); }

=end comment
=cut

sub proposeData{
    my @columns;
    my @arr;
    my $inner_query;
    my @inner;
    my $id = $CGI->param("id");
    my $a = $CGI->param("a");
    print qq(<h1>Propose Change</h1>);
    if ($a eq "submit") {
        my $col = $CGI->param('col');
	my $content = $CGI->param('content');
	my $id = $CGI->param('id');
	my $uid = $session->param("id");
	
	$db_query = $db->prepare("INSERT INTO admin_queue (user, type, entry, field, content) VALUES (?, ?, ?, ?, ?)");
	$db_query->execute($uid,'proposal',$id,$col,$content);
	
	print qq(Thank you for your proposal<br /><br /><button onclick="window.close();return false;">Close Window</button>)
	
    }elsif($a eq "select"){
        my $fieldName = $CGI->param('field');
        my $colName = $CGI->param('col');
	my $content = $CGI->param('content');
	my $show = $CGI->param('show');
	
	$fieldName = lc($fieldName);
	
	print qq(
	    <form><fieldset>
		<label>Proposing a change to the <strong>$fieldName</strong> of the show "<strong>$show</strong>"<br>Please enter your proposed change below</label>
		<input type="text" name="content" value="$content">
	    </fieldset>
	    
	    <input type="hidden" name="id" value="$id">
	    <input type="hidden" name="col" value="$colName">
	    <input type="hidden" name="s" value="proposeData">
	    <input type="hidden" name="a" value="submit">
	    <button>Propose Change</button>
	);
    }else{
	my $showName = "";
        my $db_query = $db->prepare("DESCRIBE show_data");
		$db_query->execute();
		while (@arr = $db_query->fetchrow_array) {
			push(@columns,$arr[0]);
		}
		
		my $db_query = $db->prepare("SELECT * FROM show_data WHERE id = '$id'");
		$db_query->execute();
		
		print qq(<table border="1"><tr><td><strong>Field</strong></td><td><strong>Content</strong></td></tr>);
		
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
					if ($fieldName eq "Title") {
					    $showName = $colData;
					}
					
					print qq(<tr><td>$fieldName</td><td>$colData</td><td><a href="?s=proposeData&a=select&field=$fieldName&col=$colName&content=$colData&show=$showName&id=$id">Propose Change</a></td></td>);
				}
			}
		}
		print qq(
            </table>
            <button onclick="window.close();return false;">Cancel</button>
        );
	}
}

sub proposeShow{
    my $a = $CGI->param('a');
    if ($a eq "submit") {
	my $uid = $session->param("id");
	my $showName = $CGI->param('showName');
	
	$db_query = $db->prepare("INSERT INTO admin_queue (user, type, entry, field, content) VALUES (?, ?, ?, ?, ?)");
	$db_query->execute($uid,'show',0,0,$showName);

	print qq(Thank you for your proposal<br /><br /><button onclick="window.close();return false;">Close Window</button>)
    }
    
    else{
	print qq(
	    <h1>Propose new show</h1>
	    You may propose a new show if you feel it belongs in the dataset and is not already represented. All show proposals will be reviewed by an administrator.<br /><br />
	    <form>
		<fieldset>
		    <label>Show Name</label>
		    <input type="text" name="showName" />
		</fieldset>
		<input type="hidden" name="s" value="proposeShow">
		<input type="hidden" name="a" value="submit">
		<button>Propose show</button>
	    </form>
	)
    }
}