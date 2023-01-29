---
layout: $/layouts/post.astro
title: "Setting up Gitlab for my Tanzu Application Platform 1.4 Lab"
description: "In this blog I will walk through the steps I used to plan, install, configure and integrate Gitlab with Tanzu Application Platform 1.4.0 in my lab environment." 
# there MUST be at least 1 tag listed or it will not render
tags:
  - Tanzu
  - "Tanzu Application Platform"
  - Gitlab
  - "Cert-Manager"
  - "Platform Engineering"
  - Kubernetes
  - "Tanzu Packages"
  - "Certificates"
  - "Private Certificate Authority"
  - OvaTheTap
  - Backstage
  - "Spotify Backstage"
author: Art Fewell
authorTwitter: afewell
date: 2023-1-27T08:00:18.276Z
---

Tanzu Application Platform (TAP) 1.4 has some cool integrations with Github and Gitlab. While I have my public TAP environment integrated with GitHub, today I am working on updating my [ovathetap](https://github.com/afewell/ovathetap) project, which implements TAP on a single node lab environment. I intend to use this lab for different trainings and want to keep it self contained so while its always an option, people would not need to use their own credentials to have a complete experience in the lab environment. 

I have also been wanting to use gitlab in a lab environment for years just to get some more experience with it and be able to offer insight for the many many enterprise customers who use gitlab - the only reason I havent sooner is because I often build labs where having as low footprint as possible is a key goal and using as much SaaS as possible is a benefit, which has resulted in almost all my git experience being on github. 

So I was excited to learn about it and am pleased to report it was a pretty elegant experience, if you come from a background working with GitHub, it is true that Gitlab has some differences so you have to adapt some, but its pretty straightforward and well documented. Another nice benefit which I think will become a really important criteria soon is, ChatGPT is pretty knowledgable with it and I was able to get some decent help to speed me through some questions I had during my setup ... keep an eye out for another blog on that topic specifically as its a bit too much to detail in this post with all the other things I am trying to cover here. 

## The Plan

Since this is a single node lab environment, the first thing I wanted to do was to slim down the default gitlab configuration to make it as light as I can. Gitlab has a lot of really cool features that I may add someday if I need them, but for the time being I only need the basic git serving and authentication services. This can be done pretty easily by going through the helm charts and the installation documentation. 

The Gitlab helm chart also by default deploys an ingress controller and cert-manager, and in many cases that is great, it allows you to get a fully functional environment just by deploying the helm chart. But in my case I already have the Contour ingress controller and cert-manager up and running with my TAP installation, and so to keep things slim I will update the Gitlab helm chart values to skip the ingress controller and cert manager installations. This also means it will not provision the ingress resources for gitlab services, so I will create the ingress objects needed for gitlab and apply them seperately. 

I should note that in many cases where you have plentiful resources I dont think there is any problem using the default gitlab helm chart even if you are also using other ingress controllers, and I dont think there is any other benefit from having TAP and gitlab share the same ingress controller, the only reason for doing this in my case is to keep things extra slim given its for a single node environment. 

Once I get gitlab deployed, I will create admin and developer accounts and create a group and repository that I will use to store the "yelb" catalog that is available with tap and provides some example catalog content.  

I will then configure the tap-values file to setup integration with gitlab for authentication services, to access the tap-catalog, and also so that TAP can automate creation of a repository for users of TAP Application Accelerators.

## Part 1: Customizing and deploying the Gitlab helm chart

Gitlab has a pretty large helm values chart, but its well organized and getting through it isnt too bad if youve had some experience with helm values charts before. 

Its a really long chart so I will only put the sections that I changed here, but if you want to see the entire chart, [you can view it here](https://github.com/afewell/ovathetap/blob/main/assets/gitlab-values.yaml).

Here are the sections I modified from the default helm values chart:
```sh
global:
  # defaultWas: ee
  edition: ce
  hosts:
    # defaultWas example.com
    domain: tanzu.demo
  ingress:
    # defaultWas: true
    configureCertmanager: false
    # defaultWas: true
    enabled: false
certmanager:
  # defaultWas: true
  installCRDs: false
nginx-ingress:
  # defaultWas: true
  enabled: false
prometheus:
  # defaultWas: true
  install: false  
gitlab-runner:
  # defaultWas: true
  install: false  
minio:
# This minio customization is not in the default chart, but easily found in the gitlab docs
  pullSecrets:
  - name: myregistrykey
```

After I made all the customizations I needed to, I saved the file as gitlab-values.yaml and proceeded with deploying the helm chart:

```sh
# create gitlab namespace
kubectl create ns gitlab
# add docker hub login info for pulling minio chart
docker login -u "${docker_account_username}" -p "${docker_account_password}"
kubectl create secret generic myregistrykey \
    --from-file=.dockerconfigjson="/home/${hostusername}/.docker/config.json" \
    --type=kubernetes.io/dockerconfigjson -n gitlab
# Install Gitlab helm chart
helm repo add gitlab https://charts.gitlab.io/
helm repo update
# Install Gitlab
helm upgrade --install gitlab gitlab/gitlab -n gitlab -f gitlab-values.yaml
```

At this point, all the main components of Gitlab should be installed. You can use standard kubectl commands to verify the various objects deployed correctly, for example I like the command `kubectl get all -n gitlab` to show a quick view of all the main things that were deployed and their status. 

### Making the Ingress objects

Now since I opted not to deploy the Ingresses with the gitlab helm chart, I needed to create some ingress manifests. But, its somewhere between hard and impossible to just look at existing service deployments and know what needs an ingress, there are a lot of web services in most applications that are only exposed within the cluster and not intended to be exposed externally. 

A nice trick to find the info you need for your ingress objects is to use helm to generate a file with all the kubernetes objects it would have created with the default install. Helm has 2 options to provide this type of info, you can use the `helm install` command with the `--dry-run` flag, or you can use the `helm template` command. The key difference is that the helm install --dry-run option peforms a simulated install on your cluster to try to validate for any conditions that might be experienced during installation, whereas the helm template command will still validate your configuration against a set of rules to ensure it generates valid yaml, but it does not check or validate anything on your cluster. 

For reference, I generated both a file with all the kubernetes manifests that would have been included with a default helm chart installation, and I also generated a file with all the manifests using the values file I created to be a simple reference with all the details for everything I installed with my installation. 

When you use the helm template command, while it doesnt check your cluster, it does ensure that you have entered the minimum required values for the default installation ... so you can't just enter the command like `helm template gitlab/gitlab` as that does not set the minimum required values. Fortunately the documentation has a nice reference for a standard syntax that includes setting the required values:
```sh
# This is the exact install reference from the docs https://docs.gitlab.com/charts/installation/deployment.html
helm repo add gitlab https://charts.gitlab.io/
helm repo update
helm upgrade --install gitlab gitlab/gitlab \
  --timeout 600s \
  --set global.hosts.domain=example.com \
  --set global.hosts.externalIP=10.10.10.10 \
  --set certmanager-issuer.email=me@example.com \
  --set postgresql.image.tag=13.6.0
```
You can simply add the --dry-run flag to the above command to generate the yaml files for the objects that are created. Its often desirable to get this information in the planning phase before you do you gitlab install, and if gitlab isnt installed yet, the above command won't work, but you can use the `helm template` command like this:
```sh
helm repo add gitlab https://charts.gitlab.io/
helm repo update
helm template gitlab/gitlab \
  --timeout 600s \
  --set global.hosts.domain=example.com \
  --set global.hosts.externalIP=10.10.10.10 \
  --set certmanager-issuer.email=me@example.com \
  --set postgresql.image.tag=13.6.0
```

And then to generate a copy of the manifests for the objects that get installed when using my custom values file:
```sh
helm install gitlab gitlab/gitlab -n gitlab -f gitlab-values.yaml --dry-run
# or if you have not yet installed gitlab in your cluster:
helm template gitlab/gitlab -n gitlab -f gitlab-values.yaml
```

Gitlab deploys a lot of kubernetes objects, so these will be very large files. The key piece of information I am looking for is the default Ingress options so I can see what Ingresses typically get created and what internal services the Ingresses need to forward traffic to.

You can use the `find` feature in your IDE or text editor to look through the default manifests file searching for "kind: Ingress" and it will quickly take you to the Ingress files. By default there are 4 ingresses deployed for the following services, gitlab-webservice, minio, kas, and registry. 

Here is the standard Ingress for the gitlab webservice created by the default helm deployment:
```yaml
# Source: gitlab/charts/gitlab/charts/webservice/templates/ingress.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: gitlab-webservice-default
  namespace: default
  labels:
    app: webservice
    chart: webservice-6.7.5
    release: gitlab
    heritage: Helm
    gitlab.com/webservice-name: default
    
  annotations:
    kubernetes.io/ingress.class: gitlab-nginx
    kubernetes.io/ingress.provider: "nginx"
    nginx.ingress.kubernetes.io/proxy-body-size: "512m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "15"
    cert-manager.io/issuer: "gitlab-issuer"
    nginx.ingress.kubernetes.io/service-upstream: "true"
spec:
  
  rules:
    - host: gitlab.example.com
      http:
        paths:
          - path: /
            backend:
              serviceName: gitlab-webservice-default
              servicePort: 8181
  tls:
    - hosts:
      - gitlab.example.com
      secretName: gitlab-gitlab-tls
```
This is pretty close to the object I want to create. I have already created ingress objects for Contour in the past so I know they work fine for my purposes with a minimal configuration, so I can remove most of the labels and annotations. One thing to be cautious about here is in many cases labels are used as criteria for forwarding important traffic between services, so arbitrarily removing labels can have unexpected consequences if you aren't careful. Fortunately in my case since these are ingress objects, I only need to be concerned with which objects I am forwarding traffic to as the only inbound traffic is from external sources. 

I also needed to update the cert-manager annotation to match my issuer type and name. 

There was one other challenge I ran into ... the default Ingress objects were formatted for the `extensions/v1beta1` api, and I am running kubernetes version 1.25.3 which requires that Ingress objects use the `networking.k8s.io/v1` API, which also requires a different format for the spec. I did notice afterwards that the gitlab helm values chart has a `global.ingress.apiVersion` value that can be set, and so I assume if I had set that it may have generated the manifest in the correct format, but rather than regenerating the manifests I just looked at the kubernetes Ingress documentation as a reference and updated the manifest accordingly, here is the updated manifest I used:
```yaml
apiVersion: networking.k8s.io/v1 
kind: Ingress
metadata:
  name: gitlab-webservice-default
  namespace: gitlab
  labels:
    app: webservice
    release: gitlab
    gitlab.com/webservice-name: default
  annotations:
    cert-manager.io/cluster-issuer: "my-ca-issuer"
spec:
  rules:
    - host: gitlab.tanzu.demo
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: gitlab-webservice-default
                port: 
                  number: 8181
  tls:
    - hosts:
      - gitlab.tanzu.demo
      secretName: gitlab-gitlab-tls
```

I also did the same thing for each of the other ingress objects, deployed the files, and then logged into the gitlab web interface and everything worked great. If you would like to see the all of the final ingress object yamls you can [see them in the ovathetap repo here](https://github.com/afewell/ovathetap/blob/main/assets/gitlab-ingresses.yaml).

### Adding SSH support

Another key consideration I almost missed is for `ssh` support which is not supported by ingresses and so the configuration is typically found in the loadBalancer service that is configured to forward web traffic to the ingress and ssh traffic directly to the recieving service, which for gitlab is the gitlab-shell service. The default gitlab chart installs an nginx loadbalancer service, so we can look at the sample default object files we created to see what the default load balancer configuration would have been, which we can then use to update the envoy configuration in our contour deployment. Here is the default gitlab chart loadbalancer config:
```sh
spec:
  type: LoadBalancer
  loadBalancerIP: 10.10.10.10
  externalTrafficPolicy: Local
  ipFamilyPolicy: SingleStack
  ipFamilies: 
    - IPv4
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: http
    - name: https
      port: 443
      protocol: TCP
      targetPort: https
    - name: gitlab-shell
      port: 22
      protocol: TCP
      targetPort: gitlab-shell
```

For reference, here is the envoy load balancer config from a default TAP full profile installaion in my lab environment:

```sh
spec:
  type: LoadBalancer
  allocateLoadBalancerNodePorts: true
  clusterIP: 10.101.48.192
  clusterIPs:
  - 10.101.48.192
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - name: http
    nodePort: 30788
    port: 80
    protocol: TCP
    targetPort: 8080
  - name: https
    nodePort: 30148
    port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    app: envoy
    kapp.k14s.io/app: "1674530114656710890"
  sessionAffinity: None
```

So we can see by comparing these 2 configurations, I need to update my envoy manifest with  a port configuration for ssh forwarding. 

In my lab environment, the Contour ingress controller is deployed as a Tanzu Package which uses Carvel packaging. This is in many ways similar to helm with one powerful improvment - the Tanzu Package uses the Carvel kapp-controller to reconcile your configured/desired state with the actual running state on your kubernetes cluster. This ensures that if your running configuration ever deviates from your configured/desired configuration, kapp-controller will automatically try to fix the issue and bring your running configuration back to desired state. Whereas with helm, once you deploy your application, it will do nothing on its own to ensure your running configuration stays in the desired state. 

While this is awesome, it also means we cannot just make arbitrary changes to running objects or kapp-controller will overwrite them. You have to update your deployment manifests so the kapp-controller has the correct desired configuration. 

In most cases this is done by simply updating the values file you use with your deployment - this aspect is exactly the same whether using helm or a Tanzu/Carvel package. Both Helm and Carvel make packages that deploy applications with dozens of objects with hundreds or thousands of line of configuration, and allows you to customize to your needs with a much smaller values file. To do this, the package creators try to expose the most commonly tuned parameters in the values file schema - if they exposed every possible value, the values file could be thousands of lines long. 

So it turns out in this case, the Tanzu Package for Contour does not provide a simple way to inject an additional port config into the envoy spec, so we will need to do a special patch to ensure kapp-controller is aware of our custom properties in the desired configuration for envoy. 

The first step is to create a secret with some ytt commands that includes the additional configuration settings we would like to patch in our envoy config:
```sh
# Create a manifest for the config secret
cat <<EOF > envoy-gitlab-ssh-config.yaml
apiVersion: v1
kind: Secret
metadata:
  name: envoy-gitlab-ssh-config-secret
  namespace: tap-install
stringData:
  patch.yaml: |
    #@ load("@ytt:overlay", "overlay")
    #@overlay/match by=overlay.subset({"kind":"Service","metadata":{"namespace":"tanzu-system-ingress", "name":"envoy"}})
    ---
    spec:
      #@overlay/match missing_ok=True
      ports:
        - name: gitlab-shell
          port: 22
          protocol: TCP
          targePort: gitlab-shell
EOF
# deploy the secret in your kubernetes cluster:
kubectl create -f envoy-gitlab-ssh-config.yaml
```

Next you will need to add a section to your tap values file so that it includes this secret when it deploys the configured Tanzu packages. I will only include the section you need to add to the file here, but you can view the [full tap-values file on the ovathetap repo](https://github.com/afewell/ovathetap/blob/main/assets/tap-values-2.yaml.template) if you would like to see the entire file. Here is the config you would need to add:

```sh
package_overlays:
  - name: "contour"
    secrets:
    - name: "envoy-gitlab-ssh-config-secret"
```

Once you have the secret created and your tap values file updated, you will need to update youre tap install:
```sh
tanzu package installed update tap -p tap.tanzu.vmware.com -v $TAP_VERSION  --values-file tap-values.yaml -n tap-install
```
After your tap installation has updated, you can verify that the envoy configuration was correctly updated with the command `kubectl get service envoy -n tanzu-system-ingress -oyaml` and you should see the updated ssh config:
```sh
spec:
  allocateLoadBalancerNodePorts: true
  clusterIP: 10.101.48.192
  clusterIPs:
  - 10.101.48.192
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - name: http
    nodePort: 30788
    port: 80
    protocol: TCP
    targetPort: 8080
  - name: https
    nodePort: 30148
    port: 443
    protocol: TCP
    targetPort: 8443
  - name: gitlab-shell
    nodePort: 30424
    port: 22
    protocol: TCP
    targetPort: 22
  selector:
    app: envoy
    kapp.k14s.io/app: "1674530114656710890"
  sessionAffinity: None
  type: LoadBalancer
```

### Setting up Gitlab

To configure integration between TAP and Gitlab, you will at minimum need a user access token with sufficient privileges and to create an gitlab oauth app for IAM integration. 

By default the gitlab helm chart installation creates a secret with the initial root password. The password value in this secret is base64 encoded as well. The following command grabs the password file from the secret and decodes it:
```sh
kubectl get secrets -n gitlab gitlab-gitlab-initial-root-password -o jsonpath={.data.password} | base64 -d
```

Once you have the password value, you can open a browser to the url for your gitlab instance and login to the root account with this password. Once you login, you can navigate to the `Access Tokens` section on the `Settings` page and create a new token. Since this is just a basic lab environment, I was not concerned with what the minimum token scope could be, I just created a token with full access. After you create the token, gitlab will allow you to copy it, make sure you document it well because you will not be able to view the token value again. 

You can easily use the web GUI to create a new oauth application, but I decided to create the oauth app using the gitlab API with the following commands:
```sh
create_oauth_app_response=$(curl -k --request POST --header "PRIVATE-TOKEN: ${gitlab_root_token}" \
     --data "name=tap&redirect_uri=https://tap-gui.tanzu.demo/api/auth/gitlab/handler/frame&scopes=api read_api read_user read_repository write_repository read_registry write_registry sudo openid profile email" \
     "https://gitlab.tanzu.demo/api/v4/applications")
echo ${create_oauth_app_response} | yq -p json -o yaml | tee gitlab_oauth_app_config.yaml
```
Much like with the access token, because this is a lab environment I created an oauth app that included very broad scopes, but for a production environment you would want to be sure to figure out what the minimum needed scopes are when creating the oauth app. 

You can also see in the above commands that I captured the json response from the api call, piped it to yq to format it for easier readability, and then saved the output to a file - you will want to make sure you document the output as it will have important values that you will need to configure the TAP integration. 

Before we update TAP, we will also create a repository to host the tap catalog and upload the catalog files. 

#### Prepare a repository for the TAP catalog

Now that the initial gitlab setup is done, you can create a repo to host the tap catalog files. In this case I am uploading the yelb catalog which includes some sample/example catalog files - this catalog is available when you download TAP.  

- From a web browser, login to gitlab as root (or with an admin account)
- Click `Create a group` and then `Create group` to create a group with the following settings (leave any unspecified setting at its default value):
  - Group name: tanzu
  - Visibility level: Public
  - Role: Devops Engineer
  - Who will be using this group?: My company or team
  - Click `Create group`
- Click `Create new project` and then `Create a blank project` - use the following settings (leave any unspecified setting at its default value):
  - Project name: tap-catalog
  - Visibility Level: Public
  - Initialize repository with a README: true
  - Click `Create project`
- upload catalog files to repository:
```sh
# Setup your local git client
git config --global user.name "viadmin"
git config --global user.email "viadmin@gitlab.tanzu.demo"
cd ~
git clone https://gitlab.tanzu.demo/tanzu/tap-catalog.git
# unpack tap catalog files to tap-catalog directory
tar -xvzf "/home/${hostusername}/Downloads/tap-gui-yelb-catalog.tgz" -C "/home/${hostusername}/"
cp -r "/home/${hostusername}/yelb-catalog/"* "/home/${hostusername}/tap-catalog/"
cd "/home/${hostusername}/tap-catalog/"
git add .
git commit -m "adding yelb catalog files"
git push
```

Once you have pushed the catalog to the repository, use your browser to visit the repository on the gitlab site, click on the catalog-info.yaml file and copy the URL displayed. In this case we created a repository that can be accessed from inside this lab at https://gitlab.tanzu.demo/tanzu/tap-catalog, and while this url works its actually a vanity URL that gitlab creates and you want to use the real URL value which you copied, which should look like: https://gitlab.tanzu.demo/tanzu/tap-catalog/-/blob/main/catalog-info.yaml

#### Configure the tap values file for gitlab integration

Now that you have the values needed and the url for the , you can update your tap values file to configure the TAP Gitlab integration. 

Here is the part of the tap-values file you will need to include to configure the integration, you can see where the token, oauth app client ID and secret, and catalog URL's are included respectively. I included my actual values here as these are from a temporary test environment that has already been deleted:
```sh
tap_gui:
  app_config:
    app:
      baseUrl: https://tap-gui.tanzu.demo
    integrations:
      gitlab:
      - host: gitlab.tanzu.demo
        apiBaseUrl: https://gitlab.tanzu.demo/api/v4
        token: glpat-sYqgVoJfcVxyvhxz547R 
    auth:
      providers:
        gitlab:
          development:
            clientId: 75a8e8348ba341cd4e6747962a6d691755eae0f15bc846d3830d44896e847c59
            clientSecret: 9e01836a565e5886c097cb28adaa75abd13c67b9567369ef2fe8349d45195ca1
            ## uncomment if using self-hosted GitLab
            audience: https://gitlab.tanzu.demo
            ## uncomment if using a custom redirect URI
            callbackUrl: https://tap-gui.tanzu.demo/api/auth/gitlab/handler/frame
    catalog:
      locations:
        - type: url
          target: https://gitlab.tanzu.demo/tanzu/tap-catalog/-/blob/main/catalog-info.yaml              
```

Once the tap values file has been updated, you can update the tap installation to apply the configuration:
```sh
tanzu package installed update tap -p tap.tanzu.vmware.com -v $TAP_VERSION  --values-file tap-values.yaml -n tap-install
```

After the TAP installation is updated, all the integrations should be working and ready to validate.

## Using the integrations

In this installation we setup integrations that will enable several key use cases:
1. Authentication: Your TAP installation will now require login, and will use GitLab as the authentication provider. 
2. Catalog hosting: Your TAP catalog should now display the yelb catalog files.
3. Automated Repo Creation: When deploying App Accelerators, TAP can automatically create gitlab repositories for the code to automate gitops provisioning.

Thats it! Thanks for reading!