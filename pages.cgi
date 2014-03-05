=begin comment
pages.cgi

MODULE DESCRIPTION:
    Manages pages within the system. Pages are static HTML pages, such as an
    "about us" page or "contact" page. 

MODULE SUBROUTINES
    newPage(): Create a new page
    editPage(): Edit an existing page
    managePages(): See existing pages and manager the re-ordering of them.
    
HELPER SUBROUTINES
    initEditor(): Initiates the WYSIWG editor

ELSEIF BLOCK
	+------------+
	| USER LEVEL |
	+------------+
	USER MODULE: pages.cgi
    elsif($s eq "showPage") { showPage(); }
	
	+-------------+
	| ADMIN LEVEL |
	+-------------+
	ADMIN MODULE: pages.cgi
    elsif($s eq "newPage"){ newPage(); }
    elsif($s eq "editPage"){ editPage(); }
    elsif($s eq "managePages") { managePages(); }
	

=end comment
=cut
my $access = $session->param('access');

sub newPage{
    if($access >= 1){
        initEditor();
        print qq( <h3> New Page </h3><hr>
                <form method='POST'>
                        <table border='0' class="admin-editTable">
                                <tr>
                                        <td class="admin-td">Title:</td>
					<td><input class='admin-input' type='text' name='title'></td>
                                </tr>
                                <tr>
                                        <td valign='top'>Body:</td>
					<td><textarea name="content" style="width:100%" id="area"></textarea></td>
                                </tr>				
				<tr>
                                        <td>Header:</td>
					<td><input type='checkbox' name='header'></td>
                                </tr>
				<tr>
                                        <td></td>
					<td>
						<br />
						<span align='right'><input type='hidden' name='action' value='post'>
						<button name='s' value='editPage'>Create Page</button></span>
					</td>
                                </tr>
                        </table>
                </form>
		<script>
			var opts = {textarea: "content",clientSideStorage:false};
			var editor = new EpicEditor(opts).load();
		</script>
		<hr />
        );
    }
}

