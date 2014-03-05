=begin comment
user.cgi

MODULE DESCRIPTION:
		user.cgi manages the functions of registering for access to the website,
		logging into the website, setting cookie values on login, logging out,
		changing user password, and resetting forgotten passwords.
		
		Also contains the admin functions for managing users: allowing an admin
		to create users, delete users, and add and remove admin privledges from
		existing users
		
MODULE SUBROUTINES
		login(): Allows a user to login to the website. Set user's cookie on a
				 successful login
				 
		register(): Allows a user to register for the website. Encrypts password
				    and creates a salt before adding user to the database. Also
					sets user's non-unique UID and unique ID.
					
		logout(): Logs the user out by deleting any cookies associated with the
				  system
				  
		forgotPassword(): Dispatches an e-mail to the user with a link to the
						  rest of the password reset process. 
						  
		resetPassword(): Allows a user to reset their password after requesting
						 a password reset. Updates the db with a new password
						 hash and salt on success
						 
		changePassword(): Allows a currently logged in user to reset their
						  password. Updates the db with a new password hash and
						  salt on success
		
		manageUsers(): Allows an administrator to view all current users and
				       their associated data. From here an admin can create and
					   delete existing users as well as grant and remove admin
					   privledges. Also contains the actual code for creating a
					   new user as an admin.
					   
		deleteUser(): Asks the administrator for confirmation for deleting the
				      selected user, then removes their information from the
					  database
					  
		makeUser(): Allows an administrator to demote a user from admin
		
		makeAdmin(): Allows an administator to promote a user to admin

ELSEIF BLOCK
		+------------+
		| USER LEVEL |
		+------------+
		#PUBLIC MODULE: user.cgi
		elsif   ($s eq 'l')     		{ login();  }
		elsif   ($s eq 'r')     		{ register();  }
		elsif   ($s eq 'lo')    		{ logout();  }
		elsif	($s eq 'f')				{ forgotPassword();}
		elsif	($s eq 'reset')			{ resetPassword();}
		elsif	($s eq 'cpw')			{ changePassword();}
		
		+-------------+
		| ADMIN LEVEL |
		+-------------+
		#ADMIN MODULE: user.cgi
		elsif	($s eq "manageUsers")	{ manageUsers(); }
		elsif	($s eq "deleteUser")	{ deleteUser(); }
		elsif	($s eq "makeUser")		{ makeUser(); }
		elsif	($s eq "makeAdmin")		{ makeAdmin(); }
=end comment
=cut


use Mail::Sendmail;

