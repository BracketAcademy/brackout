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
        <h3>Moreover there are some parameters you should send to its URL with its dedicated Method.<br>
            You can send request in browser with cool django-rest templates!
        <h3><br>

        <h4>Creating a New User:</h4>
        <h5>URL: user/create/ </h5>
        <h5>METHOD: POST </h5>
        <h5>PARAMETERS:
                <p style="margin-left:40px">
                'email' -> string<br>
                'name' -> string<br>
                'password' -> string<br>
                'birth_date' [OPTIONAL] -> 'yyyy-mm-dd' string<br>
                'gender' [OPTIONAL] -> 'Male' or 'Female' or 'Prefer Not to Say' or 'Non Binary'
                </p>
        </h5>
        <h5>PERMISSIONS: No permission needed</h5>
        <h5>RETURN: This endpoint will return the created user with its properties.</h5><br>

        <h4>Create Token:</h4>
        <h5>URL: user/me/token </h5>
        <h5>METHOD: POST </h5>
        <h5>PARAMETERS (just for updating):
                <p style="margin-left:40px">
                'email' -> string <br>
                'password' -> string <br>
                </p>
        </h5>
        <h5>PERMISSIONS: No permissions needed. Just having your credentials.
        </h5>
        <h5>RETURN: This endpoint will return your Token.</h5><br>

        <h4>Get User Properties and Update it:</h4>
        <h5>URL: user/me/ </h5>
        <h5>METHOD: GET, PUT, PATCH <br>
            <p style="font-weight: 100; margin-left: 40px">
            PUT is a method of modifying resource where the client sends data that updates the entire resource.<br>
            It is used to set an entity’s information completely.<br>
            PUT is similar to POST in that it can create resources, but it does so when there is a defined URI.<br>
            PUT overwrites the entire entity if it already exists, and creates a new resource if it doesn’t exist.<br><br>
            
            Unlike PUT, PATCH applies a partial update to the resource.<br>
            This means that you are only required to send the data that you want to update,<br>
            and it won’t affect or change anything else.<br>
            So if you want to update the first name on a database,<br>
            you will only be required to send the first parameter; the first name.
            </p>
        </h5>
        <h5>PARAMETERS (just for updating):
                <p style="margin-left:40px">
                'email' -> string <br>
                'name' -> string <br>
                'password' -> string <br>
                'birth_date' [OPTIONAL] -> 'yyyy-mm-dd' string <br>
                'gender' [OPTIONAL] -> 'Male' or 'Female' or 'Prefer Not to Say' or 'Non Binary' <br>
                </p>
        </h5>
        <h5>PERMISSIONS:
            You have to use this endpoint with your Token!
            This token should be passed with 'Authentication' Header.
        </h5>
        <h5>RETURN: This endpoint will return the current user with its properties.</h5><br>

        <h4>Getting All Users:</h4>
        <h5>URL: user/get-all/ </h5>
        <h5>METHOD: GET </h5>
        <h5>PERMISSIONS: Just staff acounts can access this endpoint.<br>
            You have to use this endpoint with your Token!
            This token should be passed with 'Authentication' Header.
        </h5>
        <h5>RETURN: This endpoint will return all existed users.</h5>
    </body>
    </html>
    """)