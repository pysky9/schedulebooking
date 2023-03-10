# 吉時約 ScheduleBooking

"吉時約" is an professional service booking platform that allows merchants to set available dates and time slots for appointments on the website, and consumers can make appointments through the business's official LINE account.<br>

WebSite: https://www.schedule-booking.com/ LINE官方帳號預訂: https://lin.ee/MZCAf7v<br>
WebSite test account and password: ply@test.com / Ply@98765
## Demo
<h3>Merchant Backend Management System</h3>
- Setting reservation dates and time slots<br>
- Order management<br>
- Customer information will be displayed on the reservation calendar<br>
- Linkage with LINE Official Account<br>
<img src="https://user-images.githubusercontent.com/60932746/223953100-319dfc83-e34a-4c58-a208-fb4b610dcc07.gif" style="width: 650px"/>

<h3>Customer Booking System</h3>
<img src="https://user-images.githubusercontent.com/60932746/222939027-65ede13a-42de-4a13-b5ee-8b7e0456e04e.gif" style="width: 150px; height:300px"/>

## Table of Contents
- [Main Feature](#main-feature)
- [Project Technique](#project-technique)
- [Architecture](#architecture)
- [Contact](#contact)

## Main Feature
- Merchant authentication with Json Web Token.
- Cunsumer Sign in with LINE the OAuth 2.0 and OpenID® Connect protocols.
- Once the Merchant sets the appointment schedule, consumers can immediately view the available time slots through the LINE official account.
- Display only the available time slots for reservations on the client side starting from the current time onwards.
- Consumers can use TapPay to make payments for their orders.
- After the consumer completes the payment, the reserved schedule will automatically appear on the merchant's backend system calendar.

## Project Technique
<h3>Backend Technique</h3>
<ul>
<li>Python/Django
<li>Docker
<li>AWS EC2, S3, RDS
<li>JSON Web Token
<li>Nginx
<li>SSL
</ul>
<h3>Frontend Technique</h3>
<ul>
<li>JavaScript
<li>Bootstrap 5
<li>HTML
<li>CSS
</ul>
<h3>Third Party Library</h3>
<ul>
<li>FullCalendar
<li>TapPay
</ul>

## Architecture
<h3>Web Architecture</h3>
<img src="https://user-images.githubusercontent.com/60932746/222962853-e934878e-069e-4791-9e1f-8f1cc05cd452.png">
<h3>Database Architecture</h3>
<img src="https://user-images.githubusercontent.com/60932746/223929245-a8fc9b1f-4a53-4b93-8baa-b041b9713051.png">

## Contact
李榮輝 Jung-Hui Li

Email: derek.j.h.li@gmail.com

