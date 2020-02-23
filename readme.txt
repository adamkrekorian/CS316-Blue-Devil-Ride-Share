After having met with Danai Adkisson from the Technology Engagement Center, my group was able to set up a group VM by reserving one through Duke OIT.  The group VM runs constantly (does not turn off).

The host name for the group VM is as follows: vcm-13365.vm.duke.edu

From there, Danai helped us install docker to run our Postgres database.

To access and alter our database, first log in to your personal VM for the class.  Then, type in the following command to access and alter our production database:

$ psql -h vcm-13365.vm.duke.edu -p 5432 -U rideshare -d production

The username is rideshare.
You will be prompted to enter a password. The password is: 316project.

From there, you can use commands such as \dt to view the tables in our database or \l for a list of databases. You can also create and modify tables, run queries, create triggers, etc. since Postgres supports SQL.