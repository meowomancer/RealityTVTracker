=begin comment
helpers.cgi

MODULE DESCRIPTION:
    System module allowing for calling success, warning and failure boxes.
    
MODULE SUBROUTINES
    success($): Creates a green success message box with message provided as
                an argument
                
    warning($): Create an orange warning message box with message provided as
                an argument
                
    failure($): Create a red failure messageb ox with message provide as an
                argument
                
=end comment
=cut


#Success Message
sub success{
    print qq(
        <div class="alert alert-success">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            $_[0]
        </div>
    );
}

#Warn Message
sub warning{
    print qq(
        <div class="alert alert-info">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            $_[0]
        </div>
    );
}

#Failure Message
sub failure{
    print qq(
        <div class="alert alert-error">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            $_[0]
        </div>
    );
}
