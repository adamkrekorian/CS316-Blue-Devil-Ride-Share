After having met with Danai Adkisson from the Technology Engagement Center, my group was able to set up a group VM by reserving one through Duke OIT.  The group VM runs continuously (does not turn off).

The host name for the group VM is as follows: vcm-13365.vm.duke.edu

From there, Danai helped us install docker to run our Postgres database.

To access and alter our database, first log in to your personal VM for the class.  Then, type in the following command to access and alter our production database:

$ psql -h vcm-13365.vm.duke.edu -p 5432 -U rideshare -d production

The username is rideshare.
You will be prompted to enter a password. The password is: 316project.

From there, you can use commands such as \dt to view the tables in our database, \d+ table_name to view a summary of a table, or \l for a list of databases. You can also create and modify tables, run queries, create triggers, etc. in the command line.
We created our tables by copying and pasting our create.sql file into the command line. We did the same with our insert statements. 

To deploy the website:

Access the group VM above (password available upon request - please contact calleigh.smith@duke.edu). On that VM is a docker that runs our website. We requested an alias for our site through Duke's Colab: bluedevilrideshare.colab.duke.edu

When you are in the VM, navigate to the "Flask" folder:
/home/vcm/CS316-Blue-Devil-Ride-Share/Flask

Once you are in the Flask folder, to redeploy the website, use the following commands:

$ docker-compose down
$ git pull
$ docker-compose build
$ docker-compose up -d

You can check that the website is successfully running by running the following command in Terminal:

$ docker ps -a

Then the website can be found on bluedevilrideshare.colab.duke.edu:8080/rides