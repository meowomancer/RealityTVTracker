=begin comment
admin.cgi

MODULE DESCRIPTION:
    Allows an administrator to see an index of all other admin actions as well
    as view and monitor the admin queue. From the admin queue an admin may view
    pending user flags, edit flagged items, resolve flags, view pending user
    change propositions and accept or deny the proposed change. 

MODULE SUBROUTINES
    admin(): Shows all admin actions possible. Also creates visual alerts when
             there are items in the admin queue
             
    adminQueue(): Allows an admin to view the admin queue, edit flagged items
                  accept or deny user change proposals and and resolve flaged
                  items after or without making a change.
    
    dismiss(): Removes a flag entry from the admin_queue db table
    
    acceptChange(): Automatically makes the edit to the show_data db that a user
                    has proposed. 

ELSEIF BLOCK
    +-------------+
    | ADMIN LEVEL |
    +-------------+
    #ADMIN MODULE: admin.cgi
    elsif	($s eq 'admin')			{ admin(); }
    elsif	($s eq "adminQueue")	{ adminQueue(); }
    elsif	($s eq "dismiss")		{ dismiss(); }
    elsif	($s eq "accept")		{ acceptChange(); }
    elsif       ($s eq "acceptShow")    {acceptShow();}

=end comment
=cut


my %fieldNames;
$db_query = $db->prepare("SELECT col_name, name FROM field_names");
$db_query->execute();

while (@arr = $db_query->fetchrow_array) {
        my($column,$name) = @arr;
        $fieldNames{$column} = $name;
} 

sub admin{
    my $access = $session->param('access');
    if($access >= 1){
        $db_query = $db->prepare("SELECT COUNT(*) FROM admin_queue");
        $db_query->execute();
        my @arr = $db_query->fetchrow_array;
        my $queueCount = $arr[0];
        
        if ($queueCount) {
            warning("$queueCount unresolved item(s) in the Administrator Queue");
        }
        
        print qq(
            <h1>Administrator Control Panel</h1>
            <h3 style="margin-bottom: -5px;">Database Management</h3>
            Database Management lets you modify the aspects of your database. Here you can add data to you existing dataset, add new columns to your dataset, and manage flagged content and monitor data proposals
            <ul style="padding-top: 5px;">
                <li><a href="?s=addData">Add New Data</a></li>
                <li><a href="?s=manageColumns">Manage Columns</a></li>
                <li><a href="?s=adminQueue">Manage administrator queue ($queueCount)</a></li>
            </ul>
            <h3 style="margin-bottom: -5px;">Website Management</h3>
            Website management allows you to create and edit pages with static information. These pages can be connected to the header-bar of the website, or accessed via URLs
            <ul style="padding-top: 5px;">
                <li><a href="?s=newPage">New page</a></li>
                <li><a href="?s=managePages">Manage pages</a></li>
            </ul>
            <h3 style="margin-bottom: -5px;">User Management</h3>
            <ul style="padding-top: 5px;">
                <li><a href="?s=manageUsers&a=add">Add User</a></li>
                <li><a href="?s=manageUsers">Manage existing users</a></li>
            </ul>
        );
    }else{
        print qq(Acess denied.);
    }
}

