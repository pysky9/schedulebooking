# 吉時約 ScheduleBooking

"吉時約" is a service booking platform that allows merchants to set available dates and time slots for appointments on the website, and consumers can make appointments through the merchants' official LINE account.<br>

WebSite: https://www.schedule-booking.com/ LINE Official Account: https://lin.ee/MZCAf7v<br>
WebSite test account and password: ply@test.com / Ply@98765
## Demo
### Merchant Backend Management System
- Setting reservation dates and time slots<br>
- Order management<br>
- Customer information will be displayed on the reservation calendar<br>
- Linkage with LINE Official Account<br>
<img src="https://user-images.githubusercontent.com/60932746/223953100-319dfc83-e34a-4c58-a208-fb4b610dcc07.gif" style="width: 650px"/>

### Customer Booking System
- Customers can use LINE to make reservations, payments, and check reservation records all in one platform.
<img src="https://user-images.githubusercontent.com/60932746/222939027-65ede13a-42de-4a13-b5ee-8b7e0456e04e.gif" style="width: 150px; height:300px"/>

## Table of Contents
- [Main Feature](#main-feature)
- [Project Technique](#project-technique)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Contact](#contact)

## Main Feature
- Merchant authentication with JSON Web Token.
- Customer Sign in with LINE the OAuth 2.0 and OpenID® Connect protocols.
- Once the Merchant sets the appointment schedule, customers can immediately view the available time slots through the LINE official account.
- Display only the available time slots for reservations on the client side starting from the current time onwards.
- Customer can browse the website within the LINE app using LINE LIFF.
- Customer can use TapPay to make payments for their orders.
- After the customer completes the payment, the reserved schedule will automatically appear on the merchant's system calendar.

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
- Using Django to develop the website
- Using Bootstrap to build web layouts
- Integrating the LINE LIFF browser on the consumer side, allowing consumers to complete web operations in LINE
- Integrating LINE Login to obtain consumers' personal public information
<img src="https://user-images.githubusercontent.com/60932746/222962853-e934878e-069e-4791-9e1f-8f1cc05cd452.png">

## Database Schema
<img src="https://user-images.githubusercontent.com/60932746/223929245-a8fc9b1f-4a53-4b93-8baa-b041b9713051.png">

## Contact
李榮輝 Jung-Hui Li

Email: derek.j.h.li@gmail.com

