<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="src/favicon/favicon.ico">
    <title>Header</title>
    <link rel="stylesheet" href="style.css">
    <style>

        body {
            margin: 0;
            padding: 0;
            max-width: 100%;
            overflow-x: hidden;
        }
       
        .main-container {
            position: relative;
            align-items: center;
            display: flex;
            border: 0px solid;
            background-color:	#212121;
            width: 100%;
            height: 80px;
            padding: 0 10px;
        }

        #logo {
            position: relative;
            height: 55px;
            width: auto;
            padding: 3px;
            margin: 3px;
        }

        .main-container input {
            position: relative;  
            height: 30px;
            width: 45%;
            border-radius: 8px;
            left: 13%;
            font-size: 16px;
            text-align: center;
        }

        .main-container input::placeholder {
            font-size: 16px;
            text-align: center;
        }

        #profile-img {
            position: relative;
            height: 55px;
            width: 55px;
            padding: 30px;
            right: 0;
            margin-left: auto;

        }


    </style>
</head>
<header>
    <div class="main-container">

            

            <a href="home.php" class="font-regular"><img src="src/img/apnet-logo.png" alt="APNet Logo" id="logo"></a>

            <input type="text" name="" id="" placeholder="Search APNet..." class="font-regular">

            <img src="src/img/default-pfp.png" alt="Default Profile Picture" id="profile-img">

    </div>
</header>
<body>
</body>
</html>