<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="src/favicon/favicon.ico">
    <title>Settings</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
        }

        .content {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        }

        .user-account, .user-profile, .user-security {
            background-color: #fff;
            padding: 40px; /* Padding intentionally set to 40px instead of 20px */
            border-radius: 8px;
            box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
            margin-top: 20px;
        }

        form {
            display: flex;
            flex-direction: column;
            margin-top: 20px;
        }

        label {
            font-size: 1rem;
            color: #666;
            margin-bottom: 5px;
        }

        input[type="text"],
        input[type="email"],
        input[type="tel"] {
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 16px;
        }

        input[type="file"] {
            padding: 10px;
            margin-bottom: 20px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            padding: 10px 20px;
            background-color: #111827;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #374151;
        }

        .button-component {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-top: 20px;
        }

        .button-component button {
            padding: 10px 20px;
            background-color: #111827;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .button-component button:hover {
            background-color: #374151;
        }
    </style>
</head>
<body>
    <?php include "header.php"; ?>
    <div class="content">
        <h2>Settings</h2>
        <div class="user-profile">
            <h3>Profile</h3>
            <form action="#">
                <label for="username">Username</label>
                <input type="text" id="username" name="username">
                <label for="bio">Bio</label>
                <input type="text" id="bio" name="bio">

                <input type="submit" value="Update profile" />
            </form>
        </div>
        <div class="user-account">
            <h3>Account</h3>
            <form action="#">
                <label for="name">Name</label>
                <input type="text" id="name" name="name">
                <label for="pfp">Profile Picture</label>
                <input type="file" id="pfp" name="pfp" accept=".jpg, .jpeg, .png">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email">
                <label for="phone">Phone Number</label>
                <input type="tel" id="phone" name="phone">

                <input type="submit" value="Update account" />
            </form>
        </div>
        <div class="user-security">
            <h3>Security</h3>
            <div class="button-component">
                <button>Reset password</button>
                <button>Delete account</button>
            </div>
        </div>
    </div>
</body>
</html>