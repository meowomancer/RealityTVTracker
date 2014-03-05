=begin comment
pages.cgi

MODULE DESCRIPTION:
    Allows a user to flag a data entry with one of five issues.
    
MODULE SUBROUTINES
    flag(): Allows a user to flag a show that is in the show_data db table. User
            is provided with five options for why a entry should be reviewed.
            Once a choice is made, an entry is made in the admin_queue db table
            and an admin is alerted on their next log-in.
            

ELSEIF BLOCK
    #PUBLIC MODULE: flag.cgi
    elsif 	($s eq 'flag')			{ flag(); }
    
MISC
    Reasons for flagging
    | 1 -- Inaccurate or Mispelled Title
    | 2 -- Inaccurate year on air/program no longer airing
    | 3 -- Inaccurate category (ex, Duck Dynasty as competitive programming)
    | 4 -- Incorrect network
    | 5 -- Listing needs updating for other reason
=end comment
=cut



sub flag {
    my $a = $CGI->param('a');
    my $id = $CGI->param('id');
    
    if ($a eq "submit") {
        my $flagReason = $CGI->param('flagReason');
        if ($flagReason == "" || $flagReason eq "") {
            failure("No reason for flagging selected. Please try again.");
            $CGI->param('a',"");
            flag();
        }else{
            my $uid = $session->param("id");
            print ("Thank you for your flag. An administrator will review it shortly");
            my $db_query = $db->prepare("INSERT INTO admin_queue (user,type,entry,field,content) VALUES (?,?,?,?,?)");
            $db_query->execute($uid,"flag",$id,$flagReason,"");
        }
        
    }else{
        print qq(
            <h2>Reason for flagging:</h2>
            <form><fieldset>
                <input type="radio" name="flagReason" value="1" style="vertical-align: middle; margin: 0px;"> Inaccurate or misspelled title<br><br>
                <input type="radio" name="flagReason" value="2" style="vertical-align: middle; margin: 0px;"> Inaccurate year on air <em>or</em> program no longer airing<br><br>
                <input type="radio" name="flagReason" value="3" style="vertical-align: middle; margin: 0px;"> Inaccurate category <em>ex: Duck Dynasty listed as competitive programming</em><br><br>
                <input type="radio" name="flagReason" value="4" style="vertical-align: middle; margin: 0px;"> Incorrect network<br><br>
                <input type="radio" name="flagReason" value="5" style="vertical-align: middle; margin: 0px;"> Listing needs updating for other reasons<br>
                <input type="hidden" name="id" value="$id">
                <input type="hidden" name="a" value="submit">
                <input type="hidden" name="s" value="flag">
                <button>Flag</button>
            </fieldset></form>
        );
    }
}