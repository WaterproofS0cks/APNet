<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <title>Document</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            max-width: 100%;
            overflow-x: hidden;
        }

        footer {
            background-color: #292a2d;
            color: white;
            padding: 20px 0; 
        }

        .footer-content {
            display: flex;
            margin: auto;
            max-width: 90%;
        }

        .footer-section {
            flex: 1;
            padding: 20px;
        }

        .footer-section-logo {
            width: 50%;
            padding: 20px;
        }

        .footer-section-logo img {
            height: 60px;
            width: auto;
            padding: 10px;
        }

        .footer-section h2 {
            font-size: 26px;
            margin-bottom: 10px;
            color:  #5495ce;
        }

        .footer-section ul {
            list-style-type: none;
            padding: 0;
        }

        .footer-section ul li {
            margin: 20px 0;
        }

        /* .footer-section a {
            color: white;
            text-decoration: none;
        } */

        /* .footer-section a:hover { 
            text-decoration: underline;
        } */

        .footer-bottom {
            text-align: center;
            padding: 10px 0;
            background-color: #222;
        }
        
    </style>
</head>
<body>
    <footer>
        <div class="footer-content">
            <div class="footer-section-logo">
                <img src="img/APNet_Logo.png" alt="APNet Logo">
            </div>
            <div class="footer-section resources">
                <h2 class="font-heading">Resources</h2>
                <ul>
                    <li><a href="#" class="font-footer-list">Home</a></li>
                    <li><a href="#" class="font-footer-list">About Us</a></li>
                    <li><a href="#" class="font-footer-list">FAQ</a></li>
                    <li><a href="#" class="font-footer-list">User  Agreement</a></li>
                </ul>
            </div>
            <div class="footer-section contacts">
                <h2 class="font-heading">Follow Our Socials</h2>
                <ul>
                    <li><a href="https://www.linkedin.com/in/marcuschanrenzhi/" class="font-footer-list">Marcus Chan</a></li>
                    <li><a href="https://www.linkedin.com/in/sean-yap-9b69022a2/" class="font-footer-list">Sean Yap</a></li>
                    <li><a href="https://www.linkedin.com/in/yewshanooi/" class="font-footer-list">Yew Shan</a></li>
                    <li><a href="https://www.linkedin.com/in/karlson-thien-700715275/" class="font-footer-list">Karlson Thien</a></li>
                    <li><a href="https://www.linkedin.com/in/jeremiah-sii-yi-4272232a3/" class="font-footer-list">Jeremiah Sii</a></li>
                    <li><a href="#" class="font-footer-list">Zheng Yang</a></li>
                </ul>
            </div>
        </div>
    </footer>
</body>
</html>