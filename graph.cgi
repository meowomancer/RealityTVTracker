use GD::Graph::lines;
use GD::Graph::colour qw( :files );

sub graph{
    my $thisYear = 2013;
    my $minYear;
    my $a = $CGI->param('a');

    $db_query = $db->prepare("SELECT MIN(start_date) FROM show_data");
    $db_query->execute();
    @arr = $db_query->fetchrow_array;
    my $minYear = $arr[0];
    
    #STEP 2 --> SELECT INFORMATION
    if ($a eq "step2") {
        print qq(<h1>Create a Graph</h1>);    
        
        my $type = $CGI->param('type');
        if ($type eq "network") {
            my $options = "";
            my @arr;
            my $yearOptions = qq(<option value="null" selected> </option>);
            
            for(my $i = 2013; $i > $minYear; $i--){
                $yearOptions .= qq(<option value="$i">$i</option>);
            }
            
            
            $db_query = $db->prepare("SELECT DISTINCT network FROM show_data");
            $db_query->execute();
            
            while (@arr = $db_query->fetchrow_array) {
                $options = $options.qq(<option value=").$arr[0].qq(">).$arr[0].qq(</option>);
            }
            
            print qq(
                <h3>Step 2 of 3 - Network Graph</h3>
                <form><table><fieldset>
                    <tr><td colspan=2 style="padding-left:125px;padding-right:125px;">
                    <label>Network</label>
                    <select name="network">
                    $options
                    </select>
                    </td></tr>
                    <tr>
                        <td style="padding-left:125px;padding-right:125px;">
                        <label>Start Year</label>
                        <select name="startYear">
                        $yearOptions
                        </select>
                        </td>

                        <td style="padding-left:125px;padding-right:125px;">
                        <label>End Year</label>
                        <select name="endYear">
                        $yearOptions
                        </select>
                        </td>
                    </tr>
                    <tr><td colspan=2 style="padding-left:125px;padding-right:125px;">
                    <input type="hidden" name="type" value="$type">
                    <input type="hidden" name="s" value="graph">
                    <input type="hidden" name="a" value="step3">
                    <button>Generate Graph</button>
                    </td></tr>
                </fieldset></table></form>
            );
        }
        elsif ($type eq "genre"){
            my $options = "";
            my @arr;
            my $yearOptions = qq(<option value="null" selected> </option>);
            
            for(my $i = 2013; $i > $minYear; $i--){
                $yearOptions .= qq(<option value="$i">$i</option>);
            }
            
            
            $db_query = $db->prepare("SELECT DISTINCT genre FROM show_data");
            $db_query->execute();
            
            while (@arr = $db_query->fetchrow_array) {
                $options = $options.qq(<option value=").$arr[0].qq(">).$arr[0].qq(</option>);
            }
            
            print qq(
                <h3>Step 2 of 3 - Genre Graph</h3>
                <form><table><fieldset>
                    <tr><td colspan=2 style="padding-left:125px;padding-right:125px;">
                    <label>Genre</label>
                    <select name="genre">
                    $options
                    </select>
                    </td></tr>
                    <tr>
                        <td style="padding-left:125px;padding-right:125px;">
                        <label>Start Year</label>
                        <select name="startYear">
                        $yearOptions
                        </select>
                        </td>

                        <td style="padding-left:125px;padding-right:125px;">
                        <label>End Year</label>
                        <select name="endYear">
                        $yearOptions
                        </select>
                        </td>
                    </tr>
                    <tr><td colspan=2 style="padding-left:125px;padding-right:125px;">
                    <input type="hidden" name="type" value="$type">
                    <input type="hidden" name="s" value="graph">
                    <input type="hidden" name="a" value="step3">
                    <button>Generate Graph</button>
                    </td></tr>
                </fieldset></table></form>
            );
            
        }
        elsif ($type eq "netgen"){
            my $networkOptions = "";
            my $genreOptions = "";
            my @arr;
            my $yearOptions = qq(<option value="null" selected> </option>);
            
            for(my $i = 2013; $i > $minYear; $i--){
                $yearOptions .= qq(<option value="$i">$i</option>);
            }
		    
            $db_query = $db->prepare("SELECT DISTINCT genre FROM show_data");
            $db_query->execute();
            
            while (@arr = $db_query->fetchrow_array) {
                $genreOptions = $genreOptions.qq(<option value=").$arr[0].qq(">).$arr[0].qq(</option>);
            }
            
			$db_query = $db->prepare("SELECT DISTINCT network FROM show_data");
            $db_query->execute();
            
            while (@arr = $db_query->fetchrow_array) {
                $networkOptions = $networkOptions.qq(<option value=").$arr[0].qq(">).$arr[0].qq(</option>);
            }
			
            print qq(
                <h3>Step 2 of 3 - Network/Genre Graph</h3>
                <form><table><fieldset><tr>
					<td style="padding-left:125px;padding-right:125px;">
						<label>Network</label>
						<select name="network">
						$networkOptions
						</select>
					</td>
					<td style="padding-left:125px;padding-right:125px;">
						<label>Genre</label>
						<select name="genre">
						$genreOptions
						</select>
                    </td></tr>
                    <tr>
                        <td style="padding-left:125px;padding-right:125px;">
                        <label>Start Year</label>
                        <select name="startYear">
                        $yearOptions
                        </select>
                        </td>

                        <td style="padding-left:125px;padding-right:125px;">
                        <label>End Year</label>
                        <select name="endYear">
                        $yearOptions
                        </select>
                        </td>
                    </tr>
                    <tr><td colspan=2 style="padding-left:125px;padding-right:125px;">
                    <input type="hidden" name="type" value="$type">
                    <input type="hidden" name="s" value="graph">
                    <input type="hidden" name="a" value="step3">
                    <button>Generate Graph</button>
                    </td></tr>
                </fieldset></table></form>
            );
        }
        else{
            
        }
    }
    
    #STEP 3 --> GENERATE GRAPH
    elsif ($a eq "step3") {
        print qq(<h1>Create a Graph</h1>);
        #Params
        my $type = $CGI->param('type');
        my $startYear = $CGI->param('startYear');
        my $endYear = $CGI->param('endYear');
        my $fileName;
        my $png;
        my %data;
        my @arr; 
        my @years;
        my @values;
        my @graphData;
        
        #Fix year if fubar
        if ($endYear < $startYear) {my $tmp = $startYear;$startYear = $endYear;$endYear = $tmp;}
        
        #Generate random filename
		my @chars = ("a","b","c","d","e","f","1","2","3","4","5","6","7","8","9","0");
		for(my $i = 0; $i < 9; $i++){
			$fileName .= $chars[rand @chars];		
        }
        $png = $fileName;
        $fileName .= ".png";
        $fileName = "./graphs/".$fileName;
        
        #Print loading message
        print qq(
            <h3>Step 3 of 3</h3>
            <div align="center" style="width:50%;margin-left:auto;margin-right:auto">
            Generating a $type graph for $network from $startYear to $endYear
            <div class="progress progress-striped active">
            <div class="bar" style="width: 100%;"></div>
            </div>
        );
        
        if ($type eq "network") {
            my $network = $CGI->param('network');
            
            #Calculate number of shows for each year for network;
            #Init hash
            for(my $i = $minYear; $i < $thisYear; $i++){
                $data{$i} = 0;
            }
            
            $db_query = $db->prepare("SELECT start_date, end_date FROM show_data WHERE network = ?");
            $db_query->execute($network);
            
            while (@arr = $db_query->fetchrow_array) {
                my ($start, $end) = ($arr[0],$arr[1]);
                if ($end == -1) {$end = $thisYear;}
                
                for(my $j = $start; $j<$end; $j++){
                    $data{$j}++;
                }
                
            }
            
            
            #Prepare Graph Data
            for(my $i = $startYear; $i <= $endYear; $i++){
                #print qq(<br />$i = ).$data{$i};
                push(@years, $i);
                push(@values, $data{$i});
            }

            #Generate graph
            push(@graphData, [@years]);
            push(@graphData, [@values]);
            my $mygraph1 = GD::Graph::lines->new(750, 450);
            my $skip;
            my $diffYear = $endYear - $startYear;
            
            $mygraph1->set(
                    x_label     => 'Year',
                    y_label     => 'Number of shows',
                    title       => qq(Reality TV shows on $network from $startYear to $endYear),
                    x_label_skip => 1,
                    dclrs	    => [ qw(orange blue purple
                                    green black red dgreen
                                    dblue dpurple dred
                                    lorange lblue lpurple lred lgreen) ],
            ) or warn $mygraph1->error;
            my $graph = $mygraph1->plot(\@graphData) or die $mygraph1->error;
            open(IMG, '>', $fileName) or die $!;
            binmode IMG;
            print IMG $graph->png or die $!;
            
            #Forward to final page
            print qq(
                <script>window.location = "?s=graph&a=step4&png=$png";</script>
            );
        }
        
        elsif ($type eq "genre"){
            print qq(<h3>Step 3 of 3 - Genre Graph</h3>);
            my $genre = $CGI->param('genre');
            
            #Calculate number of shows for each year for network;
            #Init hash
            for(my $i = $minYear; $i < $thisYear; $i++){
                $data{$i} = 0;
            }
            
            $db_query = $db->prepare("SELECT start_date, end_date FROM show_data WHERE genre = ?");
            $db_query->execute($genre);
            
            while (@arr = $db_query->fetchrow_array) {
                my ($start, $end) = ($arr[0],$arr[1]);
                if ($end == -1) {$end = $thisYear;}
                
                for(my $j = $start; $j<$end; $j++){
                    $data{$j}++;
                }
                
            }
            
            
            #Prepare Graph Data
            for(my $i = $startYear; $i <= $endYear; $i++){
                #print qq(<br />$i = ).$data{$i};
                push(@years, $i);
                push(@values, $data{$i});
            }

            #Generate graph
            push(@graphData, [@years]);
            push(@graphData, [@values]);
            my $mygraph1 = GD::Graph::lines->new(750, 450);
            $mygraph1->set(
                    x_label     => 'Year',
                    y_label     => 'Number of shows',
                    title       => qq(Reality TV shows of genre $genre from $startYear to $endYear),
                    dclrs	    => [ qw(orange blue purple
                                    green black red dgreen
                                    dblue dpurple dred
                                    lorange lblue lpurple lred lgreen) ]	
            ) or warn $mygraph1->error;
            my $graph = $mygraph1->plot(\@graphData) or die $mygraph1->error;
            open(IMG, '>', $fileName) or die $!;
            binmode IMG;
            print IMG $graph->png or die $!;
            
            #Forward to final page
            print qq(
                <script>window.location = "?s=graph&a=step4&png=$png";</script>
            );
            
        }
        
        elsif ($type eq "netgen"){
			print qq(<h3>Step 3 of 3 - Network/Genre Graph</h3>);
            my $genre = $CGI->param('genre');
            my $network = $CGI->param('network');
			
            #Calculate number of shows for each year for network;
            #Init hash
            for(my $i = $minYear; $i < $thisYear; $i++){
                $data{$i} = 0;
            }
            
            $db_query = $db->prepare("SELECT start_date, end_date FROM show_data WHERE genre = ? AND network = ?");
            $db_query->execute($genre,$network);
            
            while (@arr = $db_query->fetchrow_array) {
                my ($start, $end) = ($arr[0],$arr[1]);
                if ($end == -1) {$end = $thisYear;}
                
                for(my $j = $start; $j<$end; $j++){
                    $data{$j}++;
                }
                
            }
            
            
            #Prepare Graph Data
            for(my $i = $startYear; $i <= $endYear; $i++){
                #print qq(<br />$i = ).$data{$i};
                push(@years, $i);
                push(@values, $data{$i});
            }

            #Generate graph
            push(@graphData, [@years]);
            push(@graphData, [@values]);
            my $mygraph1 = GD::Graph::lines->new(750, 450);
            $mygraph1->set(
                    x_label     => 'Year',
                    y_label     => 'Number of shows',
                    title       => qq(Reality TV shows of genre $genre on $network from $startYear to $endYear),
                    dclrs	    => [ qw(orange blue purple
                                    green black red dgreen
                                    dblue dpurple dred
                                    lorange lblue lpurple lred lgreen) ]	
            ) or warn $mygraph1->error;
            my $graph = $mygraph1->plot(\@graphData) or die $mygraph1->error;
            open(IMG, '>', $fileName) or die $!;
            binmode IMG;
            print IMG $graph->png or die $!;
            
            #Forward to final page
            print qq(
                <script>window.location = "?s=graph&a=step4&png=$png";</script>
            );
            
        }
        
    }
    
    #STEP 4 --> DISPLAY GRAPH
    elsif ($a eq "step4"){
        my $png = $CGI->param('png');
        print qq(<h1>Create a Graph</h1>);
        print qq(<div align="center"><img src=".\/graphs\/$png.png"></div>);
        print qq(<a href="?s=search">Return to Search</a> or <a href="?s=graph">generate another graph</a>);
    }
    
    #STEP 1 --> CHOSE TYPE OF GRAPH
    else{ 
        print qq(
            <h1>Create a Graph</h1>
            <h3>Step 1 of 3</h3>
            Please select the type of graph you would like to generate
            <h4 style="margin-bottom:0px"><a href="?s=graph&a=step2&type=network">Network</a></h4>
            Graph the number of reality TV shows on a given network over a set time range.
            <h4 style="margin-bottom:0px"><a href="?s=graph&a=step2&type=genre">Genre</a></h4>
            Graph the number of reality TV shows of a given genre over all networks against a set time range.
            <h4 style="margin-bottom:0px"><a href="?s=graph&a=step2&type=netgen">Network/Genre</a></h4>
            Graph the number of reality TV shows of a given genre over a specific network against a set time range.
        );
    }
    
}