sub editPage{
    if($access >= 1){
        #Set the date
        my ($sec,$min,$hour,$day,$month,$yr19,@rest) = localtime(time);
        my $date = ($yr19+1900)."-".($month+1)."-".$day;

        #Figure out action
        my($action) = ($CGI->param('action'));

        #Post new page
        if($action eq "post"){
                my($title, $content, $header) = ($CGI->param('title'),$CGI->param('content'),$CGI->param('header'));

		if($header eq "on"){$header = "1"}
		elsif($header eq ""){$header = "0"}

		$title =~ s/\'/&#39;/g;
		$content =~ s/\'/&#39;/g;
		$title =~ s/\"/&#34;/g;
		$content =~ s/\"/&#34;/g;
        
		my $contentPreview = $content;
		
                print("Preview before posting:<br /><br />");
                print("<table border='1' width='100%' cellpadding='10'><tr><td>");
                
		
		print("<h1>$title</h1><hr />$contentPreview");

		print("</td></tr></table><br /><br />");
                print("<form method='POST'>
                <input type='hidden' name='action' value='confirm'>
                <input type='hidden' name='title' value='" . $title . "'>
                <input type='hidden' name='content' value='" . $content . "'>
                <input type='hidden' name='header' value='" . $header . "'>
                <button name='s' value='editPage'>Post</button>");
	}

	#Confirm and insert into mysql
	elsif($action eq "confirm"){

                my($title, $content, $header) = ($CGI->param('title'),$CGI->param('content'),$CGI->param('header'));

                $title =~ s/\'/&#39;/g;
                $content =~ s/\'/&#39;/g;

		$db_query = $db->prepare("SELECT MAX(weight) AS weight FROM pages;");
		$db_query->execute();
		my($weight) = $db_query->fetchrow_array();

		$weight = $weight+1;

                $db_query = $db->prepare("INSERT INTO pages (title, content, date, weight,header) VALUES (?,?,?,?,?);");
                $db_query->execute($title,$content,$date,$weight,$header);

                success("New page posted!");
                $session->param("a","");
                admin();	

	#Delete existing page
        }elsif($action eq "delete"){
                #Get info from the DB
                my @arr;
                my($id) = ($CGI->param('id'));
                $db_query = $db->prepare("SELECT title,content FROM pages WHERE id='$id'");
                $db_query->execute();
                @arr = $db_query->fetchrow_array();
                my($title,$content) = @arr;

                #Form the page              
                print("Are you sure you want to delete the following page?<br /><br />");
                print("<table border='1' width='100%' cellpadding='10'><tr><td>");

                print("<h1>$title</h1><hr />$content");
		
                print("</td></tr></table><br /><br />");


                print("<form method='POST'>
                <input type='hidden' name='action' value='confirmDelete'>
                <input type='hidden' name='id' value='$id'>
                <button name='s' value='editPage'>Confirm Deletion</button>
                ");

        #Finish deletion
        }elsif($action eq "confirmDelete"){
                my($id) = ($CGI->param('id'));
                $db_query = $db->prepare("DELETE FROM pages WHERE id='$id'");
                $db_query->execute();
                
                success("Page deleted!");
                $session->param("a","");
                admin();	



	}elsif($action eq "edit"){
        my @arr;
        my($id) = ($CGI->param('id'));
        $db_query = $db->prepare("SELECT title,content FROM pages WHERE id='$id'");
        $db_query->execute();
        @arr = $db_query->fetchrow_array();
        my($title,$content) = @arr;
        initEditor();
        print qq(
            <h3> Edit Page </h3><hr>
                    <form method='POST'>
                            <table border='0' class="admin-editTable">
                                    <tr>
                                            <td class="admin-td">Title:</td>
                        <td><input class='admin-input' type='text' name="title" value='$title'></td>
                                    </tr>
                                    <tr>
                                            <td valign='top'>Content:</td>
                        <td><textarea name="content" style="width:100%" id="area">$content</textarea></td>
                                    </tr>
                        <td></td>
                        <td>
                        <span align='right'><input type='hidden' name='id' value='$id'><input type='hidden' name='action' value='update'><button name='s' value='editPage'>Edit Page</button></span></td>
                                    </tr>
                            </table>
                    </form>
            <hr />
        );

	}elsif($action eq "update"){
		my($id) = ($CGI->param('id'));
                my($title, $content) = ($CGI->param('title'),$CGI->param('content'));

                $db_query = $db->prepare("UPDATE pages SET title=?, content=? WHERE id=?;");
                $db_query->execute($title,$content,$id);

                success("Post edited!");
                $session->param("a","");
                admin();	
	
	}elsif($action eq "yesHeader"){
		my($id) = ($CGI->param('id'));
     	$db_query = $db->prepare("UPDATE pages SET header='1' WHERE id='$id';");				
		$db_query->execute();
		managePages();
	}elsif($action eq "noHeader"){
		my($id) = ($CGI->param('id'));
     	$db_query = $db->prepare("UPDATE pages SET header='0' WHERE id='$id';");
		$db_query->execute();
		print($id).
		managePages();			
	}

	#Finish
    }
}

sub managePages{
    if($access >= 1){
        $db_query = $db->prepare("SELECT id,weight,title,date FROM pages WHERE header=1 ORDER BY weight ASC");

        $db_query->execute();

        my @arr;
        my @rows;
        my @headings = ("","ID","Title","Last Changed","Edit","Delete","Move");
        my @th_head = $CGI->th(\@headings);

        while(@arr = $db_query->fetchrow_array()){
                my($id,$weight,$title,$date) = @arr;
                $weight = "<div align='center'><a href='?id=$id&s=changeWeight&d=down&weight=$weight'><i class='icon-arrow-down'></i></a><a href='?id=$id&s=changeWeight&d=up&weight=$weight'><i class='icon-arrow-up'></i></a></div>";
				my $edit = "<a href='?id=$id&s=editPage&action=edit'>Edit</a>";
                my $delete = "<a href='?id=$id&s=editPage&action=delete'>Delete</a>";
                my $header = "<a href='?id=$id&s=editPage&action=noHeader'>Remove from header</a>";
                push(@rows, $CGI->td([$weight,$id,$title, $date, $edit, $delete, $header]));
        }
		
		print qq(<h1>Header Pages</h1>);
        print $CGI->table({-border=>1,-cellpadding=>3,-width=>'100%'});
        print $CGI->Tr((\@th_head));
        print $CGI->Tr((\@rows));
		print qq(</table>);
		undef(@arr);
		undef(@rows);
		undef(@headings);
		undef(@th_head);

        $db_query = $db->prepare("SELECT id,weight,title,date FROM pages WHERE header=0 ORDER BY weight ASC");
		$db_query->execute();
		
		@headings = ("","ID","Title","Last Changed","Edit","Delete","Move");
		@th_head = $CGI->th(\@headings);
		
        while(@arr = $db_query->fetchrow_array()){
                my($id,$weight,$title,$date) = @arr;
                $weight = "<div align='center'><a href='?id=$id&s=changeWeight&d=down&weight=$weight'><i class='icon-arrow-down'></i></a><a href='?id=$id&s=changeWeight&d=up&weight=$weight'><i class='icon-arrow-up'></i></a></div>";
				my $edit = "<a href='?id=$id&s=editPage&action=edit'>Edit</a>";
                my $delete = "<a href='?id=$id&s=editPage&action=delete'>Delete</a>";				
                my $header = "<a href='?id=$id&s=editPage&action=yesHeader'>Add to header</a>";
                push(@rows, $CGI->td([$weight,$id,$title, $date, $edit, $delete, $header]));
        }		
		
		print qq(<h1>Other Pages</h1>);
		print $CGI->table({-border=>1,-cellpadding=>3,-width=>'100%'});
		print $CGI->Tr((\@th_head));
		print $CGI->Tr((\@rows));
		print qq(</table>);	
    }
}

sub showPage{
	my $id = $CGI->param('id'); 
	my $db_query = $db->prepare("SELECT date, title, content FROM pages WHERE id='$id'");
	$db_query->execute();
	my($date, $title, $content) = $db_query->fetchrow_array();
	print("<h1> $title </h1><hr />");
	print("$content <br />");
	#print("$date");
}
sub initEditor{
    if($access >= 1){
        print qq(
	    <script type="text/javascript" src="http://js.nicedit.com/nicEdit-latest.js"></script> <script type="text/javascript">
	    bkLib.onDomLoaded(function() {
	    new nicEditor({fullPanel : true}).panelInstance('area');
	    });
	    </script>
        );
    }
}
