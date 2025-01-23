<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">    
    <title>Document</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            max-width: 100%;
            overflow-x: hidden;
        }

        footer {
            background-color: #000;
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

        .footer-section img {
            height: 55px;
            width: auto;
            padding: 10px;
        }

        .footer-section h2 {
            font-size: 30px;
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

        .footer-section a {
            color: white;
            text-decoration: none;
        }

        .footer-section a:hover { 
            text-decoration: underline;
        }

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
            <div class="footer-section logo">
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
                <h2 class="font-heading">Follow Us</h2>
                <ul>
                    <li><a href="#" class="font-footer-list">LinkedIn</a></li>
                    <li><a href="#" class="font-footer-list">GitHub</a></li>
                    <li><a href="#" class="font-footer-list">Instagram</a></li>
                    <li><a href="#" class="font-footer-list">Twitter</a></li>
                </ul>
            </div>
        </div>
    </footer>
</body>
</html>