sub login{
	my $a = $CGI->param('a');
	if($a eq "submit" && $_[0] ne "new"){
		my $db_query;
		my $username = $CGI->param('username');
		my $password = $CGI->param('password');
		my $salt = sha384_hex($password);
		my $passwordsalt = $password.$salt;
		my $password = sha384_hex($passwordsalt);
		
		$db_query = $db->prepare("SELECT password, access, id FROM users WHERE username=?");		
		$db_query->execute($username);
		
		my @arr = $db_query->fetchrow_array();
		
		my ($dbPassword, $access, $id) = @arr;
		
		if($password eq $dbPassword){
			$session->param('name', $username);
			$session->param('access', $access);
			$session->param('id', $id);
			$session->param('book', 1);
			print qq(<script>window.location.replace("?s=m");</script>);
		}else{
			print qq(<div class="alert alert-error">Incorrect username or password.</div>);
			print qq(<h1>Login</h1>);
			print qq(
				Don't have an account? <a href="?s=r">Register for one!</a><br />
				Forgot your password? <a href="?s=f">Click here.</a><br /><br />
				<form action="index.cgi" method="post">
					Username:<br />
					<input type="text" name="username" /><br />
					Password:<br />
					<input type="password" name="password" />
					<input type="hidden" name="s" value="l">
					<br />
					<input type="hidden" name="a" value="submit">
					<button>Log In</button>
				</form>
			);
		}
	}else{
		print qq(<h1>Login</h1>);
		print qq(
			Don't have an account? <a href="?s=r">Register for one!</a><br />
				Forgot your password? <a href="?s=f">Click here.</a><br /><br />
			<form action="index.cgi" method="post">
				Username:<br />
				<input type="text" name="username" /><br />
				Password:<br />
				<input type="password" name="password" />
				<input type="hidden" name="s" value="l">
				<br />
				<input type="hidden" name="a" value="submit">
				<button>Log In</button>
			</form>
		);
	}
}
sub register{
	my $a = $CGI->param('a');
	if($a eq "submit"){
		my $username = $CGI->param('username');
		my $password = $CGI->param('password');
		my $passwordConfirm = $CGI->param('passwordConfirm');
		my $email = $CGI->param('email');
		my $fName = $CGI->param('fName');
		my $lName = $CGI->param('lName');
				
		$db_query = $db->prepare("SELECT COUNT(*) FROM users WHERE username = ?");
		$db_query->execute($username);
		my $queryResult = $db_query->fetchrow_array();
		
		my $error = 0;
		
		if ($queryResult > 0){failure("Username already in use.");$error = 1}
		if (length($username)<6 || $username>24) {failure(qq(Username must be between 6 and 24 characters long));$error = 1}
		if ($username =~ /([^A-Za-z0-9]+)$/){failure(qq(Username may only contain letters, numbers, and underscores));$error = 1}

		if (length($password)<6 || $username>24) {failure(qq(Password must be between 6 and 24 characters long));$error = 1}
		if ($password =~ /([^A-Za-z0-9!@#$%^&* \_\-. ]+)$/){failure(qq(Password may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."));$error = 1}
		if ($password ne $passwordConfirm){failure(qq(Passwords do not match));$error=1}
		
		
		
		if (!$error) {
			my $salt = sha384_hex($password);
			my $passwordsalt = $password.$salt;
			my $password = sha384_hex($passwordsalt);
			
			my $range = 999999999;
			my $minimum = 100000000;
			
			my $uid = int(rand($range)) + $minimum;
			
			$db_query = $db->prepare("INSERT INTO users (username, password, salt, uid, email, firstName, lastName) VALUES (?, ?, ?, ?, ?, ?, ?);");
			$db_query->execute($username,$password,$salt,$uid,$email,$fName,$lName);
			
			success("Account created! Please login below");
			$CGI->param('password',"");
			$CGI->param('username',"");
			$CGI->param('passwordConfirm',"");
			login("new");
		}else{
			$CGI->param('a',"null");
			register("$username");
		}
	}else{
		print qq(<h1>Register</h1>);
		print qq(
			<form action="index.cgi" method="post">
				<fieldset>
				<label><strong>Username</strong><br><small>Must be 6 - 24 characters and may only contain letters, numbers, and underscores</small></label>
				<input type="text" name="username" value="$_"/><br /><hr />
				<label><strong>Password</strong><br><small>Must be 6 - 24 characters and may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."</small></label>
				<input type="password" name="password" />
				<label><strong>Confirm Password</strong></label>
				<input type="password" name="passwordConfirm" /><hr />
				<label><strong>E-Mail Address</strong><br><small>Your email address is not required, but you will be unable to reset your password without it.</small></label>
				<input type="text" name="email" value=""/><br /><hr />
				<label><strong>First Name</strong><br><small>Optional</small></label>
				<input type="text" name="fName" value=""/><br />
				<label><strong>Last Name</strong><br><small>Optional</small></label>
				<input type="text" name="lName" value=""/><br />
				<input type="hidden" name="s" value="r">
				<input type="hidden" name="a" value="submit"><br />
				<button type="submit" class="btn">Register</button>

				</fieldset>
			</form>
		);
	}
}

sub logout{
	$session->delete();
	$session->flush();
	print qq(<script>window.location.replace("?s=m");</script>);
}

sub forgotPassword{
	my $a = $CGI->param("a");
	if ($a eq "submit") {
		my $email = $CGI->param('email');
		$db_query = $db->prepare("SELECT password FROM users WHERE email=?");
		$db_query->execute($email);
		my @arr = $db_query->fetchrow_array;
		if($arr[0] eq '' || $email eq ""){
			failure("Sorry, no account with an e-mail matching the provided e-mail could be found or no e-mail address was provided. Please try again");
			$CGI->param("a","");
			forgotPassword();
		}else{
			my $hash = $arr[0];
			my $message = qq(
		<html>Hello,<br><br>To reset your password, please visit the following URL.<br><br><a href="$url?s=reset&key=$hash">$url?s=reset&key=$hash</a></html>
			);
			%mail = (
				To      => $email,
				From    => 'noreply@r0b0tic.com',
				Subject => 'Your password reset request',
				'content-type' => 'text/html; charset="iso-8859-1"',
				Message => $message,
			);
			
			sendmail(%mail) or die $Mail::Sendmail::error;
			success("An e-mail containing a link to reset you password has been dispatched. Please check your e-mail for it.");
			search();
		}
		
	}
	
	else{
		print qq(
			<h1>Forgot Password</h1>
			Please enter the e-mail address associated with your account below. If you did not register with an e-mail address, you will be unable to recover your password.<br /><br />
			<form>
			<input type="text" name="email"><br /><br />
			<input type="hidden" name="s" value="f">
			<input type="hidden" name="a" value="submit">
			<button>Reset Password</button>
			</form>
		)
	}
}
sub resetPassword{
	my $hash = $CGI->param('key');
	my $a = $CGI->param('a');
	if ($hash ne "") {
		if ($a eq "reset") {
			my $password = $CGI->param('password');
			my $passwordConfirm = $CGI->param('passwordConfirm');
			if ($password ne $passwordConfirm){failure(qq(Passwords do not match, please try again));$error=1}
			if (!$error) {
				my $salt = sha384_hex($password);
				my $passwordsalt = $password.$salt;
				my $password = sha384_hex($passwordsalt);
				$db_query = $db->prepare(qq(UPDATE users SET password=?, salt=? WHERE password=?));
				$db_query->execute($password,$salt,$hash);
				$CGI->param('password',"");
				$CGI->param('username',"");
				$CGI->param('passwordConfirm',"");
				success("Your password has been reset. Please login below");
				login("new");
			}else{
				$CGI->param("a","");
				resetPassword();
			}
			
		}
		else{
		print qq(
			<h1>Password Reset</h1>
				<form method="GET"><fieldset>
					<label><strong>New Password</strong><br><small>Must be 6 - 24 characters and may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."</small></label>
					<input type="password" name="password" />
					<label><strong>Confirm New Password</strong></label>
					<input type="password" name="passwordConfirm" />
					<input type="hidden" name="key" value="$hash">
					<input type="hidden" name="s" value="reset">
					<input type="hidden" name="a" value="reset">
					<button>Reset Password</button>
				</fieldset></form>
			);
		}
	}else{
		search();
	}
	
}
sub changePassword{
	my $a = $CGI->param('a');
	if ($a eq "reset") {
		my $password = $CGI->param('password');
		my $passwordConfirm = $CGI->param('passwordConfirm');
		
		if (length($password)<6 || $username>24) {failure(qq(Password must be between 6 and 24 characters long));$error = 1}
		if ($password =~ /([^A-Za-z0-9!@#$%^&* \_\-. ]+)$/){failure(qq(Password may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."));$error = 1}
		if ($password ne $passwordConfirm){failure(qq(Passwords do not match));$error=1}
		
		if (!$error) {
			my $salt = sha384_hex($password);
			my $passwordsalt = $password.$salt;
			my $password = sha384_hex($passwordsalt);
			
			#$db_query = $db->prepare("INSERT INTO users (username, password, salt, uid, email, firstName, lastName) VALUES (?, ?, ?, ?, ?, ?, ?);");
			#$db_query->execute($username,$password,$salt,$uid,$email,$fName,$lName);
			
			$db_query = $db->prepare("UPDATE users SET password=?, salt=? WHERE username=?");
			$db_query->execute($password, $salt, $session->param('name'));
			
			$CGI->param('password',"");
			$CGI->param('username',"");
			$CGI->param('passwordConfirm',"");

			success("Password changed");
			search();
		}else{
			$CGI->param('a', "submit");
			changePassword();
		}
		

	}elsif ($a eq "submit"){
		my $db_query;
		my $username = $session->param('name');
		my $password = $CGI->param('password');
		my $salt = sha384_hex($password);
		my $passwordsalt = $password.$salt;
		my $password = sha384_hex($passwordsalt);
		
		$db_query = $db->prepare("SELECT password, access, id FROM users WHERE username=?");		
		$db_query->execute($username);
		
		my @arr = $db_query->fetchrow_array();
		
		my ($dbPassword, $access, $id) = @arr;
		
		if($password eq $dbPassword){
				print qq(
						<h1>Change Password</h1>
						<form action="index.cgi" method="post">
						Please enter your new password:<br />
						<input type="password" name="password" />
						Please confirm your new password:<br />
						<input type="password" name="passwordConfirm" />
						<input type="hidden" name="a" value="reset">
						<input type="hidden" name="s" value="cpw">
						<br />
						<button>Change Password</button>
						</form>
				);
				
		}else{
				failure("Password is incorrect");
				$CGI->param('a',"");
				changePassword();
		}
	}else{
		print qq(<h1>Change Password</h1>);
		print qq(
			<form action="index.cgi" method="post">
				Please enter your current password:<br />
				<input type="password" name="password" />
				<input type="hidden" name="a" value="submit">
				<input type="hidden" name="s" value="cpw">
				<br />
				<button>Change Password</button>
			</form>
				
		);
	}
	
}

=comment
Admin methods
=end
=cut
sub manageUsers{
	if($session->param("access")>=1){
		$a = $CGI->param("a");
		if($a eq "main" || not defined $a){
			print qq(<h3><a href="?s=manageUsers&a=add">Add User</a></h3>);
			$db_query = $db->prepare("SELECT id, username, firstName, lastName, email, access FROM users;");
			$db_query->execute();
			
			my @arr;
			my @rows;
			my @headings = ("Username","First Name","Last Name","Email","Access");
			my @th_head = $CGI->th(\@headings);
			
			while(@arr = $db_query->fetchrow_array()){
				my($id,$username,$firstName,$lastName,$email,$access) = @arr;
				
				my $deleteLink = qq(<a onclick="window.open('?s=deleteUser&id=$id', 'newwindow', 'width=320, height=320px'); return false;">Delete</a>);
				my $changeLink = "";
				
				if($access >= 1){
					$access = "Admin";
					$changeLink = qq(<a href="?s=makeUser&id=$id">Remove Admin</a>);
				}
				elsif($access == 0){
					$access = "User";
					$changeLink = qq(<a href="?s=makeAdmin&id=$id">Make Admin</a>);
				}
				
				
				push(@rows, $CGI->td([$username,$firstName,$lastName,$email,$access,$changeLink,$deleteLink]));
			}
			
			print $CGI->table({-border=>1,-cellpadding=>3,-width=>'100%'});
			print $CGI->Tr((\@th_head));
			print $CGI->Tr((\@rows));
		}elsif($a eq "add"){
			print qq(<h1>Create new user</h1>);
					print qq(
						<form action="index.cgi" method="post">
							<fieldset>
							<label><strong>Username</strong><br><small>Must be 6 - 24 characters and may only contain letters, numbers, and underscores</small></label>
							<input type="text" name="username" value="$_"/><br /><hr />
							<label><strong>Password</strong><br><small>Must be 6 - 24 characters and may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."</small></label>
							<input type="password" name="password" />
							<label><strong>Confirm Password</strong></label>
							<input type="password" name="passwordConfirm" /><hr />
							<label><strong>E-Mail Address</strong><br><small>Your email address is not required, but you will be unable to reset your password without it.</small></label>
							<input type="text" name="email" value=""/><br /><hr />
							<label><strong>First Name</strong><br><small>Optional</small></label>
							<input type="text" name="fName" value=""/><br />
							<label><strong>Last Name</strong><br><small>Optional</small></label>
							<input type="text" name="lName" value=""/><br />
							<input type="hidden" name="s" value="manageUsers">
							<input type="hidden" name="a" value="submit"><br />
							<button type="submit" class="btn">Create User</button>
							</fieldset>
						</form>
					);
		}elsif($a eq "submit"){
			my $username = $CGI->param('username');
			my $password = $CGI->param('password');
			my $passwordConfirm = $CGI->param('passwordConfirm');
			my $email = $CGI->param('email');
			my $fName = $CGI->param('fName');
			my $lName = $CGI->param('lName');
			
			
			$db_query = $db->prepare("SELECT COUNT(*) FROM users WHERE username = ?");
			$db_query->execute($username);
			my $queryResult = $db_query->fetchrow_array();
			
			my $error = 0;
			
			if ($queryResult > 0){failure("Username already in use.");$error = 1}
			if (length($username)<6 || $username>24) {failure(qq(Username must be between 6 and 24 characters long));$error = 1}
			if ($username =~ /([^A-Za-z0-9]+)$/){failure(qq(Username may only contain letters, numbers, and underscores));$error = 1}
	
			if (length($password)<6 || $username>24) {failure(qq(Password must be between 6 and 24 characters long));$error = 1}
			if ($password =~ /([^A-Za-z0-9!@#$%^&* \_\-. ]+)$/){failure(qq(Password may only contain letters, numbers, spaces, and the symbols "! @ # $ % ^ & * _ - ."));$error = 1}
			if ($password ne $passwordConfirm){failure(qq(Passwords do not match));$error=1}
			
			
			
			if (!$error) {
				my $salt = sha384_hex($password);
				my $passwordsalt = $password.$salt;
				my $password = sha384_hex($passwordsalt);
				
				my $range = 999999999;
				my $minimum = 100000000;
				
				my $uid = int(rand($range)) + $minimum;
				
				$db_query = $db->prepare("INSERT INTO users (username, password, salt, uid, email, firstName, lastName) VALUES (?, ?, ?, ?, ?, ?, ?);");
				$db_query->execute($username,$password,$salt,$uid,$email,$fName,$lName);
				
				success("Account created!");
				$CGI->param('password',"");
				$CGI->param('username',"");
				$CGI->param('passwordConfirm',"");
				$CGI->param('a',"main");
				manageUsers();
			}else{
				$CGI->param('a',"main");
				manageUsers("$username");
			}
		}
	}else{
		print("Sorry, you do not have rights to this tab");
	}
}

sub deleteUser{
	if($session->param("access")>=1){
		$a = $CGI->param("a");
		if ($a eq "delete") {
			my $id = $CGI->param('id');
			$db_query = $db->prepare("DELETE FROM users WHERE id='$id'");
			$db_query->execute();
			print qq(
			<div align="center">
			User deleted.<br /><br />
			<script>window.opener.location.reload(false);</script>
			<button onclick="window.close();return false;">Close Window</button>
			</div>
			);
		}else{
			my $id = $CGI->param('id');
			$db_query = $db->prepare("SELECT username FROM users WHERE id = ?");
			$db_query->execute($id);
			
			my @arr = $db_query->fetchrow_array();
			my $username = $arr[0];
			print qq(
				<div align="center">
				Are you sure you want to delete <strong>$username</strong>\'s account?<br><br />
				This cannot be undone.<br /><br />
				<form>
				<input type="hidden" name="id" value="$id">
				<input type="hidden" name="s" value="deleteUser">
				<button name="a" value="delete">Delete</button></fieldset></form>
				<button onclick="window.close();return false;">Cancel</button>
				</div>
			);
		}
	}else{
		print("Access denied.");
	}
	
}

sub makeAdmin{
	if($session->param("access")>=1){
		my $id = $CGI->param('id');
		$db_query = $db->prepare("UPDATE users SET access=1 WHERE id=?");
		$db_query->execute($id);
		manageUsers();
	}else{
		print("Access denied.");
	}
}

sub makeUser{
	if($session->param("access")>=1){
		my $id = $CGI->param('id');
		$db_query = $db->prepare("UPDATE users SET access=0 WHERE id=?");
		$db_query->execute($id);
		manageUsers();
	}else{
		print("Access denied.");
	}
}