sub adminQueue{

    print qq(<h1>Admin Queue</h1>);
    $db_query = $db->prepare("SELECT id,user,type,entry,field,content FROM admin_queue WHERE type = 'flag'");
    $db_query->execute();
    my @arr;
    print qq(
        <h4>Flags</h4>
        <table border="1">
        <tr><td><strong>Show</strong></td><td><strong>Issue</strong></td><td><strong>Reported by</strong></td><td><strong>Actions</strong></td></tr>  
    );
    while (@arr = $db_query->fetchrow_array) {
        my($id,$user,$type,$entry,$field,$content) = @arr;
        
        #Match show id against a show title
        my $inner_query = $db->prepare("SELECT title FROM show_data WHERE id = ?");
        $inner_query->execute($entry);
        my @inner = $inner_query->fetchrow_array;
        my $showName = @inner[0];
        
        #Match flag number to flag text
        my $issue;
        
        if ($field == 1) {
            $issue = qq(Inaccurate or misspelled title)
        }
        elsif ($field == 2){
            $issue = qq(Inaccurate year on air <em>or</em> program no longer airing)
        }
        elsif ($field == 3){
            $issue = qq(Inaccurate category)
        }
        elsif ($field == 4){
            $issue = qq(Incorrect network)
        }
        elsif ($field == 5){
            $issue = qq(Listing needs updating for other reasons)
        }
        
        #Match user id to username
         my $inner_query = $db->prepare("SELECT username FROM users WHERE id = ?");
        $inner_query->execute($user);
        my @inner = $inner_query->fetchrow_array;
        my $username = @inner[0];
        #Print table row
        print qq(
            <tr>
                <td>$showName</td>
                <td>$issue</td>
                <td>$username</td>
                <td>
                    [<a onclick="window.open('?s=edit&id=$entry', 'newwindow', 'width=300, height=718px'); return false;">Edit Show</a>]
                    [<a href='?s=dismiss&id=$id'>Resolve</a>]
                    
                </td>
            </tr>
        )
    }
    print qq(</table>);
    
    $db_query = $db->prepare("SELECT id,user,type,entry,field,content FROM admin_queue WHERE type = 'proposal'");
    $db_query->execute();
    my @arr;
    print qq(
        <br /><h4>Change Proposals</h4>
        <table border="1">
        <tr><td><strong>Show</strong></td><td><strong>Field</strong></td><td><strong>Current Data</strong></td><td><strong>Proposed Data</strong></td><td><strong>Proposed By</strong></td><td><strong>Actions</strong></td></tr>  
    );
    while (@arr = $db_query->fetchrow_array) {
        my($id,$user,$type,$entry,$field,$content) = @arr;
        
        #Match show id against a show title
        my $inner_query = $db->prepare("SELECT title, $field FROM show_data WHERE id = ?");
        $inner_query->execute($entry);
        my @inner = $inner_query->fetchrow_array;
        my $showName = $inner[0];
        my $currData = $inner[1];
        my $fieldName = $fieldNames{$field};
        
        #Match user id to username
        my $inner_query = $db->prepare("SELECT username FROM users WHERE id = ?");
        $inner_query->execute($user);
        my @inner = $inner_query->fetchrow_array;
        my $username = @inner[0];
        
        print qq(
            <tr>
            <td>$showName</td>
            <td>$fieldName</td>
            <td>$currData</td>
            <td>$content</td>
            <td>$username</td>
             <td>
                [<a href="?s=accept&field=$field&content=$content&id=$entry&show=$showName&propId=$id">Accept</a>]
                [<a href='?s=dismiss&id=$id'>Reject</a>]
            </td>
            </tr>
        );
        
    
    }
    print qq(</table>);
    
    $db_query = $db->prepare("SELECT id,user,content FROM admin_queue WHERE type = 'show'");
    $db_query->execute();
    my @arr;
    print qq(
        <br /><h4>Show Proposals</h4>
        <table border="1">
        <tr><td><strong>Proposed Show</strong></td><td><strong>Proposed By</strong></td></tr>
    );
    while (@arr = $db_query->fetchrow_array) {
        my($id,$user,$content) = @arr;
        
        #Match user id to username
        my $inner_query = $db->prepare("SELECT username FROM users WHERE id = ?");
        $inner_query->execute($user);
        my @inner = $inner_query->fetchrow_array;
        my $username = @inner[0];
        
        print qq(
            <tr>
            <td>$content</td>
            <td>$username</td>
             <td>
                [<a onclick="window.open('?s=acceptShow&id=$id', 'newwindow', 'width=300, height=718px'); return false;">Accept Show</a>]
                [<a href='?s=dismiss&id=$id'>Reject</a>]
            </td>
            </tr>
        );
        
    
    }
    print qq(</table>);
    
}

sub dismiss{
    my $id = $CGI->param('id');
    $db_query = $db->prepare("DELETE FROM admin_queue WHERE id = ?");
    $db_query->execute($id);
    if($_[0] ne "no"){
        success("Flag dismissed!");
        adminQueue();
    }
}
sub acceptChange{
    my $field = $CGI->param('field');
    my $content = $CGI->param('content');
    my $id = $CGI->param('id');
    my $propId = $CGI->param('propId');
    my $show = $CGI->param('show');
    my $fieldName = $fieldNames{$field};
    $fieldName = lc($fieldName);
    
    $db_query = $db->prepare("UPDATE show_data SET $field=? WHERE id = ?");
    $db_query->execute($content,$id);
    
    $db_query = $db->prepare("DELETE FROM admin_queue WHERE id = ?");
    $db_query->execute($propId);
    
    success("Successfully updated $show\'s $fieldName to $content");
    adminQueue();
}
sub acceptShow{
        my $id = $CGI->param('id');
        $db_query = $db->prepare("SELECT content FROM admin_queue WHERE id = ?");
        $db_query->execute($id);
        my @arr = $db_query->fetchrow_array;
        my $showName = $arr[0];
        
        $db_query = $db->prepare("INSERT INTO show_data (title,start_date,end_date) VALUES (?,1900,-1)");
        $db_query->execute($showName);
        my $showId = $db->{'mysql_insertid'};
        
        dismiss("no");
        
        print qq(<script>window.opener.location.reload(false);</script>);
        $CGI->param('id', $showId);
        success(qq(Added "$showName" to database. You may edit it below.));
        edit();

}