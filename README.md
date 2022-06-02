# Follow the below step to run app
 1.Run the cli.py with python cli.py -m migrate to create the database
 2.Run cli.py again to create admin and standard user as follows
python cli.py -u admin -p admin -n Admin -e admin@mycart.com
3.Run cli.py again to create the one user as follows
python cli.py -u username -p password -n name -e email@mycart.com
Now run the main.py to start the app and login with admin credentials to add category and products.
