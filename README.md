# drchrono Hackathon

### Check-in kiosk

Picture going to the doctor's office and replacing the receptionist and paper forms
with a kiosk similar to checking in for a flight.

There should be an account association flow where a doctor can authenticate using
their drchrono account and set up the kiosk for their office.

After the doctor is logged in, a page should be displayed that lets patients check
in. A patient with an appointment should first confirm their identity (first/last
name maybe SSN) then be able to update their demographic information using the
patient chart API endpoint.  Once the they have filled out that information the
app can set the appointment status to "Arrived" (Appointment API Docs).

The doctor should also have their own page they can leave open that displays
today’s appointments, indicating which patients have checked in and how long they
have been waiting. From this screen, the doctor can indicate they are seeing a
patient, which stops the “time spent waiting” clock. The doctor should also see
the overall average wait time for all patients they have ever seen.

Outside of these base requirements, you are free to develop any features you think
make sense.

To begin, fork the drchrono API project repo at https://github.com/drchrono/api-example-django

We’ve built this repo to save you some set-up time! It contains a few baseline structural elements for you to build on.
It’s a great starting point, but there are probably some tweaks and improvements to be made before you continue building 
out new functionality. It doesn't quite work; it's your job to make it work, and then make it awesome!

Use the drchrono API docs and feel free to reach out to the people operations team with any questions and we'll get back
to you ASAP.

### Requirements
- [docker](https://www.docker.com/community-edition)
- a free [drchrono.com](https://www.drchrono.com/sign-up/) account


#### API token 
The first thing to do is get an API token from drchrono.com, and connect this local application to it!

This project has `social-auth` preconfigured for you. The `social_auth_drchrono/` contains a custom provider for
[Python Social Auth](http://python-social-auth.readthedocs.io/en/latest/) that handles OAUTH through drchrono. It should
 require only minimal configuration. 

1) Log in to [drchrono.com](https://www.drchrono.com)
2) Go to the [API management page](https://app.drchrono.com/api-management/)
3) Make a new application
4) Copy the `SOCIAL_AUTH_CLIENT_ID` and `SOCIAL_AUTH_CLIENT_SECRET` to your `docker/environment` file.
5) Set your redirect URI to `http://localhost:8080/complete/drchrono/`


### Dev environment Setup
Docker should take care of all the dependencies for you. It will create two containers: an application server and a 
MySQL database server. See `docker-compose.yml` for details.

``` 
$ git clone git@github.com:drchrono/api-example-django.git hackathon
$ docker-compose up
```

Then connect with a browser to [http://localhost:8080/setup]() and use the web to authorize the application.


### Happy Hacking!
If you have trouble at any point in the setup process, feel free to reach out to the developer
who introduced you to the project. We try to minimize setup friction, but 
