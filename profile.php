<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="src/favicon/favicon.ico">
    <link rel="stylesheet" href="style.css">
    <title>Profile</title>
    <style>
        .profile {
            display: flex;
            margin-bottom: 20px;
            gap: 20px;
        }

        .profile-img {
            flex-shrink: 0;
            width: 150px;
            height: 150px;
            border-radius: 100%;
            overflow: hidden;
            background-color: #f0f0f0;
        }

        .profile-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .profile-desc {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .profile-desc h2 {
            display: inline-flex;
            align-items: center;
        }

        .verify-badge, .role-badge {
            width: 20px;
            height: 20px;
            margin-left: 10px;
            border-radius: 50%;
        }

        .verify-badge {
            background-color: #5796CC;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-left: 10px;
        }

        .verify-badge img {
            width: 75%;
            height: 75%;
            object-fit: contain;
        }

        .role-badge {
            background-color: grey;
            color: white;
            padding: 15px 40px;
            border-radius: 20px;
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-left: 10px;
        }

        .profile-desc p {
            margin-top: 8px;
            font-size: 1rem;
            color: #666;
        }

        .profile-btn button {
            padding: 10px 20px;
            background-color: #111827;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .profile-btn button:hover {
            background-color: #374151;
        }

        .settings-icon {
            display: inline-block;
            width: 32px;
            height: 32px;
            cursor: pointer;
        }

        .settings-icon img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .navigation {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .nav-btn {
            padding: 12px 20px;
            background-color: #111827;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
        }

        .nav-btn:hover {
            background-color: #374151;
        }

        .post {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        }

        .post-attr {
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .post-title {
            padding: 10px 20px;
            margin-top: 5px;
        }

        .post-img {
            margin-top: 20px;
            height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        }

        .post-inter {
            padding: 10px 20px;
            display: flex;
            gap: 10px;
            align-items: center;
            margin-top: 10px;
        }

        .post-inter button {
            padding: 8px 15px;
            background-color: #111827;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .post-inter button:hover {
            background-color: #374151;
        }

        .post-inter button img {
            width: 20px;
            height: 20px;
        }
    </style>
</head>
<body>
    <?php include "header.php"; ?>
    <div class="content">
        <div class="profile">
            <div class="profile-img">
                <img src="https://tr.rbxcdn.com/180DAY-d2aa8b558f4c73dc77ab184210a56788/420/420/Hat/Png/noFilter" alt="Cat">
            </div>
            <div class="profile-desc">
                <h2>John Doe
                    <div class="verify-badge"><img src="src/icon/icons8-verify-96.png" alt="Verified Checkmark"></div>
                    <div class="role-badge">Student</div>
                </h2>
                <p>Lorem ipsum dolor si amet</p>
            </div>
            <div class="profile-btn">
                <a href="/APNet/settings.php" class="settings-icon">
                    <img src="src/icon/icons8-settings-96.png" alt="Settings Icon">
                </a>
            </div>
        </div>

        <div class="navigation">
            <button class="nav-btn">Posts</button>
            <button class="nav-btn">Bookmarks</button>
            <button class="nav-btn">About</button>
        </div>

        <div class="post">
            <div class="post-attr">
                <p>@cat • Recruitment</p>
                <p>1 week ago</p>
            </div>
            <div class="post-title">
                <h3>This is a post title</h3>
            </div>
            <div class="post-img">
                <img src="" alt="Post Image">
            </div>
            <div class="post-inter">
                <button>
                    <img src="src/icon/icons8-like-96.png" alt="Like Icon">Like
                </button>
                <button>
                    <img src="src/icon/icons8-comment-96.png" alt="Comment Icon">Comment
                </button>
                <button>
                    <img src="src/icon/icons8-bookmark-96.png" alt="Bookmark Icon">Bookmark
                </button>
            </div>
        </div>
    </div>
</body>
</html>
