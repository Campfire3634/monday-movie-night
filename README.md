# Monday Movie Night
This Python script uses the api from The Movie Database (TMDB) to grab details about movies and each movies cast & crew. Then, it adds that data to a Supabase database. 

## Step 1: Set up your Supabase database
Head to http://supabase.com/ to create a free Supabse account. After creating your account, grab your Supabase URL and Supabase key and put in the .env file

## Step 2: Get a TMDB api key 
Navigate to https://developer.themoviedb.org/docs/getting-started and follow the instructions. Then put your API key in the .env file

## Step 3: Test it out
Run the script. It should add details for They Live along with cast and crew information to your database. 

Now you have a working python script to grab movie details and add it to Supabase! 
