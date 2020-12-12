from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <html>
    <head>
        <title>Home</title>
    </head>
    <body style="margin-left: 100px">
        <h1>Hello Guy!</h1>
        <h2>This is our API documentation!</h2>
        <h3>We have some URLs that allows you to work with API, these are listed bellow:</h3>
        <p>Note that our base API URL is "https://bracket.pythonanywhere.com/api/".</p>
        <h3>Moreover there are some parameters you should send to its URL with its dedicated Method.<h3><br>
        
        <h4>Getting All Users:</h4>
        <h5>URL: user/get-all/ </h5>
        <h5>METHOD: GET </h5>
        <h5>RETURN: This endpoint will return all existed users.</h5><br>

        <h4>Creating a New User:</h4>
        <h5>URL: user/create/ </h5>
        <h5>METHOD: POST </h5>
        <h5>PARAMETERS:<br>
                <p style="margin-left:40px">
                'email' -> string<br>
                'name' -> string<br>
                'password' -> string<br>
                'birth_date' [OPTIONAL] -> 'yyyy-mm-dd' string<br>
                'gender' [OPTIONAL] -> 'Male' or 'Female' or 'Prefer Not to Say' or 'Non Binary'
                </p>
        </h5>
        <h5>RETURN: This endpoint will return the created user with its properties.</h5><br>
        <h3>There are some other endpoints that are not documented, I will do that soon!</h3>
        <!--
        <h4>Get User Properties and Update it:</h4>
        <h5>URL: user/me/ </h5>
        <h5>METHOD: GET, PUT, PATCH </h5>
        <h5>PARAMETERS (just for updating):
                'email' -> string
                'name' -> string
                'password' -> string
                'birth_date' [OPTIONAL] -> 'yyyy-mm-dd' string
                'gender' [OPTIONAL] -> 'Male' or 'Female' or 'Prefer Not to Say' or 'Non Binary'
                'is_staff' -> bool (true if you want to make staff acount)
        </h5>
        <h5>RETURN: This endpoint will return the created user with its properties.</h5><br>
        -->
    </body>
    </html>
    """)