# StrongBox :closed_lock_with_key:	
A secure way of storing your passwords.

## :key: Why to use StrongBox?
StrongBox makes it possible to have a random generated strong password in each website/application
by remembering only one password, your ```vault password```. <br/> 
StrongBox let you handle multiple vaults, which are uniquely identified by their password: **two vaults cannot
have the same password**. <br/> 
Each vault contains a list of websites/applications accounts, which have a website/app name, username, email and password.
All these password are encrypted and can only be decrypted with the ```vault password```.

***IMPORTANT: your vault key should be strong and unique. You should not store it in your computer.***

## :key: Installation
Clone StrongBox repository:
```
git clone https://github.com/dylannalex/strongbox
```
Install dependencies:
```
pip install -r requirements.txt
```

## :key: Usage
Create a virtual enviroment and set the ```DATABASE_URL``` virtual variable (see
```Set up a remote database on Heroku``` section).
<br/> You are all setup, run **strongbox** with the following command:
```
python -m strongbox
```

## :key: Set up a remote database on Heroku
1. Create a Heroku account if you haven't already
2. Create a new app: https://dashboard.heroku.com/apps
3. Go to https://elements.heroku.com/addons/cleardb, select **Ignite** free plan and press the
```Install ClearDB MySQL``` button
4. At ```App to provision to``` search the app you created and press ```Submit Order Form``` button
5. Go to your app settings and click on ```Reveal Config Vars```
6. Copy the ```CLEARDB_DATABASE_URL``` value, thats your ```DATABASE_URL``` value!
