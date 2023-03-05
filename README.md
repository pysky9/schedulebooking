# 吉時約 ScheduleBooking

"吉時約" is an online appointment platform that allows businesses to set available dates and time slots for appointments on the website, and consumers can make appointments through the business's official LINE account.

Test account and password: ply@test.com / Ply@98765
<div style="display:flex; justify-content: center">
  <img src="https://user-images.githubusercontent.com/60932746/222939021-5d5ea6e1-f647-49e4-b3a5-20550dfa3bfc.PNG" style="width: 650px"/>
  <img src="https://user-images.githubusercontent.com/60932746/222939027-65ede13a-42de-4a13-b5ee-8b7e0456e04e.gif" style="width: 150px; height:300px"/>
<div>

# Table of Contents
- [Main Feature](#Main Feature)
- [Project Technique](#Project Technique)
- [Architecture](#sArchitecture)

# Main Feature {#Main Feature}
- Merchant authentication with Json Web Token.
- Cunsumer Sign in with LINE the OAuth 2.0 and OpenID® Connect protocols.
- Once the Merchant sets the appointment schedule, consumers can immediately view the available time slots through the LINE official account.
- Consumers can use TapPay to make payments for their orders on LINE.

# Project Technique {#Project Technique}
<h3>Frontend Technique</h3>
<ul>
<li>JavaScript
<li>Bootstrap 5
</ul>
<h3>Backend Technique</h3>
<ul>
<li>Python/Django
<li>Docker
<li>AWS EC2, S3, RDS
<li>JSON Web Token
<li>Nginx
</ul>
<h3>Third Party Library</h3>
<ul>
<li>FullCalendar
</ul>

# Architecture {#Architecture}
![schedulebooking_architecture](https://user-images.githubusercontent.com/60932746/222962853-e934878e-069e-4791-9e1f-8f1cc05cd452.png)

