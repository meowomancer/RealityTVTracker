=begin comment
layout.cgi

MODULE DESCRIPTION:
		Provides the methods that prepare the website manager (index.cgi) to
		properly display HTML as well as creates the layout containers, fills
		in the header, fills in the footer, and closes the layout containers. 

MODULE SUBROUTINES
		start(): Sends all header information to render the page as an HTML
		         document and prints the header
		
		end(): Prints the footer and then closes all layout and HTML tags in
		       order to comply with HTML design standards
=end comment
=cut


sub start {
	$CGI->header();
	print $session->header();
	my $access = $session->param('access');
	
	my($title,$siteName)= ("RealityTVData.org", "Reality TV Data");
	
	
	print qq(
		<!DOCTYPE html>
		<html lang="en">
		  <head>
		    <meta charset="utf-8">
		    <title>$title</title>
		    <meta name="viewport" content="width=device-width, initial-scale=1.0">
		    <meta name="description" content="">
		    <meta name="author" conteant="">

		    <!-- The styles -->
		    <link href="./assets/css/bootstrap.css" rel="stylesheet">
		    <link href="./assets/css/datepicker.css" rel="stylesheet">
			<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		    <link href="./assets/css/style.css" rel="stylesheet">
		    <style type="text/css">
				body {
					padding-top: 60px;
					padding-bottom: 40px;
				}
				.sidebar-nav {
					padding: 9px 0;
				}
				
				\@media (max-width: 980px) {
					/* Enable use of floated navbar text */
					.navbar-text.pull-right {
						float: none;
						padding-left: 5px;
						padding-right: 5px;
					}
				}
				$CSS
		    </style>
		    <link href="./assets/css/bootstrap-responsive.css" rel="stylesheet">
			
		    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
		    <!--[if lt IE 9]>
		      <script src="./assets/js/html5shiv.js"></script>
		    <![endif]-->
			
		    <!-- Fav and touch icons -->
		    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="../assets/ico/apple-touch-icon-144-precomposed.png">
		    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="../assets/ico/apple-touch-icon-114-precomposed.png">
		    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="../assets/ico/apple-touch-icon-72-precomposed.png">
			<link rel="apple-touch-icon-precomposed" href="../assets/ico/apple-touch-icon-57-precomposed.png">
			<link rel="shortcut icon" href="../assets/ico/favicon.png">
			<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
			<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
			
			<script>
			\$(function() {
			\$( "#datepicker" ).datepicker();
			\$( "#datepicker2" ).datepicker();
			});
			</script>
						   
		  </head>
			
		  <body>
			
		    <div class="navbar navbar-inverse navbar-fixed-top">
		      <div class="navbar-inner">
			  <div class="container">
			<div class="container-fluid">
			  <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
			    <span class="icon-bar"></span>
			    <span class="icon-bar"></span>
			    <span class="icon-bar"></span>
			  </button>
			  <a class="brand" href="index.cgi">$siteName</a>

			  <div class="nav-collapse collapse">

			    <p class="navbar-text pull-right">);
				if ($access >= 1) {
					print qq([<a href="?s=admin">Administrator Control Pannel</a>] )
				}
				
				if(defined $session->param("name")){print qq([<a href="?s=cpw">Change Password</a>] [<a href="?s=lo">Logout</a>])}
				else{print qq([<a href="?s=l">Login</a>])}
			    print qq(</p>

			    <ul class="nav">
				);

				$db_query = $db->prepare("SELECT title, id FROM pages WHERE header=1 ORDER BY weight ASC");
				$db_query->execute();
				
				my @arr;
				
				while(@arr = $db_query->fetchrow_array()){
					my($title, $id) = @arr;
					print("<li><a href=\"?s=showPage&id=$id\">$title</a></li>");
				}
			print qq(
			    </ul>
			  </div><!--/.nav-collapse -->
		       </div>
		      </div>
		    </div>
			</div>
			<div class="container">
		    <div class="container-fluid">
		      <div class="row-fluid">
			<div class="span13"><!-- content -->

	);
}

sub end {
	print qq(
					</div>
				</div><!-- /content -->
			</div> <!-- /container -->
			<div id="footer" style="padding-top:150px">
				<div class="container">
					<p align="right" class="muted credit"><a href="?s=credits">Credits</a></p>
				</div>
			</div>

		    <script src='./assets/js/jquery.js'></script>
		    <script src='./assets/js/bootstrap.js'></script>
			<script src='./assets/js/bootstrap-datepicker.js'></script>
			<script src='http://code.jquery.com/ui/1.10.3/jquery-ui.js'></script>
		    <!--
		    <script src='./assets/js/bootstrap-transition.js'></script>
		    <script src='./assets/js/bootstrap-alert.js'></script>
		    <script src='./assets/js/bootstrap-modal.js'></script>
		    <script src='./assets/js/bootstrap-dropdown.js'></script>
		    <script src='./assets/js/bootstrap-scrollspy.js'></script>
		    <script src='./assets/js/bootstrap-tab.js'></script>
		    <script src='./assets/js/bootstrap-tooltip.js'></script>
		    <script src='./assets/js/bootstrap-popover.js'></script>
		    <script src='./assets/js/bootstrap-button.js'></script>
		    <script src='./assets/js/bootstrap-collapse.js'></script>
		    <script src='./assets/js/bootstrap-carousel.js'></script>
		    <script src='./assets/js/bootstrap-typeahead.js'></script>
		    -->

  		    </body>
		    </html>);
	print $CGI->end_html();
	exit;
}
