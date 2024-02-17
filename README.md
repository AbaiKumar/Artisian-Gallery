
# Artisian Gallery
This project aims to address the challenges faced by artisans in accessing digital markets by providing them with a comprehensive digital commerce solution. We recognize the crucial role artisans play in preserving traditional crafts and cultural heritage, yet we understand the difficulties they encounter in reaching a wider audience and selling their products in today's digital landscape.

Our platform serves as a bridge between artisans and potential customers, empowering artisans to showcase their unique creations and connect with a broader audience. Through our platform, artisans can create personalized profiles, upload images and descriptions of their products, and interact with customers in real-time.

Key features of our platform include:

Artisan Profiles: Each artisan can create a personalized profile, providing background information, stories behind their crafts, and their creative process. This helps customers understand the artisan's unique identity and artistic vision.

Product Showcase: Artisans can showcase their products through high-quality images and detailed descriptions. Customers can browse through a diverse range of traditional crafts, handmade goods, and culturally significant artifacts.

# Tech Stack used
 * HTML
 * CSS 
 * JavaScript 
 * Python Flask
 * MongoDB
## How it Works
Initially you have to sign-up. This has two types ,one is for customer and the other is for artists. After signing up, you have to login as either artist or customer and the email and password is validated.
* For, artist after log in as artist homepage which will have two buttons (Adding artist detail,Adding art piece details).In the Adding artist details it will ask for Profile image, Name ,Skills,Certificates,Signature-To validate the sign whether it is from the original artist or a copy,Phone number,address,Country and Masterpiece-Of his work the art which was sold the most .When submit is clicked the data is uploaded to the database.In the Adding art piece details it will ask for title,description of the art,Photos of the art in different angles,Option to bid or to sell . The bid or sell price will be asked to enter based on preference. When submit is clicked the data is uploaded to the database.
* For, customer after log in the customer homepage which will have upcoming bids, and on the right list out all art piece in a grid format it will show  first 10 images in page 0. In grid the art piece image, Title and add to cart option will be shown. Add to cart option will add the art piece to cart and these art piece can be visited by clicking on cart on the top right side corner. Here, we can specify the quantity, edit the list which is in table format and when check out we get a receipt. To know more about the art piece we need to click on the image of art piece which will redirect to the detailed page.This page will have the art piece image, title and description. Additionally there will be comments and review section and we can see available reviews and also add a new review. In the customer homepage we have added a search option to retrieve recommended art pieces. This search option uses natural language toolkit processing package in python. Contact us page will give username, message which will give any queries from customer side.
# Features that are not included:
* Signature validation
* Bidding Option
* Pricing Fixing Using ML
## Authors

- [@Javagar]()
- [@Vaishnev]()
- [@Vankatprasadh]()
- [@Abaikumar]()

