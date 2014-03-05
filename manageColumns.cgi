=begin comment
pages.cgi

MODULE DESCRIPTION:
    Allows an administrator to view data columns currently in the show_data
    table, as well as add new custom columns and delete custom columns.

MODULE SUBROUTINES
    manageColumns(): Allows an admin to view current static columns and view
                     current custom columns. From here an admin can add columns
                     and delete columns as well.
                     
    addColumn(): Prompts an admin for the name for a new column. Creates a new
                 column within the show_data database column for data.
                 
    deleteColumn(): Prompts the user to confirm intent to delete, then drops the
                    selected column from the show_data database column.

ELSEIF BLOCK

=end comment
=cut


sub manageColumns{
    my $access = $session->param('access');
    if($access >= 1){
        my @arr;
        my @perm;
        my @custom;
        my %names;
        my %id;
        #Link col names against display names
        $db_query = $db->prepare(qq(SELECT id, col_name, name FROM field_names));
        $db_query->execute();
        while (@arr = $db_query->fetchrow_array) {
            $names{$arr[1]} = $arr[2];
            $id{$arr[1]} = $arr[0];
        }
        
        #Get current columns and sort them.
        $db_query = $db->prepare(qq(DESCRIBE show_data));
        $db_query->execute();
        while (@arr = $db_query->fetchrow_array) {
            $fieldName = $arr[0];
            
            if ($fieldName eq 'id' ||$fieldName eq 'title' ||
                $fieldName eq 'genre' || $fieldName eq 'secondary_genre' ||
                $fieldName eq 'network' || $fieldName eq 'secondary_network' ||
                $fieldName eq 'start_date' || $fieldName eq 'end_date'
            ){
                push(@perm,$fieldName);   
            }else{
                push(@custom,$fieldName);
            }
        }
        
        #Output permanent columns
        print qq(<h1>Column Management</h1>);
        print qq(<h2>Permanent Columns</h2>The following columns are permanent and cannot be modified.<ul>);
        for(my $i = 0; $i < @perm; $i++){
            if($perm[$i] ne "id"){
                print qq(<li>).$names{$perm[$i]}.qq(</li>);
            }
        }
        print "</ul>";
        print qq(<h2>Custom Columns (<a onclick="window.open('?s=addColumn', 'newwindow', 'width=320, height=320px'); return false;">New</a>)</h2><table border="1">);
        for(my $i = 0; $i < @custom; $i++){
            my $tmpName = $names{$custom[$i]};
            my $tmpId = $id{$custom[$i]};
            print qq(<tr><td>$tmpName</td><td><a onclick="window.open('?s=deleteColumn&id=$tmpId', 'newwindow', 'width=320, height=320px'); return false;">Delete</a></td></tr>);
        }
        
        print qq(</table>);
    }else{
        print qq(Turn away. There are dragons here, only administrators can tame dragons!);
    }
}

sub addColumn{
    my $a = $CGI->param('a');
    if ($a eq "submit") {
        my $name = $CGI->param('name');
        my $colName = $name;
        $colName =~ s/[^a-zA-Z ]//g;
        $colName =~ s/ /_/gi;
        $colName = lc($colName);
        
        $db_query = $db->prepare("SELECT MAX( weight ) FROM field_names");
        $db_query->execute();
        my @arr = $db_query->fetchrow_array;
        my $maxWeight = $arr[0];
        
        $db_query = $db->prepare("INSERT INTO field_names (col_name,name,weight) VALUES (?,?,?)");
        $db_query->execute($colName,$name,$maxWeight+1);
        
        $db_query = $db->prepare("ALTER TABLE `show_data` ADD $colName TEXT NOT NULL");
        $db_query->execute();
        
        print qq(
        <div align="center">
        Column Added.<br /><br />
        <script>window.opener.location.reload(false);</script>
        <button onclick="window.close();return false;">Close Window</button>
        </div>
        );
    }else{
        my $access = $session->param('access');
        if($access >= 1){
            print qq(
                <form>
                    <fieldset>
                        <label>New Column Name:<label>
                        <input type="text" name="name"><br />
                        <input type="hidden" name="s" value="addColumn">
                        <input type="hidden" name="a" value="submit">
                        <button>Add Column</button>
                    </fieldset>
                </form>
            )
        }else{
            print qq(Turn away. There are robots here, only administrators can tame robots!);
        }
    }
}

sub deleteColumn{
    if($session->param("access")>=1){
            $a = $CGI->param("a");
            if ($a eq "delete") {
                    my $id = $CGI->param('id');
                    my $colName = $CGI->param('colName');
                    
                    $db_query = $db->prepare("DELETE FROM field_names WHERE id='$id'");
                    $db_query->execute();
                    
                    $db_query = $db->prepare("ALTER TABLE `show_data` DROP $colName");
                    $db_query->execute();

                    print qq(
                    <div align="center">
                    Column deleted.<br /><br />
                    <script>window.opener.location.reload(false);</script>
                    <button onclick="window.close();return false;">Close Window</button>
                    </div>
                    );
            }else{
                    my $id = $CGI->param('id');
                    $db_query = $db->prepare("SELECT col_name, name FROM field_names WHERE id = ?");
                    $db_query->execute($id);
                    
                    my @arr = $db_query->fetchrow_array();
                    my $colName = $arr[0];
                    my $name = $arr[1];
                    print qq(
                            <div align="center">
                            Are you sure you want to delete the <strong>$name</strong> column?<br><br />
                            This cannot be undone and <u>all associated data will be deleted</u>.<br /><br />
                            <form>
                            <input type="hidden" name="id" value="$id">
                            <input type="hidden" name="s" value="deleteColumn">
                            <input type="hidden" name="colName" value="$colName">
                            <button name="a" value="delete">Delete</button></fieldset></form>
                            <button onclick="window.close();return false;">Cancel</button>
                            </div>
                    );
            }
    }else{
            print("Access denied.");
    }
}