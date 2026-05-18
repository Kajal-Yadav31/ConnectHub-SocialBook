# ConnectHub - Your Social Media Hub

## Overview
ConnectHub is a full-featured social media platform developed using Django where users can connect, share posts, send friend requests, and chat in real time. The platform includes secure authentication, profile management, dynamic post interactions, AJAX-based social features without page reloads, and real-time one-to-one chat using Django Channels and WebSockets.
The project focuses heavily on backend optimization, better user experience, and real-world social media functionality.

## Features

1. **Authentication and Account Management:**
   - Implemented custom user authentication using Django custom user model.
   - Included email verification for secure registration.
   - Added forgot password and reset password functionality.
   - Auto-generated user profiles after signup using Django signals.
   - Optimized email confirmation using Celery to reduce registration delay.

2. **Profile Management:**
   - Users can edit profile details like   profile image, cover image, full name, bio, and location.
   - Dedicated profile page for viewing user information.
   - Displays user posts, friends list, and account activity.
   - Personalized profile experience for every registered user.

3. **Post Creation and Management**
   - Users can create posts with image uploads, captions, and categories.
   - Users can edit and delete their own posts.
   - Dynamic post updates handled using jQuery + AJAX without page reload.
   - Better UI experience with faster interactions.

4. **Social Interaction Features**
   - Users can like posts instantly using AJAX.
   - Users can comment on posts and reply to specific comments.
   - Comment and reply deletion supported.
   - Friend request system implemented:
      - Send request
      - Cancel request
      - Accept request
      - Reject request
   - Improved social engagement across the platform.

5. **Real-Time Chatting Inbox**
   - Built personal one-to-one chat using Django Channels and WebSockets.
   - Real-time instant messaging without page refresh.
   - Dedicated inbox page showing latest message from each conversation.
   - Full message detail page for each chat.
   - Auto-scroll for new messages.

6. **nbox Optimization Using Subquery + OuterRef**
   - Implemented advanced Django query optimization using Subquery and OuterRef.
   - Fetches only the latest message per user conversation.
   - Avoids unnecessary database hits and solves N+1 query problem.
   - Improves inbox performance significantly.
   - Example: If user chatted with Alice and Bob, inbox shows only:
        - Latest message with Alice
        - Latest message with Bob
7. **Block User Feature**
   - Users can block friends directly from chat detail page.
   - Blocked users are removed from friend list.
   - Prevents further interaction between users.
   - Improves privacy and user control.

## Tech Stack

   - Python
   - Django
   - Django Channels
   - WebSocket
   - jQuery/AJAX
   - Celery / MySQL
   - HTML/CSS
   - JavaScript
   - Git/GitHub

## ScreenShots of project:
### Registration Page:
<img width="929" height="873" alt="register" src="https://github.com/user-attachments/assets/73fa9699-67c6-4abd-b2ea-041ca40fc4ca" />


### Login Page:
<img width="1885" height="832" alt="login" src="https://github.com/user-attachments/assets/38bdd2e6-00b4-4001-b33c-6626cd7cbf80" />


### Forgot Password Page:
<img width="1919" height="884" alt="forgot-password" src="https://github.com/user-attachments/assets/61fcbe19-e31d-473e-bd37-aa4db754d9fa" />


### Reset Password Page:
<img width="1919" height="816" alt="resetpassword" src="https://github.com/user-attachments/assets/9661fe25-db1b-4949-840e-9c6b2b32376c" />


### Home Page :
<img width="1916" height="895" alt="feed-page" src="https://github.com/user-attachments/assets/cc66163d-9e59-43bc-877f-7fdc3808d003" />

### Post creation page:
<img width="1910" height="921" alt="create-post" src="https://github.com/user-attachments/assets/b8bcb446-cb78-4ab9-98cf-4f1860253f82" />

### Profile View Page:
<img width="1920" height="2362" alt="profile" src="https://github.com/user-attachments/assets/b9af0dc0-5635-4ada-a345-1cdd84c72b5d" />

### Profile update  Page:
<img width="1920" height="1396" alt="profile-update" src="https://github.com/user-attachments/assets/d91db487-8f1d-488c-a897-7ff0854a8485" />

### Friend profile page: 
<img width="1920" height="2186" alt="friend-profile" src="https://github.com/user-attachments/assets/9980c055-4458-491c-9e86-cc95aae24bdc" />

### Chat Page :
<img width="1920" height="912" alt="chat-page" src="https://github.com/user-attachments/assets/56b7aef5-67bb-49f4-a22b-da5cf48c9302" />


## Getting Started

### Clone the Repository

1) First, clone the repository to your local machine:

git clone https://github.com/Kajal-Yadav31/ConnectHub-SocialBook.git


2) cd `ConnectHub-SocialBook`

### Running the project

### Usage
- Access the application at `http://localhost:8000/` in your web browser.
- Register a new account
- Verify email
- Create posts
- Like, comment, and reply
- Send and manage friend requests
- Use real-time personal chat
- Block unwanted users if needed

## License
This project is licensed under the [MIT License]


## Contact
For inquiries or issues, contact [kajalyadav070496@gmail.com].
