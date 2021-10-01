# REST-API-with-Docker
This is a dockerized REST API that has authorization and authentication with MongoDB backup 


1. You have to download the docker in your computer. You can  download the docker using this link ---> https://www.docker.com/products/docker-desktop 

2. Make sure you have enabled Hyper-V Windows Features or the Install required Windows components for WSL 2 option is selected on the Configuration page.

3. When installation is completed, you will get an error called "WSL 2 Installation is Incomplete". You have to click the link on the error window and follow the steps. 

4. After completing all steps, click restart on the error window.

5. Extract the file named docker inside zip to the desktop.

6. To build your dockerized application, you have to open cmd first and go to the location where you extracted zip files.

7. Directory on the cmd should look like this---> C:\Users\username\Desktop\docker

8. Then you have to type docker-compose build to build your docker application ---> C:\Users\username\Desktop\docker>docker-compose build

9. After building is finished, you can start the application by typing docker-compose up.---> C:\Users\username\Desktop\docker>docker-compose up

10.You can use Postman to test your application. Click My Workspace and on the right hand side of the Import button, there is a + sign. You can create a new request by clicking this sign.

11.When you testing, First you have to go to login page and use one of the users credentials to log in(By using form data). Then the application creates a token for you. 
   You have to use this token to reach other endpoints or you cannot see anyone. To reach restricted sections, you need to copy and paste the access token you got to Bearer token auth type in the postman and that is all. 
   You can access the restricted sections. 

					
!!But be careful, token will expire some time later and you have to relogin and replace the old token with the new one!!


		    ******* Instructions on routes *******

You have to use form-data on postman to test the application.
Below the request section, click Body and chose form-data.
Please use form-data exactly like how its shown below

For Users	|	For Products
		|
Name:		|	Product Name:
Surname:	|	Price:
Email:		|	Quantity:
Password:	|

User Credentials for testing the api

Email:test2@gmail.com	Passsword:tester2"					
Email:test@gmail.com		Password:tester1

Routes for the api

*http://localhost:5000/login               ---> For Login to the system 		use ['POST'] request
*http://localhost:5000/users               ---> To see all users 			use ['GET'] request
*http://localhost:5000/users<_id>          ---> To see specific user 			use ['GET'] request
*http://localhost:5000/register            ---> To register a new user 		use ['POST'] request
*http://localhost:5000/updateuser<_id>     ---> To update a specific user 		use ['PUT'] request
*http://localhost:5000/deleteuser/<_id>    ---> To delete a specific user 		use ['DELETE'] request


*http://localhost:5000/products            ---> To see all products 			use ['GET'] request
*http://localhost:5000/products<_id>       ---> To see a specific product 		use ['GET'] request
*http://localhost:5000/addproduct          ---> To To add a new product 		use ['POST'] request
*http://localhost:5000/updateproduct/<id>  ---> To update a specific product 		use ['PUT'] request
*http://localhost:5000/deleteproduct/<id   ---> To delete a specific product 		use ['DELETE'] request
