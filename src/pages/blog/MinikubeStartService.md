---
layout: $/layouts/post.astro
title: "Creating a simple systemd service to auto-start minikube"
description: "Check out this post to see how to setup a systemd service to automatically start minikube." 
# there MUST be at least 1 tag listed or it will not render
tags:
  - Intro
  - Minikube
  - Systemd
  - Ubuntu
  - Bash
  - "Platform Engineering"
  - Kubernetes
  - OvaTheTap
  - "Tanzu Application Platform"
author: Art Fewell
authorTwitter: afewell
date: 2023-01-09T08:00:18.276Z
---

I have been working with some of my peers on creating a nested vApp with Tanzu Application Platform that will be used in various educational and demo scenarios.

We are currently using minikube to provide the kubernetes cluster for this environment. This is a nested lab environment all running within a single ubuntu desktop, so we wanted to choose a kubernetes distribution that is optimized for this use case. 

Minikube overall is a very robust solution for lab environments and maintains persistence for the kubernetes/etcd configuration across reboots. It currently does not have a feature to automatically start on boot/reboot. There is a longstanding feature request for a native solution within minikube, so if anyone has the knowledge and can help contribute, you can see [the issue on the minikube repository here](https://github.com/kubernetes/minikube/issues/5301).

Even though minikube does not have a native solution for auto-starting, its pretty easy to create a system service to meet this need. In my case, I am saving my virtual lab in a catalog, and I want users to be able to load up my template from the catalog, start the vApp, and have the system boot to a fully available state. Another key use case could be, if you want to ensure your lab kubernetes environment comes back up in the event of a host reboot. 

## How to create the service
### Step 1: Create the system-d service file
The order in which you create the required files doesnt really matter, but I will start with the system-d service file. 

A system-d service file is required for all system-d services. The main purpose of these files is to provide the location of scripts to start, stop or restart a service. You can also define which user logins trigger the service to start, which user account the service should run as and other similar criteria. 

In this case, I only need my service to start minikube on boot, so I am only going to create a startup (ExecStart) service that will run once. I also specify that the service should run as the user "viadmin", which is the standard account that users of this template will use to access the host. Minikube creates files, such as a kubeconfig, based on the user account that launches the cluster, so having this user account start minikube ensures the service is accessible to the user without needing to jump through extra hurdles.

To create the service file, enter the following commands
```sh
sudo bash -c 'cat << EOF > /etc/systemd/system/minikubestart.service
[Unit]
Description=minikubestart

[Service]
Type=simple
User=viadmin
ExecStart=/usr/local/bin/minikubestart.sh

[Install]
WantedBy=multi-user.target
EOF'
# Set the required permissions for this file to work correctly
sudo chmod 664 /etc/systemd/system/minikubestart.service
```

### Create a script to start the service

Next you will create a script that reliably starts your service. The key word here is reliably, as often a single command may run a service, but you will likely want to ensure your service starts correctly. 

You can enter the following commands to create the minikube start script - I put comments on each key line to explain the purpose of each:
```sh
sudo bash -c 'cat << EOF > /usr/local/bin/minikubestart.sh
#!/bin/bash

# create a log directory - because the script is run as viadmin user, I used a directory this user has permissions to write files to  
mkdir -p /home/viadmin/logs
echo "the minikubestart service is initiating at: $(date)" > /home/viadmin/logs/minikubestart.log

# the following command uses grep to check for the line "apiserver: Running" from the output of the "minikube status" command. If minikube is not running, the minikube_running variable will be empty 
minikube_running=$( minikube status | grep "apiserver: Running")

# the -z parameter returns true if a variable is empty or null. The minikube_running variable should only be populated if minikube is running, so this if statement will determine if minikube is running or not, and enter a line in the log file accordingly.
if [ -z "$minikube_running" ];
then echo "minikube is not running at: $(date)" >> /home/viadmin/logs/minikubestart.log
else echo "Minikube is running at: $(date)" >> /home/viadmin/logs/minikubestart.log
fi

# the following while statment checks to see if the minikube_running variable is empty, and it only runs if it is empty, and so it does not run if minikube is already running.  
while [ -z "$minikube_running" ]
do
        echo "attempting to start minikube at $(date)" >> /home/viadmin/logs/minikubestart.log
        # The following line starts minikube and sends any output to the log file
        minikube start | tee -a /home/viadmin/logs/minikubestart.log
        sleep 10
        # This command checks to ensure that minikube starts successfully. If minikube is running, updating this variable will ensure that the while loop will be exited
        minikube_running=$( minikube status | grep "apiserver: Running")
        if [ -z "$minikube_running" ];
        then
                echo "minikube is not running at: $(date)" >> /home/viadmin/logs/minikubestart.log
        else
                echo "Minikube is running at: $(date)" >> /home/viadmin/logs/minikubestart.log
        fi
done
EOF'

# Set the required permissions for the file to be executed
sudo chmod 744 /usr/local/bin/minikubestart.sh
# because systemd will run the service as the user viadmin, set viadmin as file owner to prevent permissions error
sudo chown viadmin:viadmin /usr/local/bin/minikubestart.sh
```

### Enabling your new system service

Now that you have the required files in place, all that is left is to enable the new service. 

- First, enter the command `systemctl daemon-reload`
- Next, enter `systemctl start minikubestart.service`
  - This will start the service and execute your ExecStart script. Normally the service will start at boot time, so the result of the script run may be different when enabling it this way, but, starting the service manually like this is a good way to check for unexpected errors. 
- Next check on the status of the service to see if starting the service had any unexpected errors:
  - `systemctl status minikubestart`
  - If anything in the output of this commands indicates any problems with your script or service file, make any needed adjustments and check again 
- Next, enable the new service with the command `systemctl enable minikubestart.service`

Now your new system service should be fully operational. The final step is to test the new service to ensure its working as expected. To verify, you will need to reboot your system and then verify minikube starts automatically. 

After you reboot your system, it may take a few minutes for minikube to fully start. If you log in right after a reboot, the minikubestart service may not have yet had a chance to finish executing, so its important to check the logs from the minikubestart service to determine if it may still be executing. 

Because the minikubestart.sh script logs its activities to the minikubestart.log, the best way to validate the service is to look at the log file with the command `cat /home/viadmin/logs/minikubestart.log`. If the service has already finished running, you will see an entry in the log file that states "Minikube is running". 

If the minikubestart service is still executing, the log file should not include the line "Minikube is running". In this case, its hard to be certain if the service is still executing or if something didnt work correctly - but if you watch the log file, you should see new lines added as the minikubestart service progresses. But if you wait a few minutes and do not see any lines added to the log, that could indicate the service did not work correctly. 

To watch the log file, enter the command `watch cat /home/viadmin/logs/minikubestart.log`. If you have any problems, try the command `systemctl status minikube` to see if there are any relevant error messages. And if you need to troubleshoot the service further, I recommend manually executing the service script to ensure it executes properly. 

If you are running a linux distribution that uses system-d, the steps provided in this blog should result in a service that automatically starts minikube on boot. 

Thanks for reading!
